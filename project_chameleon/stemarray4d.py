import py4DSTEM
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import argparse
from pathlib import Path

def stemarray4d(file_name,output_name):
    """
    ``stemarray4d()`` is a function designed to take raw 4D STEM files and process them into more disgestable images. 

    :args: This function has two inputs: ``file_name`` and ``output_name``. ``file_name`` should be a 4D STEM .raw file. ``output_name`` should be a string which will be the name of all outputs combined with the designator of the specific output.

    :return: does not return anything. There are three primary outputs: a mean image, a max image, and a folder containing the decomposed 2D images of the 4D .raw image.

    :exceptions: will throw an exception if the input is not a file.
    """

    #Check if input is a file
    if os.path.isfile(file_name) is False:
        raise ValueError("ERROR: bad input. Expected file")
    if not file_name.endswith('.raw'):
        raise ValueError("ERROR: bad input. Function takes a .raw 4D stem file")
    if os.path.getsize(file_name) < 10:
        raise ValueError("ERROR: This size of file cannot be handled by this function. File too small.")
    if '.' in output_name:
        raise ValueError("ERROR: Output Name should not contain '.'")
    
    #Import the file as 4D STEM array
    dataset = py4DSTEM.import_file(file_name)

    #Calculate mean and max of the dataset
    meanDP = dataset.get_dp_mean()
    maxDP = dataset.get_dp_max()

    #Save an individual 2D slice from the 4D array
    #vBF = dataset.data[:, :, 64, 64]

    #Save mean as a png
    plt.imsave(
    fname=Path(str(output_name) + "_mean_DP.png"),
    arr=meanDP.data,
    vmin=np.percentile(meanDP.data, 1),
    vmax=np.percentile(meanDP.data, 99),
    cmap="gray",
    )

    #Save max as a png
    plt.imsave(
    fname=Path(str(output_name) + "_max_DP.png"),
    arr=maxDP.data,
    vmin=np.percentile(meanDP.data, 1),
    vmax=np.percentile(meanDP.data, 99),
    cmap="gray",
    )

    #Save individual 2D slice as a png
    count = 0
    upper_limit = len(dataset.data[2])
    while 0 <= count < upper_limit:
        vBF = dataset.data[:,:,count,count]
        plt.imsave(
        fname=Path(str(output_name) + str(count) + "_vBF.png"),
        arr=dataset.data[:,:,count,count],
        vmin=np.percentile(vBF, 1),
        vmax=np.percentile(vBF, 99),
        cmap="gray",
        )
        count += 1

    #Make a folder to holder all the images from the 4d array
    output_folder = Path(str(output_name) + 'array')
    os.makedirs(output_folder)

    #Sort all the slices into the directory
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith('.png'):
            filepath = os.path.join(current_directory, filename)
        else:
            continue
            
        if (str(output_name) in filename) and ('vBF' in filename): 
            shutil.move(filepath, os.path.join(output_folder, filename))
        elif (str(output_name) in filename) and ('_mean_DP' in filename):
            shutil.move(filepath, os.path.join(output_folder, filename))
        elif (str(output_name) in filename) and ('_max_DP' in filename):
            shutil.move(filepath, os.path.join(output_folder, filename))
        else:  
            continue

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    stemarray4d(args.input, args.output)