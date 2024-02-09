# project_chameleon
Repository for Project Chameleon conversion scripts

## Working conversion functions held in the repository:
- 4D STEM: documented and converted to series of 2D slices (16bpp TIFS)
- NON 4D STEM: Data graphed and converted to png
- XRD: Brker RAW/UXD to CSV
- RHEED: 16 bpp images to TIF/PNG
- MBE: Data sorted and graphed

## Conversions still in progress
- ARPES
- EPR
- JEOL SEM
- EBSD
- PPMS/MPMS

## Description of individual working functions

### 4D STEM 
**Function: stemarray4d('filename')** 

This function takes a raw (.raw files) 4D STEM array as an input, and outputs three png files: The mean of the dataset, the max of the data set, and one specific slice from the 4D array. The function will take files from the directory where the function is run and the outputs will but output in the directory where the function is run. This function relies on the library py4DSTEM functions to load and read the 4D STEM files. This function does not return anything.

### NON 4D STEM
**Function: non4dstem('foldername')**

This function takes a folder of non-4D STEM images (.dm4, .ser, .emd) files as an input, and outputs a folder called 'outputs' that contains .png images for each of the inputs. The folder containing the input files must be in the same directory where the function is run, and the folder 'ouputs' will be created in the folder where the function is run. Files must be put into a folder even if there is just one file. This function relies on the library hypserspy to load and read the data. This function does not return anything. 

### XRD BRUKER RAW/UXD
**Function: brukerrawconverter('input_filename','output_filename)**

This function takes a raw Bruker file (.raw, .uxd) as an input(input_filename), and outputs a text file titled 'output_filename.txt' containing metadata and all data from the raw file. This function will look for the input file in the directory where the function is run, and the output file will be created in the folder where the function is run. This function relies on the library xylib. This function does not return anything.

### RHEED
**Function: rheedconverter('filename')**

This function taks a 16bpp rheed image file(.img) as an input, and outputs a 8bpp image file(.png). This function will look for the input file in the directory where the function is run, and the ouput file will be created in the folder where the function is run. This function does not return anything.

### MBE
**Function: mbeparser('foldername')**

This function takes a folder as an input. This folder should contain all text file(.txt) outputs from a specific MBE run. The input folder should be in the same folder where the function is run. Within the input folder, the function will sort all text files into two sub directories: useful, and useless. Sorting is accomplished using keywords from file names. After sorting is complete, the useful files will be listed and the user may choose if they would like to graph a specific file. If users would like to graph a file, they must input the full file name and then this graph of the file will be displayed. This function does not return anything. 


## Dependencies
Dependency install instructions written for a conda environment
- os (pip install os)
- matplolib.pyplot (pip install matplotlib.pyplot)
- glob (pip install glob)
- numpy (pip install numpy)
- pathlib (pip install pathlib)
- shutil (pip install shutil)
- argparse (pip install argparse)
- sys (pip install sys)
- hyperspy (install directions can be found [here](https://hyperspy.org/hyperspy-doc/current/user_guide/install.html))
- py4dstem (install directions can be found [here](https://github.com/py4dstem/py4DSTEM))
- xylib (install directions can be found [here](https://github.com/wojdyr/xylib))
If further instructions are needed for the xylib install, reference the file "xylib Install Instructions" for a second set of instructions of how to download xylib on a windows machine. 


