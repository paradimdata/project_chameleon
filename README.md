# project_chameleon
Repository for Project Chameleon conversion scripts

## Working conversion functions held in the repository:
- 4D STEM: documented and converted to series of 2D slices (16bpp TIFS)
- NON 4D STEM: Data graphed and converted to png
- XRD: Brker RAW/UXD to CSV
- RHEED: 16 bpp images to TIF/PNG
- MBE: Data sorted and graphed
- PPMS/MPMS: Relevant lines extracted and saved

## Conversions still in progress
- ARPES
- EPR
- JEOL SEM
- EBSD
- Bruker BRML

## Description of individual working functions

### 4D STEM 
**Function: stemarray4d('file_name','output_name')** 

This function takes a raw (.raw files) 4D STEM array as an input, and outputs two png files and a folder of png files: The mean of the dataset, the max of the data set, and 128 2D slices of the 4D array. The function will take of a file from the directory where the function is run, or a path to a file. Outputs will take the name 'output_name', which is just the name of the output file. 'output_name' may also include a file path as part of the name (example: /root/folder/output_name). 'output_name' should not include any file type designation(.txt,.png.jpeg) as this is added in the code. This function relies on the library py4DSTEM functions to load and read the 4D STEM files. This function does not return anything.

### NON 4D STEM
**Function: non4dstem('foldername','outputfolder')**

This function takes a folder of non-4D STEM images (.dm4, .ser, .emd) files as an input, and outputs a folder called 'outputs' that contains .png images for each of the inputs. The folder containing the input files may be in the same directory where the function is run, or 'foldername' can be a path to a folder. The folder 'outputfolder' will be created in the folder where the function is run if only a name is given. 'outputfolder' may also be a path. Files must be put into a folder even if there is just one file. This function relies on the library hypserspy to load and read the data. This function does not return anything. 

### XRD BRUKER RAW/UXD
**Function: brukerrawconverter('input_filename','output_filename)**

This function takes a raw Bruker file (.raw, .uxd) as an input(input_filename), and outputs a text file titled 'output_filename.txt' containing metadata and all data from the raw file. This function will by default look for the input file in the directory where the function is run unless 'input_filename' includes a path. The output file will be created in the folder where the function is run unless 'output_filename' includes a path. 'output_filename' should include the file type designation '.txt' at the end. This function relies on the library xylib. This function does not return anything.

### RHEED
**Function: rheedconverter('filename', 'outputname')**

This function taks a 16bpp rheed image file(.img) as an input, and outputs a 8bpp image file(.png). This function will look for the input file in the directory where the function is run by default, unless 'filename' contains a path. The ouput file will be created in the folder where the function is run with the name 'outputname'.png unless 'outputname' contains a path. 'outputname' should include the file type designation '.png' at the end. This function does not return anything.

### MBE
**Function: mbeparser('foldername')**

This function takes a folder as an input. This folder should contain all text file(.txt) outputs from a specific MBE run. The input folder may be in the same folder where the function is run, or 'foldername' may be a file path to a folder. Within the input folder, the function will sort all text files into two sub directories: useful, and useless. Sorting is accomplished using keywords from file names. After sorting is complete, the user may choose what kind of action they want to take: graph and show a file, graph, show, and save a file, check setpoints, or exit. If graph and show is chosen, all graphable files from the useful folder will be printed and the user can choose one to graph which will then be displayed. If graph, show, and save a file is chosen, all graphable files from the useful folder will be printed and the user can pick one which will then be graphed and also saved in the useful folder. If check setpoints is chosen, all the setpoint files will be displayed and the user can choose a setpoint to check the value of. Users will be continuously given these option until they pick the exit option. 

### PPMS/MPMS
**Function: ppmsmpmsparser('inputfile', 'outputfile')** 

This function takes a .dat file as an input. This .dat file should be one of four types so that the function can extract the data properly. The four types are 4 probe resistivity, heat capacity, thermal transport, and magnetic susceptibility. The input file may be a file or a path to a file in a different folder. When the function is run the user may choose what kind of file was input so the correct columns can be extracted. The relevant columns in the .dat input file are read by the function and written into a .txt file called 'outputfile'.  'inputfile' and 'outputfile' should both contain full file names and file extensions (.dat for input, .txt for output). 

## Dependencies Install Instructions
Full listed of dependencies used by Project Chameleon
- matplolib.pyplot 
- numpy 
- hyperspy (Further information can be found [here](https://hyperspy.org/hyperspy-doc/current/user_guide/install.html))
- py4dstem (Further information can be found [here](https://github.com/py4dstem/py4DSTEM))
- xylib (install directions can be found [here](https://github.com/wojdyr/xylib))
If further instructions are needed for the xylib install, reference the file ["xylib_Install_Instructions"](https://github.com/paradimdata/project_chameleon/blob/main/xylib%20Install%20Instructions.txt) for a second set of instructions of how to download xylib on a windows machine. 


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
