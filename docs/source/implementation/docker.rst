=======================
Chameleon Docker Image
=======================

Chameleon provides a prebuilt Dockerfile that can be used to run the package. This Dockerfile is based on a Python 3.12 slim base image. After building and running the Docker image, Project Chameleon is best accessed by running the Chameleon API. This method is useful if a user wants to set up Chameleon endpoints so they can be accessed via a URL or a broader network interface.

Running Chameleon in Docker 
---------------------------

The first step to running Project Chameleon in Docker is to ensure you have Docker installed. If Docker is not installed, instructions can be found `here <https://pipx.pypa.io/stable/installation/>`_. Once Docker is installed, navigate to the directory you downloaded or cloned from the GitHub repository. The Dockerfile should also work if it is downloaded independently from the package.

1. **Build the Image**

Once in the same directory as the Dockerfile, build the image using the command below:

.. code-block:: shell

    docker build -t test . \
      --build-arg GIT_USERNAME=username \
      --build-arg GIT_ACCESS_TOKEN=githubaccesstoken \
      --no-cache

In this example, Docker builds an image called `test` from the Dockerfile in the current directory. The name of the image is specified by the ``-t`` flag, and the current directory is represented by ``.``. Two build arguments are supplied: a GitHub username and a GitHub personal access token. These are used to clone the Chameleon repository. The ``--no-cache`` flag ensures that no cached layers are reused when building the image.

2. **Run the Docker Container**

After the Docker image is built, it needs to be run as a container. Here’s an example command:

.. code-block:: shell

    docker run -p 5020:5020 --rm -it test:latest /bin/bash

This command runs the latest version of the `test` image with a Bash shell. It maps host port 5020 to container port 5020, specified by ``-p 5020:5020``. These ports can be adjusted, but the Dockerfile and Uvicorn command must be updated accordingly. The ``--rm`` flag ensures Docker deletes the container after it exits. This command places the user in the container at `/app`. From there, the API must be started with Uvicorn.

3. **Running Uvicorn**

Once inside the container, start Uvicorn with the following command:

.. code-block:: shell

    uvicorn api:app --host 0.0.0.0 --port 5020 --reload

This starts the app defined in `api.py` (denoted by ``api:app``). The ``--host 0.0.0.0`` flag makes it listen on all available interfaces. The port is set to 5020. As mentioned earlier, if this is changed, it must also be reflected in the Dockerfile and run command.

After running Uvicorn, Chameleon should be accessible locally at ``http://localhost:5020``. Note that this base URL will not return any data by itself—an API endpoint must be appended. For example: ``http://localhost:5020/rheedconverter``.

Available API endpoints include:

 - /rheedconverter 
 - /rheed_video_converter 
 - /brukerrawconverter 
 - /mbeparser 
 - /non4dstem_folder 
 - /non4dstem_file
 - /ppms 
 - /stemarray4d 
 - /arpes_workbook 
 - /hs2converter 
 - /brukerrawbackground 
 - /jeol_sem_converter 
 - /brukerbrmlconverter 

Note: Not all Chameleon functions are currently available through the API and therefore may not be accessible through this Docker implementation.
