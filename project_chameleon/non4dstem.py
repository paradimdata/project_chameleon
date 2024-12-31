import hyperspy.api as hs
from glob import glob
import matplotlib.pyplot as plt
import os
import argparse

def non4dstem(data_folder = None, outputs_folder = None, data_file = None, output_file = None):
    """
    ``non4dstem`` is a function that takes an input folder or file containing 2D and 3D STEM images and converts those files into plots that are saved either in output folder or as a single output file. This function was tested on .dm4 files, .ser files, and .emd files, but can handle any filetypes that can be parserd by the hyperspy 'load' function. This file can only take inputs in specific pairings. ``data_file`` can be paired with ``output_file`` and ``outputs_folder``. ``data_folder`` may only be paired with ``outputs_folder``. There may only be one data input and one output type input.
 
    :args: ``data_folder`` should be a folder holding all non 4D files that are being processed. ``data_file`` should be a string or path to a single file non 4D stem file. ``outputs_folder`` is a string which will be the name out the folder that holds all the processed images. ``output_file`` is a string which will be the name of the single file output. All inputs are optional. Some are conditionally required.

    :return: this function does not return anything. It saves converted files as .png images in the folder labeled ``output_folder``, or as single .png images.

    :exceptions: ``data_folder`` must be a folder. ``data_folder`` must contain files. ``output_folder`` must not contain a file extension. Will throw exceptions if there are any mismatches in input pairings.  
    """

    # Errors if we have bad combinations of inputs, or if the inputs are not of the correct form
    if data_folder and os.path.isdir(data_folder) is False:
        raise ValueError("ERROR: bad input. Expected folder")
    if outputs_folder and '.' in str(outputs_folder):
        raise ValueError("ERROR: Output Folder should not contain '.'")
    if data_folder and os.listdir(data_folder) == 0:
        raise ValueError("ERROR: bad input. Data folder should contain files")
    if data_folder and data_file:
        raise ValueError("ERROR: Too many inputs. Can only have one of data_folder and data_file")
    if data_folder and output_file:
        raise ValueError("ERROR: Incorrect inputs. data_folder in not compatible with output_file")
    if data_folder and not outputs_folder:
        raise ValueError("ERROR: Incorrect inputs. data_folder must have an outputs_folder")
    if outputs_folder and output_file:
        raise ValueError("ERROR: Too many inputs. Can only have one of outputs_folder and output_file")
    
    # We need if statement for the different combinations of inputs. First combination is folder input which requires folder output
    if data_folder:
        # Create outputs folder and read in files from data folder
        count = 0
        os.makedirs(outputs_folder)
        for file in glob(data_folder + "/*"): # Load all files from the folder
            data = hs.load(file) # hs.load() is how we are reading all the data. Comes from hyperspy

        #For each file that gets read in, plot and save as a figure
        print(data)
        for obj in data:
            count = count + 1
            obj.plot()
            plt.savefig(f"{outputs_folder}/{os.path.splitext(os.path.split(file)[-1])[0]}_{obj.metadata.Signal.signal_type}{count}.png") # Give all the outputs unique names
            plt.close()

    # Second combo is file input with file outputs
    elif data_file and output_file:
        data = hs.load(data_file) # hs.load() is how we are reading all the data. Comes from hyperspy
        data.plot()
        plt.savefig(output_file)
        plt.close()

    # Final combo is file input with folder output
    elif data_file and outputs_folder:
        os.makedirs(outputs_folder)
        data = hs.load(data_file) # hs.load() is how we are reading all the data. Comes from hyperspy
        data.plot()
        plt.savefig(f"{outputs_folder}/{os.path.splitext(os.path.split(data_file)[-1])[0]}_{data.metadata.Signal.signal_type}.png")
        plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input folder")
    parser.add_argument("output", help="the output folder")
    args = parser.parse_args()
    non4dstem(data_folder = args.input, output_folder = args.output)
