import py4DSTEM
import matplotlib.pyplot as plt
import numpy as np
import os

def 4dstemarray(file_name):
    
    #Import the file as 4D STEM array
    dataset = py4DSTEM.import_file(file_name)

    #Calculate mean and max of the dataset
    meanDP = dataset.get_dp_mean()
    maxDP = dataset.get_dp_max()

    #Save an individual 2D slice from the 4D array
    vBF = dataset.data[:, :, 64, 64]

    #Save mean as a png
    plt.imsave(
    fname=os.path.splitext(os.path.split(filepath)[1])[0] + "_mean_DP.png",
    arr=meanDP.data,
    vmin=np.percentile(meanDP.data, 1),
    vmax=np.percentile(meanDP.data, 99),
    cmap="gray",
    )

    #Save max as a png
    plt.imsave(
    fname=os.path.splitext(os.path.split(filepath)[1])[0] + "_max_DP.png",
    arr=maxDP.data,
    vmin=np.percentile(meanDP.data, 1),
    vmax=np.percentile(meanDP.data, 99),
    cmap="gray",
    )

    #Save individual 2D slice as a png
    plt.imsave(
    fname=os.path.splitext(os.path.split(filepath)[1])[0] + "_vBF.png",
    arr=vBF,
    vmin=np.percentile(vBF, 1),
    vmax=np.percentile(vBF, 99),
    cmap="gray",
    )