from fastapi import FastAPI, HTTPException, Body, Header
import os
import requests as r
import json
from requests import get
import base64 
import tempfile
import urllib.request
import zipfile
from project_chameleon.rheedconverter import rheedconverter
from project_chameleon.brukerrawbackground import brukerrawbackground
from project_chameleon.brukerrawconverter import brukerrawconverter
from project_chameleon.mbeparser import mbeparser
from project_chameleon.non4dstem import non4dstem
from project_chameleon.stemarray4d import stemarray4d
from project_chameleon.ppmsmpms import ppmsmpmsparser

app = FastAPI()

def authorized(access_token, endpoint_id, params):
    if r.post('https://data.paradim.org/poly/api/opa', headers={'X-Auth-Access-Token': access_token}, json={ "endpoint_id": endpoint_id, "opa_json": params}).status_code == 200:
        return True
    return False # or throw not authorized exception

@app.post('/rheedconverter')
def rheed_convert_route(data: dict = Body(...), access_token: str = Header(...)):   

    #EXCEPTIONS
    if not (('file_name' in data) ^ ('file_bytes' in data) ^ ('file_url' in data)) or 'output_file' not in data:
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')
    
    if 'output_type' in data: 
        if not 'JSON' in data.get('output_type'):
            if not 'raw' in data.get('output_type'):
                if not 'file' in data.get('output_type'):
                    raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
    
    if not authorized(access_token, "org.paradim.data.api.v1.chameleon", data):
        raise HTTPException(status_code=401, detail='Unauthorized')

    #INPUTS
    if 'file_name' in data:
        file_name = data.get('file_name')
        output_file = data.get('output_file')

        if not os.path.isfile(file_name):
            raise HTTPException(status_code=400, detail='Local path is not a valid file')
        result = rheedconverter(file_name, output_file)
    
    if 'file_bytes' in data:
        file_bytes = data.get('file_bytes')
        output_file = data.get('output_file')

        decoded_data = base64.b64decode(file_bytes)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(decoded_data)
            temp_name = temp_file.name + '.img'
        os.rename(temp_file.name, temp_name)
        output_file = os.path.join(tempfile.gettempdir(), output_file)
        result = rheedconverter(temp_name, output_file)
        os.remove(temp_name)

    if 'file_url' in data:
        file_url = data.get('file_url')
        output_file = data.get('output_file')

        urllib.request.urlretrieve(file_url, filename = 'temp_name.img') 
        result = rheedconverter('temp_name.img', output_file)
        os.remove('temp_name.img')

    #OUTPUTS
    if 'output_type' in data:
        if data.get('output_type') == 'raw':
            with open(output_file, 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
                out = encoded_data
                os.remove(output_file)
        elif data.get('output_type') == 'JSON':
            with open(output_file, 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
            with open('rheed_out_json', 'w') as json_file:
                json.dump({"file_data": encoded_data}, json_file)
                out = json_file
            os.remove(output_file)
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
    
@app.post('/brukerrawbackground')
def brukerbackground_convert_route(data: dict = Body(...), access_token: str = Header(...)):

    #EXCEPTIONS
    if not (('background_file_name' in data) ^ ('background_file_bytes' in data) ^ ('background_file_url' in data)) or not (('sample_file_name' in data) ^ ('sample_file_bytes' in data) ^ ('sample_file_url' in data)) or 'output_file' not in data:
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')
    
    if 'output_type' in data: 
        if not 'JSON' in data.get('output_type'):
            if not 'raw' in data.get('output_type'):
                if not 'file' in data.get('output_type'):
                    raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
                
    if 'background_input_type' in data:
        if not '.raw' in data.get('background_input_type'):
            if not '.csv' in data.get('background_input_type'):
                raise HTTPException(status_code=400, detail='Incorrect file extension: background_input_type options are .raw and .csv')
    
    if 'sample_input_type' in data:
        if not '.raw' in data.get('sample_input_type'):
            if not '.csv' in data.get('sample_input_type'):
                raise HTTPException(status_code=400, detail='Incorrect file extension: sample_input_type options are .raw and .csv')
            
    if not authorized(access_token, "org.paradim.data.api.v1.chameleon", data):
        raise HTTPException(status_code=401, detail='Unauthorized')

    #INPUTS 
    background_ext = '.raw'
    sample_ext = '.raw'
    if 'background_input_type' in data:
        background_ext = data.get('background_input_type')
    if 'sample_input_type' in data:
        sample_ext = data.get('sample_input_type')

    if 'background_file_name' in data:
        background = data.get('background_file_name')
        if not os.path.isfile(background):
            raise HTTPException(status_code=400, detail='Local path is not a valid file')

    if 'sample_file_name' in data:    
        sample = data.get('sample_file_name')
        if not os.path.isfile(sample):
            raise HTTPException(status_code=400, detail='Local path is not a valid file')
        
    if 'background_file_bytes' in data:
        background_file_bytes = data.get('background_file_bytes')
        decoded_data = base64.b64decode(background_file_bytes)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(decoded_data)
            background = temp_file.name + background_ext
        os.rename(temp_file.name, background)
        

    if 'sample_file_bytes' in data:
        sample_file_bytes = data.get('sample_file_bytes')
        decoded_data = base64.b64decode(sample_file_bytes)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(decoded_data)
            sample = temp_file.name + sample_ext
        os.rename(temp_file.name, sample)   

    if 'background_file_url' in data:
        background_file_url = data.get('background_file_url')
        urllib.request.urlretrieve(background_file_url, filename = 'background_temp_name' + background_ext) 
        background = 'background_temp_name' + background_ext

    if 'sample_file_url' in data:
        background_file_url = data.get('background_file_url')
        urllib.request.urlretrieve(background_file_url, filename = 'background_temp_name' + sample_ext) 
        background = 'background_temp_name' + sample_ext

    output_file = data.get('output_file')
    result = brukerrawbackground(background, sample, output_file)

    if ('background_file_bytes' in data) or ('background_file_url' in data):
        os.remove(background)
    if ('sample_file_bytes' in data) or ('background_file_url' in data):
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
    
@app.post('/brukerrawconverter')
def brukerraw_convert_route(data: dict = Body(...), access_token: str = Header(...)):

    #EXCEPTIONS
    if not (('file_name' in data) ^ ('file_bytes' in data) ^ ('file_url' in data)) or 'output_file' not in data:
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')
    
    if 'output_type' in data: 
        if not 'JSON' in data.get('output_type'):
            if not 'raw' in data.get('output_type'):
                if not 'file' in data.get('output_type'):
                    raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
    
    if not authorized(access_token, "org.paradim.data.api.v1.chameleon", data):
        raise HTTPException(status_code=401, detail='Unauthorized')

    #INPUTS
    input_ext = '.raw'
    if 'file_input_type' in data:
        input_ext = data.get('file_input_type')

    if 'file_name' in data:
        file_name = data.get('file_name')
        output_file = data.get('output_file')

        if not os.path.isfile(file_name):
            raise HTTPException(status_code=400, detail='Local path is not a valid file')
        result = brukerrawconverter(file_name, output_file)
    
    if 'file_bytes' in data:
        file_bytes = data.get('file_bytes')
        output_file = data.get('output_file')

        decoded_data = base64.b64decode(file_bytes)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(decoded_data)
            temp_name = temp_file.name + input_ext
        os.rename(temp_file.name, temp_name)
        output_file = os.path.join(tempfile.gettempdir(), output_file)
        result = brukerrawconverter(temp_name, output_file)
        os.remove(temp_name)

    if 'file_url' in data:
        file_url = data.get('file_url')
        output_file = data.get('output_file')

        urllib.request.urlretrieve(file_url, filename = 'temp_name' + input_ext) 
        result = brukerrawconverter('temp_name' + input_ext, output_file)
        os.remove('temp_name' + input_ext)

    #OUTPUTS
    if 'output_type' in data:
        if data.get('output_type') == 'raw':
            with open(output_file, 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
                out = encoded_data
                os.remove(output_file)
        elif data.get('output_type') == 'JSON':
            with open(output_file, 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
            with open('brukerraw_out_json', 'w') as json_file:
                json.dump({"file_data": encoded_data}, json_file)
                out = json_file
            os.remove(output_file)
        else:
            out = None
    else:
        out = None

    if result is None:
        if out:
            return {'message': 'File converted successfully'}, out
        else:
            return {'message': 'File converted successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    
@app.post('/mbeparser')
def MBE_parser_route(data: dict = Body(...), access_token: str = Header(...)):

    #EXCEPTIONS
    if not (('folder_name' in data) ^ ('folder_bytes' in data) ^ ('folder_url' in data)):
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')
    
    if 'output_type' in data: 
        if not 'JSON' in data.get('output_type'):
            if not 'raw' in data.get('output_type'):
                if not 'file' in data.get('output_type'):
                    raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
    
    if not authorized(access_token, "org.paradim.data.api.v1.chameleon", data):
        raise HTTPException(status_code=401, detail='Unauthorized')

    #INPUTS
    if 'folder_name' in data:
        folder = data.get('folder_name')
        if not os.path.isdir(folder):
            raise HTTPException(status_code=400, detail='Local path is not a valid file')
        result = mbeparser(folder)

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
        result = mbeparser(folder)

    if 'folder_url' in data:
        folder_url = data.get('folder_url')
        urllib.request.urlretrieve(folder_url, filename = 'temp_dir') 
        folder = 'temp_dir'
        result = mbeparser(folder)

    if 'output_type' in data:
        if data.get('output_type') == 'raw':
            with zipfile.ZipFile('mbe_output.zip', 'w') as zipf:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, folder))
            with open('mbe_output.zip', 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
                out = encoded_data
                os.remove(folder)
        elif data.get('output_type') == 'JSON':
            with zipfile.ZipFile('mbe_output.zip', 'w') as zipf:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, folder))
            with open('stem4d_output.zip', 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
            with open('mbe_out_json', 'w') as json_file:
                json.dump({"file_data": encoded_data}, json_file)
                out = json_file
            os.remove(folder)
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
    
@app.post('/non4dstem')
def non4dstem_convert_route(data: dict = Body(...), access_token: str = Header(...)):
    #EXCEPTIONS
    if not (('folder_name' in data) ^ ('folder_bytes' in data) ^ ('folder_url' in data)) or 'output_folder' not in data:
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')
    
    if 'output_type' in data: 
        if not 'JSON' in data.get('output_type'):
            if not 'raw' in data.get('output_type'):
                if not 'file' in data.get('output_type'):
                    raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
    
    if not authorized(access_token, "org.paradim.data.api.v1.chameleon", data):
        raise HTTPException(status_code=401, detail='Unauthorized')

    #INPUTS
    result = None
    if 'folder_name' in data:
        file_folder = data.get('folder_name')
        output_folder = data.get('output_folder')

        if not os.path.isdir(file_folder):
            raise HTTPException(status_code=400, detail='Local path is not a valid directory')
        result = non4dstem(file_folder, output_folder)
    
    if 'folder_bytes' in data:
        folder_bytes = data.get('folder_bytes')
        output_folder = data.get('output_folder')

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
        result = non4dstem(folder, output_folder)
        os.remove(folder)

    if 'folder_url' in data:
        folder_url = data.get('folder_url')
        output_folder = data.get('output_folder')

        urllib.request.urlretrieve(folder_url, filename = 'temp_name') 
        result = non4dstem('temp_name', output_folder)
        os.remove('temp_name')

    #OUTPUTS
    if 'output_type' in data:
        if data.get('output_type') == 'raw':
            with zipfile.ZipFile('non4dstem_output.zip', 'w') as zipf:
                for root, dirs, files in os.walk(output_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, output_folder))
            with open('non4dstem_output.zip', 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
                out = encoded_data
                os.remove(output_folder)
        elif data.get('output_type') == 'JSON':
            with zipfile.ZipFile('non4stem_output.zip', 'w') as zipf:
                for root, dirs, files in os.walk(output_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, output_folder))
            with open('stem4d_output.zip', 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
            with open('non4dstem_out_json', 'w') as json_file:
                json.dump({"file_data": encoded_data}, json_file)
                out = json_file
            os.remove(output_folder)
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
    
@app.post('/ppmsmpms')
def ppmsmpms_convert_route(data: dict = Body(...), access_token: str = Header(...)):
    #EXCEPTIONS
    if not (('file_name' in data) ^ ('file_bytes' in data) ^ ('file_url' in data)) or 'output_file' not in data:
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')
    
    if 'output_type' in data: 
        if not 'JSON' in data.get('output_type'):
            if not 'raw' in data.get('output_type'):
                if not 'file' in data.get('output_type'):
                    raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
    
    if not authorized(access_token, "org.paradim.data.api.v1.chameleon", data):
        raise HTTPException(status_code=401, detail='Unauthorized')

    #INPUTS
    if 'file_name' in data:
        file_name = data.get('file_name')
        output_file = data.get('output_file')

        if not os.path.isfile(file_name):
            raise HTTPException(status_code=400, detail='Local path is not a valid file')
        result = ppmsmpmsparser(file_name, output_file)
    
    if 'file_bytes' in data:
        file_bytes = data.get('file_bytes')
        output_file = data.get('output_file')

        decoded_data = base64.b64decode(file_bytes)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(decoded_data)
            temp_name = temp_file.name + '.dat'
        os.rename(temp_file.name, temp_name)
        output_file = os.path.join(tempfile.gettempdir(), output_file)
        result = ppmsmpmsparser(temp_name, output_file)
        os.remove(temp_name)

    if 'file_url' in data:
        file_url = data.get('file_url')
        output_file = data.get('output_file')

        urllib.request.urlretrieve(file_url, filename = 'temp_name.dat') 
        result = ppmsmpmsparser('temp_name.dat', output_file)
        os.remove('temp_name.dat')

    #OUTPUTS
    if 'output_type' in data:
        if data.get('output_type') == 'raw':
            with open(output_file, 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
                out = encoded_data
                os.remove(output_file)
        elif data.get('output_type') == 'JSON':
            with open(output_file, 'rb') as file:
                encoded_data = base64.b64encode(file.read()).decode('utf-8')
            with open('ppms_out_json', 'w') as json_file:
                json.dump({"file_data": encoded_data}, json_file)
                out = json_file
            os.remove(output_file)
        else:
            out = None
    else:
        out = None

    if result is None:
        if out:
            return {'message': 'File converted successfully'}, out
        else:
            return {'message': 'File converted successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    
@app.post('/stemarray4d')
def stem4d_convert_route(data: dict = Body(...), access_token: str = Header(...)):
    #EXCEPTIONS
    if not (('file_name' in data) ^ ('file_bytes' in data) ^ ('file_url' in data)) or 'output_file' not in data:
        raise HTTPException(status_code=400, detail='Incorrect number of parameters')
    
    if 'output_type' in data: 
        if not 'JSON' in data.get('output_type'):
            if not 'raw' in data.get('output_type'):
                if not 'file' in data.get('output_type'):
                    raise HTTPException(status_code=400, detail='Incorrect output_type: output_type options are raw, JSON, file')
    
    if not authorized(access_token, "org.paradim.data.api.v1.chameleon", data):
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
                os.remove(output_file)
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
            os.remove(output_file)
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
    


#curl -X POST \
#  -H "Content-Type: application/json" \
#  -d '{"source": "box:/PARADIM_DOI_UPLOAD/10.34863_xxxx-xxxx/", "local_path": "srv/zpool01/paradim-data/paradim.jhu.edu/doi/xxxx-xxxx"}' \
#  http://localhost:5020/copy-fil