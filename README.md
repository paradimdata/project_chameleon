![Chameleon](ChameleonLogo.png)

Project Chameleon is a collection of Python scripts written to assist in data processing primarily for material science research. The scripts contain funtions that help convert, parse, and query different file formats that are commmonly found in material science research. This repository includes all scripts that are a part of Project Chameleon, an API that calls all functions in Project Chameleon, and a Dockerfile that installs and runs Project Chameleon and it's API.

## Working functions held in the repository:
- 4D STEM: documented and converted to series of 2D slices 
- NON 4D STEM: Data graphed and converted to png 
- XRD: Bruker RAW/UXD to CSV
- RHEED: 16 bpp .img images to TIF/PNG
- MBE: Data sorted and graphed
- PPMS/MPMS: Relevant lines extracted and saved
- ARPES: Extracts data from pxt files
- HS2 Files: 16bpp .hs2 images to PNG
- JEOL SEM: .EMSA to basic plot of data
- Bruker BRML: Bruker brml to TXT/CSV

For more information on the working files, see the official documentation at https://project-chameleon.readthedocs.io/en/latest/

## Functions still in progress
- EBSD

## Dependencies Install Instructions
Full listed of dependencies used by Project Chameleon
- matplolib.pyplot 
- numpy 
- hyperspy (Further information can be found [here](https://hyperspy.org/hyperspy-doc/current/user_guide/install.html))
- py4dstem (Further information can be found [here](https://github.com/py4dstem/py4DSTEM))
- xylib (install directions can be found [here](https://github.com/wojdyr/xylib))
If further instructions are needed for the xylib install, reference the file ["xylib_Install_Instructions_Windows"](https://github.com/paradimdata/project_chameleon/blob/main/xylib%20Install%20Instructions.txt) for a second set of instructions of how to download xylib on a windows machine, or reference the file ["xylib_Install_Instructions_MacOS"](https://github.com/paradimdata/project_chameleon/blob/main/xylib_Install_Instructions_MacOS.txt) for a second set of instructions of how to download xylib on a MacOS machine. 


## Package Install Instructions
This package is managed using [Poetry](https://python-poetry.org/), which you should install globaly on your system. Once you have Poetry installed you can install this package and its dependencies in any environment of your choice 

### Install Poetry with pipx 
The easiest way to install Poetry is with pipx. If you do not already have pipx installed you can find the instructions [here](https://pipx.pypa.io/stable/installation/). Once pipx has been installed, restart your shell/terminal window. After Poetry has been installed, you can install poetry with:

    $ pipx install poetry
pipx should be installed on the base system, so make sure to deactivate any environments before running the command above.

### Install the Package and its Dependencies
The example below assumes a conda environment but any other virtual environment manager should work as well. 

First, create a new conda environment:

	$ conda create -n project_chameleon python -y 
	$ conda activate project_chameleon
	
Navigate to this repositories directory and install the `project_chameleon` package with its dependencies:

	$ cd project_chameleon
	$ poetry install
	
It is also possible to skip the create and activate step, and poetry will automatically create one when you run `poetry install` as seen above. 


## API for Project Chameleon

This API provides a convenient and reasonably secure way to call any Project Chameleon functions on files from a local directory, base64 encoded files, or urls of files, that can be output to a local directory as well as returned as base64 enconded bytes, or a json containing base64 encoded bytes. It's built using FastAPI and supports secure validation of inputs.

### Running the API

- Save the provided code in a Python file (e.g., `api.py`).
- Run the API using uvicorn:

```bash
uvicorn api:app --host 0.0.0.0 --port 5020 --reload
```

### Security
The Project Chameleon API has built in security. This security is written for the Johns Hopkins system that it has been developed to run on, but could easily be adjusted to work for other systems. Each API call must include an access token, `access-token`, which can be generated at the [PARADIM website](https://data.paradim.org/poly/api/token). Tokens only last two minutes, so new tokens must be generated frequently. 

### Functionality

- Validates if provided source is a valid file type for the selected endpoint.
- Operates on selected files and saves or returns them in the select output type.
- Returns a success message if the files are operated on successfully.
- Raises HTTPException for error handling.

### Dependencies

- FastAPI
- uvicorn
- os
- urllib.parse
- shutil
- base64
- tempfile
- requests
- urllib.request
- zipfile
- json

### Endpoints

#### `POST /rheedconverter`
- By default, this endpoint takes files from a source directory and outputs them to a local path.
- JSON data with the `file_name` and `output_file` parameters must be provided in the request body.
- `file_name` can be used interchangeably with `file_bytes` or `file_url`
- Adding `output_type` allows for output to be either base64 encoded bytes or JSON. Options are `raw` which corresponds to bytes or `JSON` which corresponds to JSON.  
- Example usage:

```bash
curl -X POST http://localhost:5020/rheedconverter -H \
"Content-Type: application/json" -H \
"access-token: XXXXXX" \
-d '{"file_name":/app/tests/data/image1.img","output_file": "urltest_out.png"}'
```

#### `POST /brukerrawbackground`
- By default, this endpoint takes files from a source directory and outputs them to a local path.
- JSON data with the `background_file_name`, `sample_file_name`, and `output_file` parameters must be provided in the request body.
- `background_file_name` can be used interchangeably with `background_file_bytes` or `background_file_url`
- `sample_file_name` can be used interchangeably with `sample_file_bytes` or `sample_file_url`
- Adding `output_type` allows for output to be either base64 encoded bytes or JSON. Options are `raw` which corresponds to bytes or `JSON` which corresponds to JSON.  
- This function can take sample and background files as either .raw files or .csv files. This can be designated by `background_input_type` and `sample_input_type` with options `raw` and `csv`. The function defaults to .raw inputs. 
- Example usage:

```bash
curl -X POST http://localhost:5020/brukerrawbackground \
-H "Content-Type: application/json" \
-H "access-token: XXXXXX" \
-d '{"background_file_name":"/app/tests/data/background_test.csv","sample_file_name":"/app/tests/data/sample_test.csv""background_input_type":".csv","sample_input_type":".csv"}'
```
#### `POST /brukerrawconverter`
- By default, this endpoint takes files from a source directory and outputs them to a local path.
- JSON data with the `file_name` and `output_file` parameters must be provided in the request body.
- `file_name` can be used interchangeably with `file_bytes` or `file_url`
- Adding `output_type` allows for output to be either base64 encoded bytes or JSON. Options are `raw` which corresponds to bytes or `JSON` which corresponds to JSON.  
- This function can take both .raw and .uxd file types. This can be designated by `file_input_type` with options `raw` and `uxd`.
- Example usage:

```bash
curl -X POST http://localhost:5020/brukerrawconverter \
-H "Content-Type: application/json" \
-H "access-token: XXXXXX" \
-d '{"file_name":"/app/tests/data/test.raw","output_file":"brukerraw_out.txt","output_type":"JSON"}'
```
#### `POST /mbeparser`
- By default, this endpoint takes files from a source directory and outputs them to a local path.
- JSON data with the `folder_name` parameter must be provided in the request body.
- `folder_name` can be used interchangeably with `folder_bytes` or `folder_url`
- Adding `output_type` allows for output to be either base64 encoded bytes or JSON. Options are `raw` which corresponds to bytes or `JSON` which corresponds to JSON.  
- Example usage:

```bash
curl -X POST http://localhost:5020/mbeparser \
-H "Content-Type: application/json" \
-H "access-token: XXXXXX" \
-d '{"folder_name":"/app/tests/data/mbe_example"}'
```
#### `POST /non4dstem`
- By default, this endpoint takes files from a source directory and outputs them to a local path.
- JSON data with the `folder_name` and `output_folder` parameters must be provided in the request body.
- `folder_name` can be used interchangeably with `folder_bytes` or `folder_url`
- Adding `output_type` allows for output to be either base64 encoded bytes or JSON. Options are `raw` which corresponds to bytes or `JSON` which corresponds to JSON.  
- Example usage:

```bash
curl -X POST http://localhost:5020/non4dstem \
-H "Content-Type: application/json" \
-H "access-token: XXXXXX" \
-d '{"folder_name":"/app/tests/data/non4dstem_test","output_folder":"non4dstem_test_out"}'
```
#### `POST /ppmsmpms`
- By default, this endpoint takes files from a source directory and outputs them to a local path.
- JSON data with the `file_name` and `output_file` parameters must be provided in the request body.
- `file_name` can be used interchangeably with `file_bytes` or `file_url`
- Adding `output_type` allows for output to be either base64 encoded bytes or JSON. Options are `raw` which corresponds to bytes or `JSON` which corresponds to JSON.  
- Example usage:

```bash
curl -X POST http://localhost:5020/ppmsmpms \
-H "Content-Type: application/json" \
-H "access-token: XXXXXX" \
-d '{"file_name":"/app/tests/data/Magnetic.dat","output_file": "test_out.txt","output_type":"JSON"}'
```
#### `POST /stemarray4d`
- By default, this endpoint takes files from a source directory and outputs them to a local path.
- JSON data with the `file_name` and `output_file` parameters must be provided in the request body.
- `file_name` can be used interchangeably with `file_bytes` or `file_url`
- Adding `output_type` allows for output to be either base64 encoded bytes or JSON. Options are `raw` which corresponds to bytes or `JSON` which corresponds to JSON.  
- Example usage:

```bash
curl -X POST http://localhost:5020/stemarray4d \
-H "Content-Type: application/json" \
-H "access-token: vx8AePwF1dYj0eqZXiwxCQnef9nHukx2WDXana0De5g" \
-d '{"file_url":"/app/tests/data/stemarray4d_test.raw","output_file":"stem4d_raw"}'
```



This project was developed as part of the NSF platform, PARADIM (NSF award 2039380, the PARADIM MIP, and NSF award 2129051, the VariMat Cyberinfrastructure Pilot).

![PARADIM](PARADIM_LOGO.png)
