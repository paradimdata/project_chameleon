from fastapi import FastAPI, HTTPException, Body, Header, Request
from fastapi.middleware.cors import CORSMiddleware
import os, shutil
import requests as r
import json
from requests import get
import base64 
import tempfile
import urllib.request
import zipfile
import traceback
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
        raise HTTPException(status_code=400, detail='Malformed parameters')

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
        auth_data = dict(data) # make explicit copy
        if 'folder_bytes' in data:
            del auth_data['folder_bytes']

        if not authorized(access_token, "org.paradim.data.api.v1.chameleon", auth_data):
            raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        raise HTTPException(status_code=405, detail='Method Not Allowed')
    # Nothing to return here.

# input_file,output_file = common_handler_parse_request(request, data)
def common_file_handler_parse_request(request, data, conversion):
    #EXCEPTIONS
    if not (('input_name' in data) ^ ('input_bytes' in data) ^ ('input_url' in data)) in data:
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')

    if 'output_type' in data and all(opt not in data['output_type'] for opt in ['JSON', 'raw', 'file']):
        raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')


    #INPUTS
    output_file = data.get('output')

    if conversion == 'rheed':
        input_ext = '.img'
        if not 'output' in data:
            output_file = 'temp.png'
    elif conversion == 'brukerraw':
        input_ext = '.raw'
        if 'file_input_type' in data:
            input_ext = data.get('file_input_type')
        if not 'output' in data:
            output_file = 'temp.txt'
    elif conversion == 'non4dstem':
        input_ext = '.emd'
        if 'file_input_type' in data:
            input_ext = data.get('file_input_type')
        if not 'output' in data:
            output_file = 'temp.png'
    elif conversion == 'ppms':
        input_ext = '.dat'
        if not 'output' in data:
            output_file = 'temp.txt'
    elif conversion == '4dstem':
        input_ext = '.raw'
        if not 'output' in data:
            output_file = 'temp'
    elif conversion == 'hs2':
        input_ext = '.hs2'
        if not 'output' in data:
            output_file = 'temp.png'
    else:
        raise HTTPException(status_code=400, detail='Conversion must be from possible file conversion types.')

    if 'input_name' in data:
        file_name = data.get('input_name')

        if not os.path.isfile(file_name):
            raise HTTPException(status_code=400, detail='Local path is not a valid file')
        return file_name, output_file

    if 'input_bytes' in data:
        file_bytes = data.get('input_bytes')

        decoded_data = base64.b64decode(file_bytes)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(decoded_data)
            temp_name = temp_file.name + input_ext
        os.rename(temp_file.name, temp_name)
        return temp_name, output_file

    if 'input_url' in data:
        file_url = data.get('input_url')
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_name = temp_file.name + input_ext
            urllib.request.urlretrieve(file_url, filename = temp_name)
        except r.exceptions.RequestException as e:
            traceback.print_exc()
            if e.response is not None:
                raise HTTPException(status_code=400, detail=f'Error occured while accessing {file_url}')
            else:
                raise HTTPException(status_code=400, detail=f'Request failed while accessing {file_url}')
        return temp_name, output_file

    raise HTTPException(status_code=400, detail='Malformed parameters')

def common_folder_handler_parse_request(request, data):
    #EXCEPTIONS
    if not (('input_name' in data) ^ ('input_bytes' in data) ^ ('input_url' in data)):
            raise HTTPException(status_code=400, detail='Incorrect number of parameters') 
    
    if 'output_type' in data and all(opt not in data['output_type'] for opt in ['JSON', 'raw', 'file']):
            raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
    #INPUTS
    if not 'output' in data:
        output = 'temp'
    elif 'output' in data:
        output = data.get('output')
    if 'input_name' in data:
        folder = data.get('folder_name')
        if not os.path.isdir(folder):
            raise HTTPException(status_code=400, detail='Local path is not a valid file')
        return folder, output

    if 'folder_bytes' in data:
        folder_bytes = data.get('folder_bytes')
        decoded_data = base64.b64decode(folder_bytes)
        with tempfile.NamedTemporaryFile(delete=False) as temp_folder:
            temp_folder.write(decoded_data)
            temp_name = temp_folder.name + '.zip'
        os.rename(temp_folder.name, temp_name)
        if not os.path.exists('temp_dir'):
            os.makedirs('temp_dir')
        with zipfile.ZipFile(temp_name, 'r') as zip_ref:
            zip_ref.extractall('temp_dir')
        folder = 'temp_dir'
        return folder, output

    if 'folder_url' in data:
        folder_url = data.get('folder_url')
        urllib.request.urlretrieve(folder_url, filename = 'temp.zip')
        with zipfile.ZipFile('temp.zip', 'r') as zip_ref:
            zip_ref.extractall('temp_dir') 
        folder = 'temp_dir' 
        return folder, output

def common_folder_handler_prepare_output(request, data, input_folder, output_folder, result):
    if output_folder == None:
        output_folder = input_folder
    if 'output_type' in data:
        if data.get('output_type') == 'raw':
            with ZipFile('chameleon_output.zip', 'w') as zip_object:
                for folder_name, sub_folders, file_names in os.walk(output_folder):
                    for filename in file_names:
                        file_path = os.path.join(folder_name, filename)
                        zip_object.write(file_path, os.path.basename(file_path))
            with open('chameleon_output.zip', 'rb') as file:
                encoded_data = file.read()
                out = encoded_data
            if ('folder_bytes' or 'folder_url') in data:
                shutil.rmtree(input_folder)
            os.remove('chameleon_output.zip')
        elif data.get('output_type') == 'JSON':
            with ZipFile('chameleon_output.zip', 'w') as zip_object:
                for folder_name, sub_folders, file_names in os.walk(output_folder):
                    for filename in file_names:
                        file_path = os.path.join(folder_name, filename)
                        zip_object.write(file_path, os.path.basename(file_path))
            with open('chameleon_output.zip', 'rb') as file:
                encoded_data = file.read()
            with open('mbe_out_json', 'w') as json_file:
                json.dump({"file_data": encoded_data}, json_file)
                out = json_file
            if ('folder_bytes' or 'folder_url') in data:
                shutil.rmtree(input_folder)
            os.remove('chameleon_output.zip')

        else:
            out = None
    else:
        out = None

    if result is None:
        if out:
            return out
        else:
            return {'message': 'Files processed successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    
# common_handler_prepare_output(request, data, input_file, output_file, request)
def common_file_handler_prepare_output(request, data, input_file, output_file, result):
    #OUTPUTS
    if 'output_type' in data:
        if data.get('output_type') == 'raw':
            with open(output_file, 'rb') as file:
                encoded_data = file.read()
                out = encoded_data
                os.remove(output_file)
        elif data.get('output_type') == 'JSON':
            with open(output_file, 'rb') as file:
                encoded_data = file.read()
            with open('output_json', 'w') as json_file:
                json.dump({"file_data": encoded_data}, json_file)
                out = json_file
            os.remove(output_file)
        elif data.get('output_type') == 'file':
            out = output_file
    else:
        out = None

    if result is None:
        if out:
            return out
        else:
            return {'message': 'Image converted successfully'}
    
    raise HTTPException(status_code=500, detail=f'Failed to convert file')

# common_handler_cleanup_request(request, data, input_file, output_file)
def common_handler_cleanup_request(request, data, input_file, output_file):
    if not ('file_name' in data) and ('file_bytes' in data or 'file_url' in data):
        # Cleanup temp input file
        os.remove(input_file)
    # Nothing to return

def common_folder_handler_cleanup_request(request, data, input_folder, output_file):
    if not ('folder_name' in data) and ('folder_bytes' in data or 'folder_url' in data):
        # Cleanup temp input file
        os.remove(input_folder)
    # Nothing to return

@app.post('/rheedconverter')
async def rheed_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):  
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)
    
    er = common_handler_early_response(request, data)
    if not (er is None):
        return er

    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, 'rheed')
    try:
        result = rheedconverter(input_file, output_file)
        return common_file_handler_prepare_output(request, data, input_file, output_file, result)
    except:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    finally:
        common_handler_cleanup_request(request, data, input_file, output_file)

@app.post('/brukerrawconverter')
def brukerraw_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    
    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, 'brukerraw')
    
    try:
        result = brukerrawconverter(input_file, output_file)
        return common_file_handler_prepare_output(request, data, input_file, output_file, result)
    except:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    finally:
        common_handler_cleanup_request(request, data, input_file, output_file)
    
@app.post('/mbeparser')
def MBE_parser_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    common_handler_method_auth_check(request, data, access_token)
    input_folder,output_folder = common_folder_handler_parse_request(request, data)
    
    try:
        result = mbeparser(input_folder)
        return common_folder_handler_prepare_output(request, data, input_folder, output_folder, result)
    except:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    finally:
        common_folder_handler_cleanup_request(request, data, input_folder, output_folder)
    
@app.post('/non4dstem_folder')
def non4dstem_folder_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):

    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    common_handler_method_auth_check(request, data, access_token)
    input_folder,output_folder = common_folder_handler_parse_request(request, data)
    
    try:
        result = result = non4dstem(data_folder = input_folder,outputs_folder = output_folder)
        return common_folder_handler_prepare_output(request, data, input_folder, output_folder, result)
    except:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    finally:
        common_folder_handler_cleanup_request(request, data, input_folder, output_folder)

@app.post('/non4dstem_file')
def non4dstem_file_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    
    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, 'non4stem')

    try:
        result = non4dstem(data_file = input_file, output_file = output_file)
        return common_file_handler_prepare_output(request, data, input_file, output_file, result)
    except:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    finally:
        common_handler_cleanup_request(request, data, input_file, output_file)
    
@app.post('/ppmsmpms')
def ppmsmpms_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    
    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, 'ppms')

    if 'value_name' in data:
        value = data.get('value_name')
    else:
        value = 1

    try:
        result = ppmsmpmsparser(input_file, output_file, value)
        return common_file_handler_prepare_output(request, data, input_file, output_file, result)
    except:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    finally:
        common_handler_cleanup_request(request, data, input_file, output_file)
    
@app.post('/stemarray4d')
def stem4d_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):

    try:
        if 'access_token' in data:
            # JSON overrides header
            access_token = str(data['access_token'])
        elif len(access_token) == 0:
            access_token = x_auth_access_token
    except:
        raise HTTPException(status_code=400, detail='Malformed parameters')

    try:
        if len(str(access_token)) > 0:
            # Add header when we retrieve URLs
            # TODO: Maybe add a flag in the request JSON and only do this if requested to do so?
            opener = urllib.request.build_opener()
            opener.addheaders = [('X-Auth-Access-Token', str(access_token))]
            urllib.request.install_opener(opener)
    except:
        # We ignore as if this is a problem we will get an error later.
        pass

    if request.method == 'OPTIONS':
        # Handle preflight requests
        response = app.make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, access-token'
        return response
    elif request.method == 'POST':
        #EXCEPTIONS
        if not (('file_name' in data) ^ ('file_bytes' in data) ^ ('file_url' in data)) or 'output_file' not in data:
            raise HTTPException(status_code=400, detail='Incorrect number of parameters')
        
        if 'output_type' in data and all(opt not in data['output_type'] for opt in ['JSON', 'raw', 'file']):
                raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
        
        auth_data = dict(data)
        if 'file_bytes' in data:
            del auth_data['file_bytes']

        if not authorized(access_token, "org.paradim.data.api.v1.chameleon", auth_data):
            raise HTTPException(status_code=401, detail='Unauthorized')

        if 'file_name' in data:
            file_name = data.get('file_name')
            output_file = data.get('output_file')

            if not os.path.isfile(file_name):
                raise HTTPException(status_code=400, detail='Local path is not a valid file')
            result = stemarray4d(file_name, output_file)

        if 'file_bytes' in data:
            file_bytes = data.get('file_bytes')
            output_file = data.get('output_file')

            decoded_data = base64.b64decode(file_bytes)
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(decoded_data)
                temp_name = temp_file.name + '.raw'
            os.rename(temp_file.name, temp_name)
            output_file = os.path.join(tempfile.gettempdir(), output_file)
            result = stemarray4d(temp_name, output_file)
            os.remove(temp_name)

        if 'file_url' in data:
            file_url = data.get('file_url')
            output_file = data.get('output_file')

            urllib.request.urlretrieve(file_url, filename = 'temp_name.raw') 
            result = stemarray4d('temp_name.raw', output_file)
            os.remove('temp_name.raw')

        if 'output_type' in data:
            if data.get('output_type') == 'raw':
                with zipfile.ZipFile('stem4d_output.zip', 'w') as zipf:
                    for root, dirs, files in os.walk(output_file):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, output_file))
                with open('stem4d_output.zip', 'rb') as file:
                    encoded_data = base64.b64encode(file.read()).decode('utf-8')
                    out = encoded_data
                shutil.rmtree(output_file + 'array')
            elif data.get('output_type') == 'JSON':
                with zipfile.ZipFile('stem4d_output.zip', 'w') as zipf:
                    for root, dirs, files in os.walk(output_file):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, output_file))
                with open('stem4d_output.zip', 'rb') as file:
                    encoded_data = base64.b64encode(file.read()).decode('utf-8')
                with open('stem4d_out_json', 'w') as json_file:
                    json.dump({"file_data": encoded_data}, json_file)
                    out = json_file
                shutil.rmtree(output_file + 'array')
            else:
                out = None
        else:
            out = None

        if result is None:
            if out:
                return {'message': 'Image converted successfully'}, out
            else:
                return {'message': 'Image converted successfully'}
        else:
            raise HTTPException(status_code=500, detail=f'Failed to convert file')
    
@app.post('/arpes_workbook')
def arpes_workbook_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):

    try:
        if 'access_token' in data:
            # JSON overrides header
            access_token = str(data['access_token'])
        elif len(access_token) == 0:
            access_token = x_auth_access_token
    except:
        raise HTTPException(status_code=400, detail='Malformed parameters')

    try:
        if len(str(access_token)) > 0:
            # Add header when we retrieve URLs
            # TODO: Maybe add a flag in the request JSON and only do this if requested to do so?
            opener = urllib.request.build_opener()
            opener.addheaders = [('X-Auth-Access-Token', str(access_token))]
            urllib.request.install_opener(opener)
    except:
        # We ignore as if this is a problem we will get an error later.
        pass

    if request.method == 'OPTIONS':
        # Handle preflight requests
        response = app.make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, access-token'
        return response
    elif request.method == 'POST':
        #EXCEPTIONS
        if not (('folder_name' in data) ^ ('folder_bytes' in data) ^ ('folder_url' in data)) or 'output_file' not in data:
            raise HTTPException(status_code=400, detail='Incorrect number of parameters')
        
        if 'output_type' in data and all(opt not in data['output_type'] for opt in ['JSON', 'raw', 'file']):
                raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
        
        auth_data = dict(data)
        if 'folder_bytes' in data:
            del auth_data['folder_bytes']

        if not authorized(access_token, "org.paradim.data.api.v1.chameleon", auth_data):
            raise HTTPException(status_code=401, detail='Unauthorized')

        #INPUTS
        result = None
        output = data.get('output_file')
        if 'folder_name' in data:
            file_folder = data.get('folder_name')

            if not os.path.isdir(file_folder):
                raise HTTPException(status_code=400, detail='Local path is not a valid directory')
            result = arpes_folder_workbook(file_folder, output)
        
        if 'folder_bytes' in data:
            folder_bytes = data.get('folder_bytes')

            decoded_data = base64.b64decode(folder_bytes)
            with tempfile.NamedTemporaryFile(delete=False) as temp_folder:
                temp_folder.write(decoded_data)
                temp_name = temp_folder.name + '.zip'
            os.rename(temp_folder.name, temp_name)
            if not os.path.exists('temp_dir'):
                os.makedirs('temp_dir')
            with zipfile.ZipFile(temp_name, 'r') as zip_ref:
                zip_ref.extractall('temp_dir')
            folder = 'temp_dir/' + os.listdir('temp_dir')[0]
            result = arpes_folder_workbook(file_folder, output)
            shutil.rmtree('temp_dir')

        if 'folder_url' in data:
            folder_url = data.get('folder_url')

            urllib.request.urlretrieve(folder_url, filename = 'non4dstem_data.zip')
            with zipfile.ZipFile('non4dstem_data.zip', 'r') as zip_ref:
                zip_ref.extractall('temp_dir') 
            folder = 'temp_dir/' + os.listdir('temp_dir')[0]
            result = arpes_folder_workbook(file_folder, output)
            shutil.rmtree('temp_dir')

        #OUTPUTS
        if 'output_type' in data:
            if data.get('output_type') == 'raw':
                with open(output, 'rb') as file:
                    encoded_data = base64.b64encode(file.read()).decode('utf-8')
                    out = encoded_data
                    os.remove(output)
            elif data.get('output_type') == 'JSON':
                with open(output, 'rb') as file:
                    encoded_data = base64.b64encode(file.read()).decode('utf-8')
                with open('ppms_out_json', 'w') as json_file:
                    json.dump({"file_data": encoded_data}, json_file)
                    out = json_file
                os.remove(output)
            else:
                out = None
        else:
            out = None

        if result is None:
            if out:
                return out
            else:
                return {'message': 'File converted successfully'}
        else:
            raise HTTPException(status_code=500, detail=f'Failed to convert file')
        
@app.post('/hs2converter')
async def hs2_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):  
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    
    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, 'hs2')

    try:
        result = hs2converter(input_file, output_file)
        return common_file_handler_prepare_output(request, data, input_file, output_file, result)
    except:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    finally:
        common_handler_cleanup_request(request, data, input_file, output_file)  
        
@app.post('/brukerrawbackground')
def brukerbackground_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):

    try:
        if 'access_token' in data:
            # JSON overrides header
            access_token = str(data['access_token'])
        elif len(access_token) == 0:
            access_token = x_auth_access_token
    except:
        raise HTTPException(status_code=400, detail='Malformed parameters')

    try:
        if len(str(access_token)) > 0:
            # Add header when we retrieve URLs
            # TODO: Maybe add a flag in the request JSON and only do this if requested to do so?
            opener = urllib.request.build_opener()
            opener.addheaders = [('X-Auth-Access-Token', str(access_token))]
            urllib.request.install_opener(opener)
    except:
        # We ignore as if this is a problem we will get an error later.
        pass

    if request.method == 'OPTIONS':
        # Handle preflight requests
        response = app.make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, access-token'
        return response
    elif request.method == 'POST':
        #EXCEPTIONS
        if not (('background_file_name' in data) ^ ('background_file_bytes' in data) ^ ('background_file_url' in data)) or not (('file_name' in data) ^ ('file_bytes' in data) ^ ('file_url' in data)) or 'output_file' not in data:
            raise HTTPException(status_code=400, detail='Incorrect number of parameters')
        
        if 'output_type' in data and all(opt not in data['output_type'] for opt in ['JSON', 'raw', 'file']):
                raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
                    
        if 'background_input_type' in data:
            if not '.raw' in data.get('background_input_type'):
                if not '.csv' in data.get('background_input_type'):
                    raise HTTPException(status_code=400, detail='Incorrect file extension: background_input_type options are .raw and .csv')
        
        if 'input_type' in data:
            if not '.raw' in data.get('nput_type'):
                if not '.csv' in data.get('input_type'):
                    raise HTTPException(status_code=400, detail='Incorrect file extension: sample_input_type options are .raw and .csv')
                
        auth_data = dict(data)
        if 'folder_bytes' in data:
            del auth_data['folder_bytes']

        if not authorized(access_token, "org.paradim.data.api.v1.chameleon", auth_data):
            raise HTTPException(status_code=401, detail='Unauthorized')

        #INPUTS 
        background_ext = '.raw'
        sample_ext = '.raw'
        if 'background_input_type' in data:
            background_ext = data.get('background_input_type')
        if 'input_type' in data:
            sample_ext = data.get('input_type')

        if 'background_file_name' in data:
            background = data.get('background_file_name')
            if not os.path.isfile(background):
                raise HTTPException(status_code=400, detail='Local path is not a valid file')

        if 'file_name' in data:    
            sample = data.get('file_name')
            if not os.path.isfile(sample):
                raise HTTPException(status_code=400, detail='Local path is not a valid file')
            
        if 'background_file_bytes' in data:
            background_file_bytes = data.get('background_file_bytes')
            decoded_data = base64.b64decode(background_file_bytes)
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(decoded_data)
                background = temp_file.name + background_ext
            os.rename(temp_file.name, background)
            

        if 'file_bytes' in data:
            sample_file_bytes = data.get('file_bytes')
            decoded_data = base64.b64decode(sample_file_bytes)
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(decoded_data)
                sample = temp_file.name + sample_ext
            os.rename(temp_file.name, sample)   

        if 'background_file_url' in data:
            background_file_url = data.get('background_file_url')
            urllib.request.urlretrieve(background_file_url, filename = 'background_temp_name' + background_ext) 
            background = 'background_temp_name' + background_ext

        if 'file_url' in data:
            sample_file_url = data.get('file_url')
            urllib.request.urlretrieve(sample_file_url, filename = 'sample_temp_name' + sample_ext) 
            sample = 'sample_temp_name' + sample_ext

        output_file = data.get('output_file')
        result = brukerrawbackground(background, sample, output_file)

        if ('background_file_bytes' in data) or ('file_url' in data):
            os.remove(background)
        if ('file_bytes' in data) or ('background_file_url' in data):
            os.remove(sample)

        #OUTPUT
        if 'output_type' in data:
            if data.get('output_type') == 'raw':
                file_paths = [output_file + '_raw_data.png', output_file + '_background_adjusted.png', output_file + '_background_subtracted.png', output_file + '_backgroundSubtracted.csv']
                encoded_files = {}
                for file_path in file_paths:
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as file:
                            encoded_data = base64.b64encode(file.read()).decode('utf-8')
                            encoded_files[os.path.basename(file_path)] = encoded_data
                out = encoded_files
                for file_path in file_paths:
                    os.remove(file_path)
            if data.get('output_type') == 'JSON':
                file_paths = [output_file + '_raw_data.png', output_file + '_background_adjusted.png', output_file + '_background_subtracted.png', output_file + '_backgroundSubtracted.csv']
                encoded_files = {}
                for file_path in file_paths:
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as file:
                            encoded_data = base64.b64encode(file.read()).decode('utf-8')
                            encoded_files[os.path.basename(file_path)] = encoded_data
                with open('bruker_background_out_json', 'w') as json_file:
                    json.dump({"file_data": encoded_files}, json_file)
                    out = json_file
                for file_path in file_paths:
                    os.remove(file_path)
            else:
                out = None
        else:
            out = None

        if result is None:
            if out:
                return {'message': 'Background subtracted files generated successfully'}, out
            else:
                return {'message': 'Background subtracted files generated successfully'}
        else:
            raise HTTPException(status_code=500, detail=f'Failed to convert file')
