import hyperspy.api as hs
from glob import glob
import matplotlib.pyplot as plt
import os
import sys
import argparse

def non4dstem(data_folder,outputs_folder):
    """
    'non4dstem' is a function that takes an input folder containing 2D and 3D STEM images and converts those files into plots that are saved to an output folder. This function was tested on .dm4 files, .ser files, and .emd files, but can handle any filetypes that can be parserd by the hyperspy 'load' function. 
 
    args: This function has two inputs: 'data_folder' and 'outputs_folder'. 'data_folder' should be a folder holding all non 4D files that are being processed. 'outputs_folder' is a string which will be the name out the folder that holds all the processed images.

    return: this function does not return anything. It saves converted files as .png images in the folder labeled 'output_folder'.

    exceptions: will throw an exception if the 'data_folder' is not a folder.
    """
    count = 0

    #Create outputs folder
    os.makedirs(outputs_folder)
    
    #Make sure input is a folder
    if os.path.isdir(data_folder) is False:
        raise ValueError("ERROR: bad input. Expected folder")
    
    #Read in files from data folder
    for file in glob(data_folder + "/*"):
        data = hs.load(file)

    #For each file that gets read in, plot and save as a figure
    print(data)
    for obj in data:
        count = count + 1
        obj.plot()
        plt.savefig(f"{outputs_folder}/{os.path.splitext(os.path.split(file)[-1])[0]}_{obj.metadata.Signal.signal_type}{count}.png")
        plt.close()
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input folder")
    parser.add_argument("output", help="the output folder")
    args = parser.parse_args()
    non4dstem(args.input, args.output)
