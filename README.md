# project_chameleon
Repository for Project Chameleon conversion scripts

## Working conversion functions held in the repository:
- 4D STEM: documented and converted to series of 2D slices 
- NON 4D STEM: Data graphed and converted to png (Experiencing difficulties)
- XRD: Bruker RAW/UXD to CSV
- RHEED: 16 bpp images to TIF/PNG
- MBE: Data sorted and graphed
- PPMS/MPMS: Relevant lines extracted and saved

## Conversions still in progress
- ARPES
- JEOL SEM
- EBSD
- Bruker BRML

## Description of individual working functions

### 4D STEM 
To run the function stemarray4d in the command line, run:

	stemarray4d([inputfile],[outputfile])

Where:

* [inputfile] is a string or a path to a 4D STEM array .raw file, which is a 4D array.
* [outputfile] is a string or a path including a name which is the name of the output folder(ex. /root/folder/outputname). The output folder holds 128 2D slices of the 4D array as well as the mean and the max of the set.
* This command uses the py4DSTEM library



### NON 4D STEM
To run the function non4dstem in the command line, run:

	non4dstem([inputfile],[outputfile])

Where:

* [inputfile] is a string or a path to a folder containing non-4D STEM images (.dm4, .ser, .emd). 
* [outputfile] is a string or a path including a name which is the name of the output folder(ex. /root/folder/outputname). The output folder holds .png images for each of the input images.
* This command uses the hyperspy library

### XRD BRUKER RAW/UXD
There are two functions for Bruker RAW files: brukerrawconverter and brukerrawbackground

To run the function brukerrawconverter in the command line, run:

	brukerraw([inputfile],[outputfile])

Where:

* [inputfile] is a string or a path to a XRD Bruker file (.raw, .uxd) file. 
* [outputfile] is a string or a path including a name which is the name of the output file(ex. /root/folder/filename). The output file holds the metadata and data from the input file. Output file is just a regular text file
* This command uses the xylib library

To run the function brukerrawbackground in the command line, run:

	brukerrawbackground([background_input],[sample_input],[output_name])

Where:

* [background_input] is a string or a path to either a .csv file or a .raw file containing the background of the sample.
* [sample_input] is a string or a path to either a .csv file or a .raw file containing the sample data.
* [output_name] is a string which will be the beginning of the name of all the output files.
* This file outputs four things: A plot of the raw data, a plot of the background adjusted data, a plot of the background subtracted data, and a .csv of the background subtracted data.
* This command uses the brukerrawconverter command


### RHEED
To run the function rheedconverter in the command line, run:

	rheed([inputfile],[outputfile])

Where:

* [inputfile] is a string or a path to a 16bpp rheed image file (.img).
* [outputfile] is a string or a path including a name which is the name of the output file(ex. /root/folder/filename). The output file is a 8bpp .png file.

### MBE
To run the function mbeparser in the command line, run:

	mbeparser([inputfolder])

Where:

* [inputfile] is a string or a path to a folder holding text file outputs from MBE measurements.
* There is no output file or folder. All textfiles are sorted within the given folder and all outputs are saved within that folder.

### PPMSMPMS
To run the function ppmsmpmsparser in the command line, run:

	ppmsmpms([inputfile],[outputfile])

Where:

* [inputfile] is a string or a path to a ppms/mpms .dat file.
* [outputfile] is a string or a path including a name which is the name of the output file(ex. /root/folder/filename). The output file is a .txt file that holds relevant data columns from the input file. The "relevant" columns are chosen by user input.

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
