from fastapi import FastAPI, HTTPException, Body, Header, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
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
from api_helpers import *
from project_chameleon.rheedconverter import rheedconverter
from project_chameleon.brukerrawbackground import brukerrawbackground
from project_chameleon.brukerrawconverter import brukerrawconverter
from project_chameleon.mbeparser import mbeparser
from project_chameleon.non4dstem import non4dstem
from project_chameleon.stemarray4d import stemarray4d
from project_chameleon.ppmsmpms import ppmsmpmsparser
from project_chameleon.arpes import arpes_folder_workbook
from project_chameleon.hs2converter import hs2converter
from project_chameleon.rheed_video_converter import rheed_video_converter
from project_chameleon.jeol_sem_converter import sem_base_plot
from project_chameleon.brml_converter import brml_converter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/rheedconverter')
async def rheed_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er

    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.img', '.png')
    try:
        with open(input_file,"rb") as f:
            file_data = f.read(100)
            print(file_data)
        rheedconverter(input_file, output_file)
        return common_file_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "rheedconverter"')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)

@app.post('/rheed_video_converter')
def rheed_vide_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er

    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.imm', '.avi')
    try:
        rheed_video_converter(input_file, output_file)
        return common_file_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "rheed_video_converter"')
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
    cps = None
    if 'cps' in data:
        if data['cps']:
            cps = True
        else:
            cps = False
    try:
        brukerrawconverter(input_file, output_file, cps)
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
    
    if 'input_ext' in data:
        input_ext = str(data['input_ext'])
    
    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, input_ext, '.png')

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
    input_file,output_file = common_file_handler_parse_request(request, data, '.dat', '.csv') 

    try:
        ppmsmpmsparser(input_file, output_file)
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
    input_file,output_file = common_file_handler_parse_request(request, data, '.raw', '') # Output has no file extension, all files are in a folder
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

@app.post('/jeol_sem_converter')
async def jeol_sem_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er
    
    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.EMSA', '.png')

    try:
        sem_base_plot(input_file, output_file)
        return common_file_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "sem_base_plot"')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)

@app.post('/brukerbrmlconverter')
def brukerbrml_convert_route(request: Request, data: dict = Body(...), access_token: str = Header(default=''), x_auth_access_token: str = Header(default='')):
    access_token = common_handler_access_token(request, data, access_token, x_auth_access_token)

    er = common_handler_early_response(request, data)
    if not (er is None):
        return er

    common_handler_method_auth_check(request, data, access_token)
    input_file,output_file = common_file_handler_parse_request(request, data, '.brml', '.csv')
    try:
        brml_converter(input_file, output_file)
        return common_file_handler_prepare_output(request, data, output_file)
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Failed to convert file: an error occurred running the function "brukerrawconverter"')
    finally:
        common_handler_cleanup_request(request, data, input_file, None)