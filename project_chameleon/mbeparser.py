import os
import pathlib
import shutil
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse

def find_shutter_values(shutter_input):
    """
    ``find_shutter_values`` is a function that deciphers what shutters are open on a specific MBE run from the number given in the shutter control value text file. The number given is a combination of numbers that are 2 raised to an exponent.

    :args: ``shutter_input`` is an integer value.

    :return: returns an array of the decompose exponents that make up the original shutter value.

    :exceptions: None
    
    """

    # Set base values, our input number cannot be greater than 2^10 so we start at an exponent of 10
    exponent = 10
    shutter_array = []

    # Once the exponent is 0 we cannot extract anymore values so we break the loop
    while exponent >= 0: 

        # When the input number is greater than the exponent number, we know the exponent number exists in the input number so we subtract the exponent number and add the exponent to the array
        if shutter_input > 2**exponent:
            shutter_input = shutter_input - 2**exponent
            shutter_array = shutter_array + [exponent + 1]

        # When the input number is exactly equal to the exponent we know we have our final value, this means we can extract the final value and return the array of values
        elif shutter_input == 2**exponent: 
            shutter_array = shutter_array + [exponent + 1]
            return shutter_array
        exponent = exponent - 1


def mbeplot(useful_directory_path, filechoice, shutter_data, output_directory_path = None):
    """
    ``mbeplot`` is a function that takes an MBE measurement file and plots the contents of the file. The plot is shown and saved as a .png file. The plot shows which shutters are open during what portions of the measurement.

    :args: ``useful_directory_path`` is a string or path to the folder containing the measurement file. ``filechoise`` is a string or path to the file that will be plotted. ``shutter_data`` is an array containing the data to be plotted. ``output_directory_path`` is a string or path to the desired output directory. This parameter is optional.

    :return: This function does not return anything. A plot of the data is saved.

    :exceptions: None
    
    """

    # File path is created from choice and saved in a variable
    graph_path = pathlib.Path(useful_directory_path + filechoice) 

    # Data is read from the file, need to skip a header row
    data = np.loadtxt(graph_path,skiprows = 1)

    # Data needs to be adjuseted from seconds to hours so it fits correcty on the plot
    x_values = (data[:, 0])/3600
    y_values = data[:, 1]

    # Plot data, highlight what shutters are open in the process. 
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', label='Data Points')
    plt.xlabel('Time')
    plt.ylabel('Process Value')
    plt.title('Plot of ' + filechoice)
    for index in range(len(shutter_data) - 2): 

        # If there are shutter values we need to show where they are open in the plot
        if find_shutter_values(shutter_data[index + 1][1]):
                # plt.axvspan shades a region of a matplotlib plot. Here we shade a portion of the graph from our first shutter data point to the second. The shutter that is open is added as a label.
                plt.axvspan((shutter_data[index + 1][0]/3600),(shutter_data[index + 2][0]/3600),alpha=0.5, label="Shutter = " + str(find_shutter_values(shutter_data[index + 1][1])),color=(.1,index/len(shutter_data),index/len(shutter_data)))
    plt.legend(title="Values", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.show()

    # If theres an output path, save the file there
    if output_directory_path:
        plt.savefig(output_directory_path + filechoice + '.png')


def mbeparser(file_folder):
    """
    ``mbeparser()`` is a function to allow MBE users to parse their data more quickly and efficiently. The function allows users to sort their data into useful
    and non useful data, then query the useful data for specific files. When the function is run, the user can choose from three different actions: graph a chosen file, graph and save a chosen file, and check a specific setpoint. These actions can be repeated until the user chooses to exit. 

    :args: ``file_folder`` should be the folder containing all .txt files generated during the MBE run.

    :return: Does not return anything. Sorts data into two subdirectories within main directory. Displays plot of chosen file. Saves plot if users decides to save plot. 

    :exceptions: `file_folder` must be a folder. `file_folder` must contain files.
    """

    # Make sure input is a folder and has files in it so the function can run correctly
    if os.path.isdir(file_folder) is False:
        raise ValueError("ERROR: bad input. Expected folder")
    if os.listdir(file_folder) == 0:
        raise ValueError("ERROR: bad input. Data folder should contain files")
    
    # Create two folders to sort all of the mbe text files into and add them into the current file folder. Useful folder will contain all the files that contain useful data. Useless folder will contain only files that contain no relevant data. 
    useless_folder = os.path.join(file_folder, "useless")
    useful_folder = os.path.join(file_folder, "useful")
    output_folder = os.path.join(file_folder, "output_folder")
    for folder in [useless_folder, useful_folder,output_folder]:
        os.makedirs(folder, exist_ok=True)
        
    # Iterate through all the file names in the main folder so that they can be sorted in the loop make sure files are text files
    for filename in os.listdir(file_folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(file_folder, filename)
        elif ('use' in filename or 'output_folder' in filename):
            continue
        else:
            continue

        # Sort files into folders based on name. There are a couple of key words that appear in file names that we can use to sort the files. 
        if ('_Shutter_Control.Value.txt' in filename):
            file_path = (pathlib.Path(file_folder)/filename).resolve()
            with open(file_path, 'r') as file:
                next(file)
                shutter_data = [[float(value) for value in line.split()] for line in file]
            shutil.move(filepath, os.path.join(useless_folder, filename))
        elif ('Alarm' in filename) or ('Proportional' in filename) or ('Integral' in filename) or ('Derivative' in filename) or ('Max' in filename) or ('Min' in filename) or ('UT1' in filename): 
            shutil.move(filepath, os.path.join(useless_folder, filename))
        else:  
            shutil.move(filepath, os.path.join(useful_folder, filename))

    # After files have been sorted, move into the useful folder and list all the useful files
    Useful_directory_path = str(file_folder) + '/useful/'
    Output_directory_path = str(file_folder) + '/output_folder/'
    file_list = os.listdir(Useful_directory_path)

    # We want this loop to run as many times as the user would like. Keep running the loop until the user decides to exit and then we break
    loopholder = 1
    while loopholder > 0:
    
        #Let user decide which file/files they would like to graph
        user_input = input("What would you like to do? \n (1) Graph and show \n (2) Graph, show, and save \n (3) Check set points \n (4) Exit \n (Please only type the number) \n")

        # Graph and show
        if('1' in user_input):
            for file_name in file_list:
                if not ('Setpoint' in file_name):
                    print(file_name)
            filechoice = input("What file would you like to graph? \n")
            #Load and graph selected files
            mbeplot(Useful_directory_path, filechoice, shutter_data)
        
        # Graph, show, and save
        elif('2' in user_input):
            for file_name in file_list:
                if not ('Setpoint' in file_name):
                    print(file_name)
            filechoice = input("What file would you like to graph? \n")
            #Load and graph selected files
            mbeplot(Useful_directory_path, filechoice, shutter_data, output_directory_path = Output_directory_path)
        
        # Check set points
        elif('3' in user_input):
            for file_name in file_list:
                if('Setpoint' in file_name):
                    print(file_name)
            filechoice = input("What file would you like to check? \n")
            f = open(Useful_directory_path + filechoice)
            for line in f:
                print(line)
       
        # Exit (Break the loop)
        elif('4' in user_input):
            break
            

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input folder")
    args = parser.parse_args()
    mbeparser(args.input)