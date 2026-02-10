=================
Chameleon Web API
=================

Project Chameleon contains a web API that allows for functions to be accessed as web API endpoints. Every function in Project Chameleon has a corresponding endpoint which can be found in `the API file <https://github.com/paradimdata/project_chameleon/blob/main/api.py>`_. 

Running the API
---------------
The Project Chameleon has prebuilt impelementations for both :doc:`Docker <docker>` and :doc:`Girder <girder>`. The API can also be started locally using Uvicorn. In a virtual environment with Uvicorn and Project Chameleon dependencies installed, the API can be started using this command:

.. code-block:: bash

      uvicorn api:app --reload 

This will run the API locally at http://127.0.0.1:8000. Below is a list of endpoints that can be appended to the local url to actually access a function:

    - /arpes_workbook
    - /brukerbrmlconverter
    - /brukerrawbackground
    - /brukerrawconverter
    - /hs2converter
    - /jeol_sem_converter
    - /mbeparser
    - /non4dstem_folder
    - /non4dstem_file
    - /ppmsmpms
    - /rheedconverter
    - /rheed_video_converter
    - /stemarray4d

Calls to the endpoint require three main fields of information: content type, access token, and data. For all endpoints the content type will always be "application/json". For local functionality the access token can be a random string of alphanumeric characters. If desired, the access token functionality can be removed entirely without adversely affecting any data processed by the API. The data field will contain all information that would go in a regular function call. The information must be paired with the appropriate function variable. The function variables that hold inputs and outputs follow a specific convention. Below are all possible input and output variables:

    - input_file
    - input_folder
    - input_url
    - input_bytes
    - folder_bytes
    - output_file
    - output_folder
    - secondary_file
    - secondary_bytes
    - secondary_url

There are three categories of variable: primary input types (start with input or folder), secondary input types (start with secondary), and output types(start with output). Only one of each category should be used at any time. The secondary category is only necessary for functions like "brukerrawbackground" that take two file inputs. An example call can be seen below:

.. code-block:: bash

    curl -X POST http://localhost:5020/rheedconverter 
        -H "Content-Type: application/json" 
        -H "access-token: xxxxxx" 
        -d '{"input_url":"https://github.com/paradimdata/project_chameleon/raw/main/tests/data/rheed/test.img","output_file": "urltest_out.png"}'

In this example, the API has been configured to run at "localhost:5020" and the rheedconverter endpoint is being accessed. As mentioned, Content type is "application/json" and the access token can be any string. Looking at the data field, a file url is being given, so the input variable chosen is "input_url". The function rheedconverter only gives a single file output so the variable "output_file" is chosen for the output category. 
