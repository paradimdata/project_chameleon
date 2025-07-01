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
We recommend using miniconda3 for the easiest installation and use. miniconda3 installers can be downloaded from `the website here <https://docs.conda.io/en/latest/miniconda.html>`_, and installation instructions can be found `here <https://conda.io/projects/conda/en/latest/user-guide/install/index.html>`_.

Installation and requirements
-----------------------------
1. Poetry
This package is managed using [Poetry](https://python-poetry.org/), which you should install globaly on your system. Once you have Poetry installed, you can install this package and its dependencies in any environment of your choice 

**Install Poetry with pipx** 
The easiest way to install Poetry is with pipx. If you do not already have pipx installed you can find the instructions [here](https://pipx.pypa.io/stable/installation/). Once pipx has been installed, restart your shell/terminal window. After Poetry has been installed, you can install poetry with::

    pipx install poetry

pipx should be installed on the base system, so make sure to deactivate any environments before running the command above.

2. Download github repository
Go to the `github repository<https://github.com/paradimdata/project_chameleon>` and either download or clone it somewhere it will be accessible. 

3. Create a new virtual environment
The example below assumes a conda environment but any other virtual environment manager should work as well. A fresh conda environment can be created using the commands below. Python version must be version 3.12.2 or newer::

	conda create -n project_chameleon python=3.12.9 -y 
	conda activate project_chameleon

4. Install Boost
Project Chameleon requires the most current version of boost in the virtual environment where it will be installed. If on a MacOS system, this can be done using brew::

	brew install boost

5. Poetry and Pip Install
Navigate to this repositories directory and install the `project_chameleon` package with its dependencies::

	cd project_chameleon
	poetry lock
	poetry install
	pip install .

After running these commands, Project Chameleon should be installed in your local environment. The easiest way to access the functions for basic use is through Jupyter notebooks. Below are directions on how access functions in a notebook. If any packages or dependencies cause issues or may be useful to you in another capacity, a more in depth list of dependencies can be found at the bottom of the page. 

Running in Jupyter Notebooks
----------------------------
For quick and easy use of Project Chameleon functions, Jupyter notebooks are recommended. To use, open a new or existing Jupyter notebook and create a new cell. In the new cell add these lines::

	from project_chameleon.rheedconverter import rheedconverter
	rheedconverter('example.img','example.png')

In this example, the function being accessed is `rheedconverter`. This function has two parameters: a .img file, and a .png file. The `rheedconverter` function is one of the easiest to use to test if the package is working. A test file can be found in the 'tests' folder of the repository. A full list of functions that can be accessed and use can be found in the Data Types section. Each function has a more in depth description of what it can do and how it should be used. 

**Dependencies and Futher Information**
Full listed of dependencies used by Project Chameleon
* matplolib.pyplot 
* numpy 
* ffmpeg 
* openpyxl 
* libhdf5
* hyperspy (Further information can be found [here](https://hyperspy.org/hyperspy-doc/current/user_guide/install.html))
* py4dstem (Further information can be found [here](https://github.com/py4dstem/py4DSTEM))
* xylib (install directions can be found [here](https://github.com/wojdyr/xylib))
* htmdec_formats (install directions can be found [here](https://github.com/htmdec/htmdec_formats))
If further instructions are needed for the xylib install, reference the file ["xylib_Install_Instructions_Windows"](https://github.com/paradimdata/project_chameleon/blob/main/xylib%20Install%20Instructions.txt) for a second set of instructions of how to download xylib on a windows machine, or reference the file ["xylib_Install_Instructions_MacOS"](https://github.com/paradimdata/project_chameleon/blob/main/xylib_Install_Instructions_MacOS.txt) for a second set of instructions of how to download xylib on a MacOS machine. 


