import hyperspy.api as hs
from glob import glob
import matplotlib.pyplot as plt
import os

def non4dstem(data_folder):
    """
    A function to take 2D and 3D STEM file formats and turn them into 2D readable .png image files. 

    args: data_folder is the only input and it holds the 2D and 3D files that will be converted into .png images
    return: this function does not return anything. Instead it just saves converted files as .png images
    exceptions: will throw an exception if the input file is not a folder
    """
    #Create outputs folder
    os.makedirs('outputs')
    
    #Make sure input is a folder
    if os.path.isdir(data_folder) is False:
        raise ValueError("ERROR: bad input. Expected folder")
    
    #Read in files from data folder
    for file in glob(data_folder + "/*"):
        data = hs.load(file)

    #For each file that gets read in, plot and save as a figure
    for obj in data:
        obj.plot()
        plt.savefig(f"outputs/{os.path.splitext(os.path.split(file)[-1])[0]}_{obj.metadata.Signal.signal_type}.png")
    