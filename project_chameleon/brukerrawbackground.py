from project_chameleon.brukerrawconverter import brukerrawconverter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import csv
import argparse
import os

def brukerrawbackground(background_input, sample_input, output_name):
    """
    ``brukerrawbackground`` is a function that takes two input files and an output name. The first output file, ``sample_input``, is the sample file which can be either a bruker raw file 
    or a csv file. The second output file, ``background_input``, is the background subtraction data to be subtracted from the sample file. The ``background_input`` file 
    can be either a bruker raw file or a csv file. This function generates three plots all titled `output_name` + graph version. The plots are one plot of the raw sample 
    data, one plot of the background adjusted data, and one plot of the sample data with the background data subtracted from it. All the plots are saved as .png files.

    :args: this function has three inputs: ``background_input``, ``sample_input``, and ``output_name``. ``background_input`` should be a Bruker .raw file or a .csv file of the background data. ``sample_input`` should be a Bruker .raw file or a .csv file of the sample data. ``output_name`` should be a string which will be the name of the outputs combined with specific output designators.

    :return: does not return anything. Saves outputs as .png files.

    :exceptions: will throw an exception if the either the `background_input` or the `sample_input` are not files.
    """
    
    if os.path.isfile(background_input) is False:
        raise ValueError("ERROR: bad input. Expected file")
    if os.path.isfile(sample_input) is False:
        raise ValueError("ERROR: bad input. Expected file")
    if not (background_input.endswith('.raw') or background_input.endswith('.RAW') or background_input.endswith('.csv')):
        raise ValueError("ERROR: bad input. Background input file should be a bruker raw file or a csv file.")
    if not (sample_input.endswith('.raw') or background_input.endswith('.RAW') or background_input.endswith('.csv')):
        raise ValueError("ERROR: bad input. Sample input file should be a bruker raw file or a csv file.")
    if os.path.getsize(background_input) < 10:
        raise ValueError("ERROR: This size of file cannot be handled by this function. File too small.")
    if os.path.getsize(sample_input) < 10:
        raise ValueError("ERROR: This size of file cannot be handled by this function. File too small.")
    if '.' in output_name:
        raise ValueError("ERROR: Output Folder should not contain '.'")

    if background_input.endswith('.csv'):
        Background = pd.read_csv(background_input)
    else:
        background_name = background_input + 'text.txt'
        brukerrawconverter(background_input, background_name)
        with open(background_name, 'r') as txtfile:
            lines = txtfile.readlines()   
        with open(background_input + '.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for line in lines:
                if ('#' in line):
                    continue
                else:
                    columns = line.strip().split()
                    csvwriter.writerow(columns)
        Background = pd.read_csv(background_input + '.csv', sep=' ', header=None, names=['Time','Measurement'])

    if sample_input.endswith('.csv'):
        Sample = pd.read_csv(sample_input)
    else:
        sample_name = sample_input + 'text.txt'
        brukerrawconverter(sample_input, sample_name)
        with open(sample_name, 'r') as txtfile:
            lines = txtfile.readlines()   
        with open(sample_input + '.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for line in lines:
                if ('#' in line):
                    continue
                else:
                    columns = line.strip().split()
                    csvwriter.writerow(columns)
        Sample = pd.read_csv(sample_input + '.csv', sep=' ', header=None, names=['Time','Measurement'])   

    plt.plot(Background.iloc[:,0], Background.iloc[:,1], label='Background')
    plt.plot(Sample.iloc[:,0], Sample.iloc[:,1], label='Sample')
    plt.legend()
    plt.title('Raw Data')
    plt.xlabel('Two Theta (Degrees)')
    plt.ylabel('Intensity (Arb. Units)')
    plt.show()
    plt.savefig(output_name + '_raw_data.png')

    mult = float(input("Please input your multiplier \n"))
    back_adj= Background.copy()
    back_adj.iloc[:,1] = back_adj.iloc[:,1].apply(lambda x: x*mult) 

    fig, ax = plt.subplots()

    plt.plot(back_adj.iloc[:,0], back_adj.iloc[:,1], label='Adjusted Background')
    plt.plot(Sample.iloc[:,0], Sample.iloc[:,1], label='Sample')
    plt.legend(loc='upper left')
    plt.title('Background Adjusted Raw Data')
    plt.xlabel('Two Theta (Degrees)')
    plt.ylabel('Intensity (Arb. Units)')
    plt.savefig(output_name + '_background_adjusted.png')

    x1, x2, y1, y2 = 60, 150, 0, 800  # subregion of the original image
    axins = ax.inset_axes(
        [0.5, 0.5, 0.47, 0.47],
        xlim=(x1, x2), ylim=(y1, y2))
    axins.plot(back_adj.iloc[:,0], back_adj.iloc[:,1], label='Background')
    axins.plot(Sample.iloc[:,0], Sample.iloc[:,1], label='BCAVO')

    ax.indicate_inset_zoom(axins, edgecolor='black')
    plt.show()

    raw_diff= back_adj.copy()
    raw_diff.iloc[:,1] = Sample.iloc[:,1] - back_adj.iloc[:,1]

    plt.plot(raw_diff.iloc[:,0], raw_diff.iloc[:,1], label='Sample Subtracted')
    plt.legend()
    plt.title('Background Subtracted Raw Data')
    plt.xlabel('Two Theta (Degrees)')
    plt.ylabel('Intensity (Arb. Units)')
    plt.show()
    plt.savefig(output_name + '_background_subtracted.png')

    raw_diff.to_csv(output_name+ '_backgroundSubtracted.csv')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("background file input", help="the input file for the background data")
    parser.add_argument("sample file input", help="the input file for the sample data")
    parser.add_argument("output name", help="the name for all outputs that are saved")
    args = parser.parse_args()
    brukerrawconverter(args.input, args.output)