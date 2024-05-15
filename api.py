from fastapi import FastAPI, HTTPException, Body
import os
from project_chameleon.RHEED.rheedconverter import rheedconverter
from project_chameleon.XRD.BrukerRAW.brukerrawbackground import brukerrawbackground
from project_chameleon.XRD.BrukerRAW.brukerrawconverter import brukerrawconverter
from project_chameleon.MBE.mbeparser import mbeparser
from project_chameleon.nonfourdimension_stem.non4dstem import non4dstem
from project_chameleon.fourdimension_stem.stemarray4d import stemarray4d
from project_chameleon.ppmsmpms.ppmsmpms import ppmsmpmsparser

app = FastAPI()

@app.post('/rheedconverter')
def rheed_convert_route(data: dict = Body(...)):
    if 'file_name' not in data or 'output_file' not in data:
        raise HTTPException(status_code=400, detail='Missing parameters')

    file_name = data.get('file_name')
    output_file = data.get('output_file')

    if not os.path.isfile(file_name):
        raise HTTPException(status_code=400, detail='Local path is not a valid file')

    result = rheedconverter(file_name, output_file)
    if result is None:
        return {'message': 'Image converted successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    
@app.post('/brukerrawbackground')
def brukerbackground_convert_route(data: dict = Body(...)):
    if 'background_file' not in data or 'sample_file' not in data:
        raise HTTPException(status_code=400, detail='Missing parameters')

    background = data.get('background_file')
    sample = data.get('sample_file')

    if not os.path.isfile(background):
        raise HTTPException(status_code=400, detail='Local path is not a valid file')    
    if not os.path.isfile(sample):
        raise HTTPException(status_code=400, detail='Local path is not a valid file')

    result = brukerrawbackground(background, sample)
    if result is None:
        return {'message': 'background functions applied successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to apply background functions')
    
@app.post('/brukerrawconverter')
def brukerraw_convert_route(data: dict = Body(...)):
    if 'file_name' not in data or 'output_file' not in data:
        raise HTTPException(status_code=400, detail='Missing parameters')

    file_name = data.get('file_name')
    output_file = data.get('output_file')

    if not os.path.isfile(file_name):
        raise HTTPException(status_code=400, detail='Local path is not a valid file')

    result = brukerrawconverter(file_name, output_file)
    if result is None:
        return {'message': 'Bruker raw file converted successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    
@app.post('/mbeparser')
def MBE_parser_route(data: dict = Body(...)):
    if 'folder_name' not in data:
        raise HTTPException(status_code=400, detail='Missing parameters')

    folder = data.get('folder_name')

    if not os.path.isdir(folder):
        raise HTTPException(status_code=400, detail='Local path is not a valid file')

    result = mbeparser(folder)
    if result is None:
        return {'message': 'MBE data folder parsed successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to parse folder')
    
@app.post('/non4dstem')
def non4dstem_convert_route(data: dict = Body(...)):
    if 'file_folder' not in data or 'output_folder' not in data:
        raise HTTPException(status_code=400, detail='Missing parameters')

    file_folder = data.get('file_folder')
    output_folder = data.get('output_folder')

    if not os.path.isdir(file_folder):
        raise HTTPException(status_code=400, detail='Local path is not a valid file')

    result = non4dstem(file_folder,output_folder)
    if result is None:
        return {'message': 'Images converted successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to convert files')
    
@app.post('/ppmsmpms')
def ppmsmpms_convert_route(data: dict = Body(...)):
    if 'file_name' not in data or 'output_file' not in data:
        raise HTTPException(status_code=400, detail='Missing parameters')

    file_name = data.get('file_name')
    output_file = data.get('output_file')

    if not os.path.isfile(file_name):
        raise HTTPException(status_code=400, detail='Local path is not a valid file')

    result = ppmsmpmsparser(file_name, output_file)
    if result is None:
        return {'message': 'File converted successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    
@app.post('/stemarray4d')
def stem4d_convert_route(data: dict = Body(...)):
    if 'file_name' not in data or 'output_file' not in data:
        raise HTTPException(status_code=400, detail='Missing parameters')

    file_name = data.get('file_name')
    output_file = data.get('output_file')

    if not os.path.isfile(file_name):
        raise HTTPException(status_code=400, detail='Local path is not a valid file')

    result = stemarray4d(file_name, output_file)
    if result is None:
        return {'message': 'Image converted successfully'}
    else:
        raise HTTPException(status_code=500, detail=f'Failed to convert file')
    


#curl -X POST \
#  -H "Content-Type: application/json" \
#  -d '{"source": "box:/PARADIM_DOI_UPLOAD/10.34863_xxxx-xxxx/", "local_path": "srv/zpool01/paradim-data/paradim.jhu.edu/doi/xxxx-xxxx"}' \
#  http://localhost:5020/copy-fil