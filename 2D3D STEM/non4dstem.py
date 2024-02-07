import hyperspy.api as hs
from glob import glob
import matplotlib.pyplot as plt
import os

def non4dstem():

    #Read in files from data folder
    for file in glob("data/*"):
    data = hs.load(file)

    #For each file that gets read in, plot and save as a figure
    for obj in data:
        obj.plot()
        plt.savefig(f"outputs/{os.path.splitext(os.path.split(file)[-1])[0]}_{obj.metadata.Signal.signal_type}.png")
    