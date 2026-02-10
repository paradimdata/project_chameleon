=============================
Installing Project Chameleon
=============================

Quick Start with Miniconda3
---------------------------
We recommend using Miniconda3 for the simplest installation. Miniconda3 installers can be downloaded from `the Miniconda website <https://docs.conda.io/en/latest/miniconda.html>`_, and installation instructions are available `here <https://conda.io/projects/conda/en/latest/user-guide/install/index.html>`_. This method should be the easiest to get running for most users as it only requires a conda environment. If you are looking for a containerized version of Project Chameleon, instructions for installing and starting the Docker Image version can be found below. 

Installation and Requirements
-----------------------------

1. **Download the GitHub Repository**

   Clone or download the `GitHub repository <https://github.com/paradimdata/project_chameleon>`_ somewhere accessible on your system. This can either be done by downloading a zip directly from the Github webpage, or through Github desktop. Both of these methods should function the same. 

2. **Create a New Virtual Environment and Install Dependencies**

   While any virtual environment manager should work, the example below uses Conda. The Python version must be 3.12.2 or newer. The commands below will both create a new virtual environment and install dependencies:

   .. code-block:: bash

      conda env create -f environment.yml
      conda activate project-chameleon

   Note that the environment.yml file will automatically name the new envrionment "project-chameleon". To change this, edit the name in the environment.yml file and adjust the conda commands accordingly. 

3. **ARPES Dependencies Installation (Optional)**
   If you do not plan on using the ARPES function in Project Chameleon this step in installation is not necessary. The ARPES functions require the installation of one additional package called HTMDEC Formats. To install this package, the `GitHub repository <https://github.com/htmdec/htmdec_formats>`_ should be cloned or downloaded. Then, within the newly created conda environment, enter the htmdec_formats repository and run:

   .. code-block:: bash

      pip install -e .

   After this package is installed, ARPES functions should work normally.

In case of trouble with installation, more detailed instructions on installation for some packages can be found on the.:doc:`instructions and specifications <instructions_and_specifications>` page. This page also details some processes and expected structures of Project Chameleon.

Running in Jupyter Notebooks
----------------------------
Jupyter notebooks are recommended for quick access to Project Chameleon functions. 

To use:

1. Install Jupyter Notebooks in your conda environment

   .. code-block:: python

      pip install notebook

2. Open a Jupyter notebook.

   .. code-block:: python

      jupyter notebook

3. In a new cell, add:

   .. code-block:: python

       from project_chameleon.rheedconverter import rheedconverter
       rheedconverter('example.img', 'example.png')

This example uses the `rheedconverter` function, which takes two parameters: a `.img` input file and a `.png` ouput file. It is one of the simplest functions that can be used to test that the package is working.

Test files can be found in the `tests/data/rheed` folder of the repository. The files that can are included in the package and can be used for testing are `Image107.img`, `rheed_test_image.img`, and `test.img`. When the function is run, an ouput should be created with the name given to the output file. In the example above, the ouput would be named `example.png`. A full list of functions and usage examples is provided in the **Data Types** section.

Docker Image
------------
Another way to deploy Project Chameleon is to use the public `Docker image <https://github.com/paradimdata/project_chameleon/blob/main/Dockerfile>`_. This method does require that the user is familiar with Docker, but also does all of the installing of packages for you. 

The image is built on the `python:3.12-slim` (Debian Linux) base image and contains a complete installation of Project Chameleon. Running the Docker image as-is will drop you into a bash terminal as the user (who has sudo privileges) in their home directory. More information on the Docker image can be found `here <https://project-chameleon.readthedocs.io/en/latest/implementation/docker.htmle>`_.

If you prefer to install Project Chameleon directly on your system instead of using a Docker container, we recommend starting with a minimal installation of Conda, the open source package and environment management system. 

Dependencies and Further Information
------------------------------------
Full list of dependencies used by Project Chameleon:

- `matplotlib.pyplot`
- `numpy`
- `ffmpeg`
- `openpyxl`
- `libhdf5`
- `hyperspy` (See installation guide: https://hyperspy.org/hyperspy-doc/current/user_guide/install.html)
- `py4DSTEM` (https://github.com/py4dstem/py4DSTEM)
- `xylib` (https://github.com/wojdyr/xylib)
- `htmdec_formats` (https://github.com/htmdec/htmdec_formats)

**Note on xylib Installation:**

If you need help installing xylib, see the following files in the repository:

- [`xylib_Install_Instructions_Windows.txt <https://github.com/paradimdata/project_chameleon/blob/main/Instructions%20and%20Specifications/xylib_Install_Instructions_Windows.txt>`_]
- [`xylib_Install_Instructions_MacOS.txt <https://github.com/paradimdata/project_chameleon/blob/main/Instructions%20and%20Specifications/xylib_Install_Instructions_MacOS.txt>`_]
- [`XYlib_ARM_Install_Instructions_v1.rxt <https://github.com/paradimdata/project_chameleon/blob/main/Instructions%20and%20Specifications/XYlib_ARM_Install_Instructions_v1.rtf>`_]

These provide additional platform-specific installation instructions.
