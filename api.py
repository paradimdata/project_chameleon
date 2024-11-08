from fastapi import FastAPI, HTTPException, Body, Header, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask # Starlette underlies FastAPI
import os, shutil
import requests as r
import json
from requests import get
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import base64
import tempfile
import urllib.request
import zipfile
import traceback
from pathlib import Path
from zipfile import ZipFile
from project_chameleon.rheedconverter import rheedconverter
from project_chameleon.brukerrawbackground import brukerrawbackground
from project_chameleon.brukerrawconverter import brukerrawconverter
from project_chameleon.mbeparser import mbeparser
from project_chameleon.non4dstem import non4dstem
from project_chameleon.stemarray4d import stemarray4d
from project_chameleon.ppmsmpms import ppmsmpmsparser
from project_chameleon.arpes import arpes_folder_workbook
from project_chameleon.hs2converter import hs2converter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_path(source_path: str, allow_nonexistent_leaf: bool = False):
    # Get the canonical, absolute path of the input path
    source_path = os.path.normpath(source_path)
    canonical_path = os.path.abspath(source_path)  # Ensure we are working with the absolute path
    # Check the returned absolute path to ensure it is valid
    normalized_canonical_path = os.path.normpath(canonical_path)
    if normalized_canonical_path != canonical_path:
        raise HTTPException(status_code=400, detail=f"Error: Failed to validate path.")

    # Open and then immediately close the file or directory to ensure it's valid
    try:
        os.close(os.open(canonical_path, os.O_RDONLY))
    except Exception as e:
        if not allow_nonexistent_leaf:
            raise HTTPException(status_code=400, detail=f"Error: Failed to validate path. Reason: {str(e)}")
        try:
            # Try parent path if allow_nonexistent_leaf it set
            os.close(os.open(Path(canonical_path).parents[0], os.O_RDONLY))
        except:
            raise HTTPException(status_code=400, detail=f"Error: Failed to validate path. Reason: {str(e)}")
    return canonical_path

def validate_url(source_url: str):
    try:
        # Deconstruct the passed URL
        parts = urlparse(source_url)
        # Process the query string into parts
        qs_parts = parse_qsl(parts.query, keep_blank_values=True, strict_parsing=True) if len(parts.query) > 0 else []
        # Remake query string
        qs = urlencode(qs_parts)
        # Remake URL
        canonical_url = urlunparse([parts.scheme,parts.netloc,parts.path,parts.params,qs,parts.fragment])
        if not (canonical_url == source_url):
            raise HTTPException(status_code=400, detail=f"Error: Failed to normalize url.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: Failed to normalize url. Reason: {str(e)}")
    return canonical_url

def authorized(access_token, endpoint_id, params):
    if r.post('https://data.paradim.org/poly/api/opa', headers={'X-Auth-Access-Token': access_token}, json={ "endpoint_id": endpoint_id, "opa_json": params}).status_code == 200:
        return True
    return False # or throw not authorized exception

# access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)
def common_handler_access_token(request, data, access_token, x_auth_access_token):
    try:
        if 'access_token' in data:
            # JSON overrides header
            access_token = str(data['access_token'])
        elif len(access_token) == 0:
            access_token = x_auth_access_token
    except:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail='Malformed parameters: Access token could not be found')

    try:
        if len(str(access_token)) > 0:
            # Add header when we retrieve URLs
            # TODO: Maybe add a flag in the request JSON and only do this if requested to do so?
            opener = urllib.request.build_opener()
            opener.addheaders = [('X-Auth-Access-Token', str(access_token))]
            # TODO: does this play well with async?
            urllib.request.install_opener(opener)
    except:
        # We ignore as if this is a problem we will get an error later.
        pass

    return access_token

# er = common_handler_early_response(request, data)
# if not (er is None):
#     return er
def common_handler_early_response(request, data):
    if request.method == 'OPTIONS':
        # Handle preflight requests
        response = app.make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, access-token'
        return response
    return None

# common_handler_method_auth_check(request, data, access_token)
def common_handler_method_auth_check(request, data, access_token):
    if request.method == 'POST':
        # Paths and URLs must be normalized before calling authorized, since they can be used in authorization decisions
        # We do this on the request passed to the function, so that future steps do not need to redo the process
        if 'input_file' in data:
            data['input_file'] = validate_path(data['input_file'])
        if 'input_folder' in data:
            data['input_folder'] = validate_path(data['input_folder'])
        if 'input_url' in data:
            data['input_url'] = validate_url(data['input_url'])
        if 'output_file' in data:
            data['output_file'] = validate_path(data['output_file'], allow_nonexistent_leaf = True)
        if 'output_folder' in data:
            data['output_folder'] = validate_path(data['output_folder'], allow_nonexistent_leaf = True)
        auth_data = dict(data) # make explicit copy so we can delete items without affecting input request
        # Remove data, keeping only metadata
        if 'input_bytes' in auth_data:
            del auth_data['input_bytes']
        if 'folder_bytes' in auth_data:
            del auth_data['folder_bytes']

        if not authorized(access_token, "org.paradim.data.api.v1.chameleon", auth_data):
            raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        raise HTTPException(status_code=405, detail='Method Not Allowed')
    # Nothing to return here.

# input_file,output_file = common_file_handler_parse_request(request, data, input_ext, output_ext)
def common_file_handler_parse_request(request, data, input_ext, output_ext):
    #EXCEPTIONS
    if not (('input_file' in data) ^ ('input_bytes' in data) ^ ('input_url' in data)):
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')

    if 'output_type' in data and all(opt not in data['output_type'] for opt in ['JSON', 'raw']):
        raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON')

    if 'output_dest' in data and all(opt not in data['output_dest'] for opt in ['file', 'caller']):
            raise HTTPException(status_code=400, detail='Incorrect output_dest: output_dest options are file, caller')

    #OVERRIDE INPUT EXTENSION TYPE IF SPECIFIED
    #TODO: do a proper check to make sure this is not tryig to elide the path
    if 'file_output_type' in data and all(c in ".0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in data['file_output_type']):
        output_ext = data['file_output_type']

    #HANDLE OUTPUT
    if 'output_dest' in data and data['output_dest'] == 'file':
        if not 'output_file' in data:
            raise HTTPException(status_code=400, detail='When the output destination is file, there must be a designated output file')
        output_file = validate_path(data['output_file'], allow_nonexistent_leaf=True)
    else:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_name = temp_file.name + output_ext
        os.unlink(temp_file.name) # cleanup
        output_file = temp_name

    #OVERRIDE INPUT EXTENSION TYPE IF SPECIFIED
    #TODO: do a proper check to make sure this is not tryig to elide the path
    if 'file_input_type' in data and all(c in ".0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in data['file_input_type']):
        input_ext = data['file_input_type']

    #HANDLE INPUT
    if 'input_file' in data:
        file_name = validate_path(data['input_file'])
        return file_name, output_file

    if 'input_bytes' in data:
        decoded_data = base64.b64decode(data['input_bytes'])
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(decoded_data)
            temp_name = temp_file.name + input_ext
        os.rename(temp_file.name, temp_name)
        return temp_name, output_file

    if 'input_url' in data:
        file_url = validate_url(data['input_url'])
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_name = temp_file.name + input_ext
            os.unlink(temp_file.name) # cleanup
            urllib.request.urlretrieve(file_url, filename = temp_name)
        except r.exceptions.RequestException as e:
            traceback.print_exc()
            if e.response is not None:
                raise HTTPException(status_code=400, detail=f'Error occured while accessing {file_url}')
            else:
                raise HTTPException(status_code=400, detail=f'Request failed while accessing {file_url}')
        return temp_name, output_file

    raise HTTPException(status_code=400, detail='Malformed parameters')

def secondary_file_handler_parse_request(request, data, input_ext):
    #EXCEPTIONS
    if not (('secondary_file' in data) ^ ('secondary_bytes' in data) ^ ('secondary_url' in data)):
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')

    #OVERRIDE INPUT EXTENSION TYPE IF SPECIFIED
    #TODO: do a proper check to make sure this is not tryig to elide the path
    if 'secondary_input_type' in data and all(c in ".0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in data['file_input_type']):
        input_ext = data['file_input_type']

    #HANDLE INPUT
    if 'secondary_file' in data:
        file_name = validate_path(data['input_file'])
        return file_name

    if 'secondary_bytes' in data:
        decoded_data = base64.b64decode(data['secondary_bytes'])
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(decoded_data)
            temp_name = temp_file.name + input_ext
        os.rename(temp_file.name, temp_name)
        return temp_name

    if 'secondary_url' in data:
        file_url = validate_url(data['secondary_url'])
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_name = temp_file.name + input_ext
            os.unlink(temp_file.name) # cleanup
            urllib.request.urlretrieve(file_url, filename = temp_name)
        except r.exceptions.RequestException as e:
            traceback.print_exc()
            if e.response is not None:
                raise HTTPException(status_code=400, detail=f'Error occured while accessing {file_url}')
            else:
                raise HTTPException(status_code=400, detail=f'Request failed while accessing {file_url}')
        return temp_name
    
    raise HTTPException(status_code=400, detail='Malformed parameters')


# input_folder,output_folder,output_file = common_folder_handler_parse_request(request, data)
def common_folder_handler_parse_request(request, data):
    #EXCEPTIONS
    if not (('input_folder' in data) ^ ('input_file' in data) ^ ('input_bytes' in data) ^ ('input_url' in data)):
            raise HTTPException(status_code=400, detail='Incorrect number of parameters')

    if 'output_type' in data and all(opt not in data['output_type'] for opt in ['JSON', 'raw']):
            raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON')

    if 'output_dest' in data and all(opt not in data['output_dest'] for opt in ['folder', 'file', 'caller']):
            raise HTTPException(status_code=400, detail='Incorrect output_dest: output_dest options are folder, file, caller')

    # HANDLE OUTPUT
    if 'output_dest' in data and data['output_dest'] == 'folder':
        if not 'output_folder' in data:
            raise HTTPException(status_code=400, detail='While the output destination is a folder, there must be a designated output folder')
        output_folder = validate_path(data['output_folder'], allow_nonexistent_leaf=True)
        output_file = None # No output file needed
    elif 'output_dest' in data and data['output_dest'] == 'file':
        if not 'output_file' in data:
            raise HTTPException(status_code=400, detail='While the output destination is a file, there must be a designated output file')
        # Need temporary directory/folder
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_name = temp_file.name
        os.unlink(temp_file.name) # cleanup
        output_folder = temp_name
        output_file = validate_path(data['output_file'], allow_nonexistent_leaf=True)
    else:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_name = temp_file.name
        os.unlink(temp_file.name) # cleanup
        output_folder = temp_name
        output_file = output_folder + ".zip"

    # HANDLE INPUT
    if 'input_folder' in data:
        input_folder = validate_path(data['input_folder'])
        return input_folder, output_folder, output_file

    if 'input_file' in data:
        input_file = validate_path(data['input_file'])
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_folder = temp_file.name
        os.unlink(temp_file.name) # cleanup
        os.makedirs(temp_folder)
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            # TODO: zip allows for relative path filenames, so we need to sanitize those, otherwise this might allow overwrite of arbitrary files
            zip_ref.extractall(temp_folder)
        # No cleanup of input zip file since it is "durable"
        return temp_folder, output_folder, output_file

    if 'input_bytes' in data:
        folder_bytes = data['input_bytes']
        decoded_data = base64.b64decode(folder_bytes)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(decoded_data)
            temp_folder = temp_file.name
            temp_name = temp_file.name + '.zip'
        os.rename(temp_file.name, temp_name)
        os.makedirs(temp_folder)
        with zipfile.ZipFile(temp_name, 'r') as zip_ref:
            # TODO: zip allows for relative path filenames, so we need to sanitize those, otherwise this might allow overwrite of arbitrary files
            zip_ref.extractall(temp_folder)
        os.unlink(temp_name) # cleanup temporary input zip file
        return temp_folder, output_folder, output_file

    if 'input_url' in data:
        dir_url = validate_url(data['input_url'])
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_name = temp_file.name + ".zip"
                temp_folder = temp_file.name
            os.unlink(temp_file.name) # cleanup
            urllib.request.urlretrieve(dir_url, filename = temp_name)
            with zipfile.ZipFile(temp_name, 'r') as zip_ref:
                # TODO: zip allows for relative path filenames, so we need to sanitize those, otherwise this might allow overwrite of arbitrary files
                zip_ref.extractall(temp_folder)
            os.unlink(temp_name) # cleanup temporary input zip file
        except r.exceptions.RequestException as e:
            traceback.print_exc()
            if e.response is not None:
                raise HTTPException(status_code=400, detail=f'Error occured while accessing {dir_url}')
            else:
                raise HTTPException(status_code=400, detail=f'Request failed while accessing {dir_url}')
        return temp_folder, output_folder, output_file

    raise HTTPException(status_code=400, detail='Malformed parameters')

# response = common_folder_handler_prepare_output(request, data, output_folder, output_file)
def common_folder_handler_prepare_output(request, data, output_folder, output_file):
    # At this point, the conversion has happened and the outputs are in output_folder

    if 'output_dest' in data and data['output_dest'] == 'folder':
        return {'status': 'ok', 'message': 'Files processed successfully'}

    # If the output is anything other than 'folder', we need to turn it into a zip file
    with ZipFile(output_file, 'w') as zip_object:
        for folder_name, sub_folders, file_names in os.walk(output_folder):
            for filename in file_names:
                file_path = os.path.join(folder_name, filename)
                zip_object.write(file_path, os.path.relpath(file_path,start=output_folder))
    # and then cleanup the output folder
    shutil.rmtree(output_folder)

    # Maybe TODO: At this point, the output is a file of raw bytes. If output_type == "JSON", should
    # we rewrite the file as a valid JSON object? This seems like a case we would never use, so I
    # tend towards "no", but then the parse_request logic should be updated to disallow output type
    # JSON when the destination is "file" or "folder".

    return common_file_handler_prepare_output(request, data, output_file, 'application/zip')

# response = common_file_handler_prepare_output(request, data, output_file, media_type (opt))
def common_file_handler_prepare_output(request, data, output_file, media_type = None):
    # At this point, the conversion has happened and the output is in output_file
    # If media_type is None, FileResponse trys to decide based on filename/extension,
    # so media_type only needed when extension does not accurately represent MIME type.

    if 'output_dest' in data and data['output_dest'] == 'file':
        return {'status': 'ok', 'message': 'Files processed successfully'}

    # If we get here, output_dest is either 'caller' or unspecified; in either case, we return the file contents.
    # (remembering to cleanup the file afterwards)
    if 'output_type' in data and data['output_type'] == 'raw':
        # Raw bytes return. We do it with asynchronous cleanup of the output_file after returning it.
        return FileResponse(output_file, media_type=media_type, background=BackgroundTask(os.unlink, output_file))

    # If not specified, default to JSON return to caller.
    # TODO: make this able to stream the result and not read the entire file into memory before returning.
    with open(output_file, 'rb') as f:
        rv = Response(content=json.dumps( { 'status': 'ok', 'message': 'Files processed successfully', 'file_data': base64.b64encode(f.read()), 'file_name': os.path.basename(output_file) } ), media_type='application/json', background=BackgroundTask(os.unlink, output_file))

    return rv

# common_handler_cleanup_request(request, data, input_file, input_folder)
def common_handler_cleanup_request(request, data, input_file, input_folder):
    # Cleanup temp folder/file if used
    if not ('input_folder' in data) and ('input_file' in data or 'input_bytes' in data or 'input_url' in data) and not (input_folder is None):
        shutil.rmtree(input_folder)
    if not ('input_file' in data) and ('input_folder' in data or 'input_bytes' in data or 'input_url' in data) and not (input_file is None):
        os.remove(input_file)
    # Nothing to return

@app.post('/rheedconverter')
async def rheed_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er

    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.img', '.png')
    try:
        rheedconverter(input_file, output_file)
        return common_file_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "rheedconverter"')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)

@app.post('/brukerrawconverter')
def brukerraw_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er

    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.raw', '.csv')

    try:
        brukerrawconverter(input_file, output_file)
        return common_file_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "brukerrawconverter"')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)
    
@app.post('/mbeparser')
def MBE_parser_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    common_handler_method_auth_check(request, data, access_token)
    input_folder,output_folder,output_file = common_folder_handler_parse_request(request, data)

    try:
        mbeparser(input_folder)
        return common_folder_handler_prepare_output(request, data, output_folder, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert folder: an error occurred running the function "mbeparser"')
    finally:
        common_handler_cleanup_request(request, data, None, input_folder)
    
@app.post('/non4dstem_folder')
def non4dstem_folder_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):

    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    common_handler_method_auth_check(request, data, access_token)
    input_folder,output_folder,output_file = common_folder_handler_parse_request(request, data)
    
    try:
        non4dstem(data_folder = input_folder,outputs_folder = output_folder)
        return common_folder_handler_prepare_output(request, data, output_folder, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert folder: an error occurred running the function "non4dstem" on a folder')
    finally:
        common_handler_cleanup_request(request, data, None, input_folder)

@app.post('/non4dstem_file')
def non4dstem_file_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    
    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.emd', '.png')

    try:
        non4dstem(data_file = input_file, output_file = output_file)
        return common_file_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "non4dstem" on a file')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)
    
@app.post('/ppmsmpms')
def ppmsmpms_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    
    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.dat', '.txt') # TODO: Should this be .csv as output format?

    if 'value_name' in data:
        value = data['value_name']
    else:
        value = 1

    try:
        ppmsmpmsparser(input_file, output_file, value)
        return common_file_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "ppmsmpmsparser"')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)
    
@app.post('/stemarray4d')
def stem4d_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)
    
    er = common_handler_early_response(request, data)
    if not (er is None):
        return er

    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.raw', '') # TODO: Does the output really have no file extension? What format is it?
    try:
        stemarray4d(input_file, output_file)
        return common_folder_handler_prepare_output(request, data, output_file, media_type='application/zip')
    except:
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "stemarray4d"')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)
    
@app.post('/arpes_workbook')
def arpes_workbook_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)
    
    er = common_handler_early_response(request, data)
    if not (er is None):
        return er

    common_handler_method_auth_check(request, data, access_token)
    input_folder,output_folder,output_file = common_folder_handler_parse_request(request, data)
    try:
        arpes_folder_workbook(input_folder, output_file)
        return common_file_handler_prepare_output(request, data, output_file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert files: an error occurred running the function "arpes_folder_workbook"')
    finally:
        common_handler_cleanup_request(request, data, None, input_folder)

@app.post('/hs2converter')
async def hs2_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    
    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.hs2', '.png')

    try:
        hs2converter(input_file, output_file)
        return common_file_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "hs2converter"')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)
        
@app.post('/brukerrawbackground')
def brukerbackground_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)
    
    er = common_handler_early_response(request, data)
    if not (er is None):
        return er

    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.raw', '.csv')
    background = secondary_file_handler_parse_request(request, data, '.raw')

    try:
        brukerrawbackground(background, input_file, output_file)
        return common_folder_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "brukerrawbackground"')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)
        if ('background_file_bytes' in data) or ('background_file_url' in data):
            os.remove(background)
