from .brukerrawconverter import brukerrawconverter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import csv
import argparse
import os
import shutil

def brukerrawbackground(background_input, sample_input, output_name):
    """
    ``brukerrawbackground`` is a function that takes sample data and corresponding background subtraction data, and creates three plots: a plot of the sample data, a plot of the background data, and a plot of the sample data with background data subtracted. These plots are saved as .png files in a folder with name `output_name`. This function utilizes the functionality of the function ``brukerrawconverter``. 

    :args: ``background_input`` should be a Bruker .raw/.csv file of the background data. ``sample_input`` should be a Bruker .raw/.csv file of the sample data. ``output_name`` should be a string which will be the name of the outputs. This output should not contain file extensions. 

    :return: does not return anything. Saves outputs as .png files.

    :exceptions: `background_input` and `sample_input` must be files. `background_input` and `sample_input` must be expected file types. `output_name` must not contain file extension.
    """
    
    # Make sure that all file are of the correct kind so the function can run without error
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
    if '.' in str(output_name):
        raise ValueError("ERROR: Output name should not contain '.'")
    
    # Normalize output name to a string
    output_name = str(output_name)

    # If input file is a .csv, just read the data from the csv into a pandas data frame
    if background_input.endswith('.csv'):
        Background = pd.read_csv(background_input)

    # If the input file is not a .csv, we know it is a Bruker raw so we have to make a new text file, use that as an input for brukerrawconverter, and then read the output data from the new text file and put it into a data frame so we have a consistent file type to work from
    else:
        background_name = background_input + 'text.txt'
        brukerrawconverter(background_input, background_name) # Call to brukerrawconverter with new text file
        with open(background_name, 'r') as txtfile:
            lines = txtfile.readlines()   
        with open(background_input + '.csv', 'w', newline='') as csvfile: # Write data from text file into a newly created .csv
            csvwriter = csv.writer(csvfile)
            for line in lines:
                if ('#' in line): 
                    continue
                else:
                    columns = line.strip().split()
                    csvwriter.writerow(columns)
        Background = pd.read_csv(background_input + '.csv', sep=' ', header=None, names=['Time','Measurement']) # From the new .csv, read into data frame

    # If input file is a .csv, just read the data from the csv into a pandas data frame
    if sample_input.endswith('.csv'):
        Sample = pd.read_csv(sample_input)

    # If the input file is not a .csv, we know it is a Bruker raw so we have to make a new text file, use that as an input for brukerrawconverter, and then read the output data from the new text file and put it into a data frame so we have a consistent file type to work from
    else:
        sample_name = sample_input + 'text.txt'
        brukerrawconverter(sample_input, sample_name) # Call to brukerrawconverter with new text file
        with open(sample_name, 'r') as txtfile:
            lines = txtfile.readlines()   
        with open(sample_input + '.csv', 'w', newline='') as csvfile: # Write data from text file into a newly created .csv
            csvwriter = csv.writer(csvfile)
            for line in lines:
                if ('#' in line):
                    continue
                else:
                    columns = line.strip().split()
                    csvwriter.writerow(columns)
        Sample = pd.read_csv(sample_input + '.csv', sep=' ', header=None, names=['Time','Measurement']) # From the new .csv, read into data frame 

    # Plot background data, and sample data independently on the same plot. Save as the raw data.png
    plt.plot(Background.iloc[:,0], Background.iloc[:,1], label='Background')
    plt.plot(Sample.iloc[:,0], Sample.iloc[:,1], label='Sample')
    plt.legend()
    plt.title('Raw Data')
    plt.xlabel('Two Theta (Degrees)')
    plt.ylabel('Intensity (Arb. Units)')
    plt.show()
    plt.savefig(output_name + '_raw_data.png')

    # User must put in their mutiplier so it can be applied to the background data
    mult = float(input("Please input your multiplier \n"))
    back_adj= Background.copy()
    back_adj.iloc[:,1] = back_adj.iloc[:,1].apply(lambda x: x*mult) 

    # Create multiple plots in the same figure
    fig, ax = plt.subplots()

    # Plot adjusted background data, and sample data independently on the same plot. Save as the raw data.png
    plt.plot(back_adj.iloc[:,0], back_adj.iloc[:,1], label='Adjusted Background')
    plt.plot(Sample.iloc[:,0], Sample.iloc[:,1], label='Sample')
    plt.legend(loc='upper left')
    plt.title('Background Adjusted Raw Data')
    plt.xlabel('Two Theta (Degrees)')
    plt.ylabel('Intensity (Arb. Units)')
    plt.savefig(output_name + '_background_adjusted.png')

    # Place plots in image
    x1, x2, y1, y2 = 60, 150, 0, 800  # subregion of the original image
    axins = ax.inset_axes(
        [0.5, 0.5, 0.47, 0.47],
        xlim=(x1, x2), ylim=(y1, y2))
    axins.plot(back_adj.iloc[:,0], back_adj.iloc[:,1], label='Background')
    axins.plot(Sample.iloc[:,0], Sample.iloc[:,1], label='BCAVO')

    ax.indicate_inset_zoom(axins, edgecolor='black')
    plt.show()

    # Subtract background data from sample data
    raw_diff= back_adj.copy()
    raw_diff.iloc[:,1] = Sample.iloc[:,1] - back_adj.iloc[:,1]

    # Plot background subtracted data
    plt.plot(raw_diff.iloc[:,0], raw_diff.iloc[:,1], label='Sample Subtracted')
    plt.legend()
    plt.title('Background Subtracted Raw Data')
    plt.xlabel('Two Theta (Degrees)')
    plt.ylabel('Intensity (Arb. Units)')
    plt.show()
    plt.savefig(output_name + '_background_subtracted.png')
    raw_diff.to_csv(output_name+ '_backgroundSubtracted.csv')

    # Create new folder to hold outputs
    output_folder = Path(str(output_name))
    os.makedirs(output_folder)

    #Sort all the slices into the directory. We need extensive checks to make sure correct files are moved into the folder
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith('.png') or filename.endswith('.csv'):
            filepath = os.path.join(current_directory, filename)
        else:
            continue
        if (str(output_name) in filename) and ('_raw_data' in filename): 
            shutil.move(filepath, os.path.join(output_folder, filename))
        elif (str(output_name) in filename) and ('_background_adjusted' in filename):
            shutil.move(filepath, os.path.join(output_folder, filename))
        elif (str(output_name) in filename) and ('_background_subtracted' in filename):
            shutil.move(filepath, os.path.join(output_folder, filename))
        elif (str(output_name) in filename) and ('_backgroundSubtracted' in filename):
            shutil.move(filepath, os.path.join(output_folder, filename))
        else:  
            continue


def main():
    parser = argparse.ArgumentParser(description="Process some input files for background and sample data")
    parser.add_argument("background_file_input", help="the input file for the background data")
    parser.add_argument("sample_file_input", help="the input file for the sample data")
    parser.add_argument("output_name", help="the name for all outputs that are saved")
    args = parser.parse_args()
    brukerrawbackground(args.background_file_input, args.sample_file_input, args.output_name)


if __name__ == "__main__":
    main()
