=============================
Installing Project Chameleon
=============================

Docker Image
------------
The quickest way to deploy OpenMSIStream programs is to use the public `Docker image<https://github.com/paradimdata/project_chameleon/blob/main/Dockerfile>`. 

The image is built off of the python:3.12-slim (Debian Linux) base image, and contains a complete install of Project Chameleon. Running the Docker image as-is will drop you into a bash terminal as the user (who has sudo privileges) in their home area. 

If you want to install Project Chameleon on your own system instead of running a Docker container, though, we recommend using a minimal installation of the conda open source package and environment management system. The instructions below start with installation of conda and outline all the necessary steps to run OpenMSIStream programs.

Quick start with miniconda3
---------------------------
We recommend using miniconda3 for the lightest installation. miniconda3 installers can be downloaded from `the website here <https://docs.conda.io/en/latest/miniconda.html>`_, and installation instructions can be found `here <https://conda.io/projects/conda/en/latest/user-guide/install/index.html>`_.

Installation and requirements
-----------------------------
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

## Dependencies and Futher Information
Full listed of dependencies used by Project Chameleon
- matplolib.pyplot 
- numpy 
- ffmpeg 
- openpyxl 
- libhdf5
- hyperspy (Further information can be found [here](https://hyperspy.org/hyperspy-doc/current/user_guide/install.html))
- py4dstem (Further information can be found [here](https://github.com/py4dstem/py4DSTEM))
- xylib (install directions can be found [here](https://github.com/wojdyr/xylib))
- htmdec_formats (install directions can be found [here](https://github.com/htmdec/htmdec_formats))
If further instructions are needed for the xylib install, reference the file ["xylib_Install_Instructions_Windows"](https://github.com/paradimdata/project_chameleon/blob/main/xylib%20Install%20Instructions.txt) for a second set of instructions of how to download xylib on a windows machine, or reference the file ["xylib_Install_Instructions_MacOS"](https://github.com/paradimdata/project_chameleon/blob/main/xylib_Install_Instructions_MacOS.txt) for a second set of instructions of how to download xylib on a MacOS machine. 


Running in Jupyter Notebooks
----------------------------

