import py4DSTEM
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import shutil
import argparse

def stemarray4d(file_name,output_name):
    """
    A function to take 4D STEM files and turn them into a series of 2D readable image files

    args: primarily takes .raw files that contain 4D arrays 
    return: does not return anything. Instead it saves files as .png images
    exceptions: will throw an exception if the input is not a file
    """

    #Check if input is a file
    if os.path.isfile(file_name) is False:
        raise ValueError("ERROR: bad input. Expected file")
    
    #Import the file as 4D STEM array
    dataset = py4DSTEM.import_file(file_name)

    #Calculate mean and max of the dataset
    meanDP = dataset.get_dp_mean()
    maxDP = dataset.get_dp_max()

    #Save an individual 2D slice from the 4D array
    #vBF = dataset.data[:, :, 64, 64]

    #Save mean as a png
    plt.imsave(
    fname=output_name + "_mean_DP.png",
    arr=meanDP.data,
    vmin=np.percentile(meanDP.data, 1),
    vmax=np.percentile(meanDP.data, 99),
    cmap="gray",
    )

    #Save max as a png
    plt.imsave(
    fname=output_name + "_max_DP.png",
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
        fname=output_name + str(count) + "_vBF.png",
        arr=dataset.data[:,:,count,count],
        vmin=np.percentile(vBF, 1),
        vmax=np.percentile(vBF, 99),
        cmap="gray",
        )
        count += 1

    #Make a folder to holder all the images from the 4d array
    output_folder = output_name + 'array'
    os.makedirs(output_folder)

    #Sort all the slices into the directory
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith('.png'):
            filepath = os.path.join(current_directory, filename)
        else:
            continue
            
        if (output_name in filename) and ('vBF' in filename): 
            shutil.move(filepath, os.path.join(output_folder, filename))
        else:  
            continue

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    stemarray4d(args.input, args.output)