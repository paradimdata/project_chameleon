import hyperspy.api as hs
from glob import glob
import matplotlib.pyplot as plt
import os
import sys
import argparse

def non4dstem(data_folder,outputs_folder):
    """
    A function to take 2D and 3D STEM file formats and turn them into 2D readable .png image files. 

    args: data_folder is the only input and it holds the 2D and 3D files that will be converted into .png images
    return: this function does not return anything. Instead it just saves converted files as .png images
    exceptions: will throw an exception if the input file is not a folder
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
