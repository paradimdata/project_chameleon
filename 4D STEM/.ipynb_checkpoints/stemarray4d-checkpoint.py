import py4DSTEM
import matplotlib.pyplot as plt
import numpy as np
import os

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
    vBF = dataset.data[:, :, 64, 64]

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
    plt.imsave(
    fname=output_name + "_vBF.png",
    arr=vBF,
    vmin=np.percentile(vBF, 1),
    vmax=np.percentile(vBF, 99),
    cmap="gray",
    )

if __name__ == '__main__':
    stemarray4d()