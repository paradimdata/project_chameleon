import os
import pathlib
import shutil
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse

def mbeparser(file_folder):
    """
    A function to allow MBE users to parse their data more quickly and efficiently. Function allows users to sort their data into useful
    and non useful data, then query the useful data for specific files. Files can be graphed and saved.

    args: Takes folder that holds text files that hold all of the mbe data
    return: Does not return anything. Sorts data into two subdirectories within main directory. Displays graph of chosen file
    exceptions: will throw an exception if the input is not a file folder. Will throw an exception if files in the folder are not text files
    """

    #Make sure input is a folder
    if os.path.isdir(file_folder) is False:
        raise ValueError("ERROR: bad input. Expected folder")
    
    #Create two folders to sort all of the mbe text files into and add them into the current file folder. Useful folder will contain all the files that contain useful data. Useless folder will contain only files that contain no relevant data. 
    useless_folder = os.path.join(file_folder, "useless")
    useful_folder = os.path.join(file_folder, "useful")
    for folder in [useless_folder, useful_folder]:
        os.makedirs(folder, exist_ok=True)
        
    #Iterate through all the file names in the main folder so that they can be sorted. in the loop make sure files are text files
    for filename in os.listdir(file_folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(file_folder, filename)
        elif ('use' in filename):
            continue
        else:
            raise ValueError("ERROR: bad data. Expected .txt file")

        # Sort files into folders based on name. There are a couple of key words that appear in file names that we can use to sort the files. 
        if ('_Shutter_Control.Value.txt' in filename):
            with open(filename, 'r') as file:
                shutter_data = [[float(value) for value in line.split()] for line in file]
            shutil.move(filepath, os.path.join(useless_folder, filename))
        elif ('Alarm' in filename) or ('Proportional' in filename) or ('Integral' in filename) or ('Derivative' in filename) or ('Max' in filename) or ('Min' in filename) or ('UT1' in filename): 
            shutil.move(filepath, os.path.join(useless_folder, filename))
        else:  
            shutil.move(filepath, os.path.join(useful_folder, filename))

    #After files have been sorted, move into the useful folder and list all the useful files
    Useful_directory_path = file_folder + '/useful/'
    file_list = os.listdir(Useful_directory_path)
    #for file_name in file_list:
     #   if not ('Setpoint' in file_name):
      #      print(file_name)

    loopholder = 1
    while loopholder > 0:
    
        #Let user decide which file/files they would like to graph
        user_input = input("What would you like to do? \n Graph and show \n Graph, show, and save \n Check set points \n Exit \n")

        if('Graph and show' in user_input):
            for file_name in file_list:
                if not ('Setpoint' in file_name):
                    print(file_name)
            filechoice = input("What file would you like to graph? \n")
            #Load and graph selected files
            graph_path = pathlib.Path(Useful_directory_path + filechoice) 
            data = np.loadtxt(graph_path,skiprows = 1)
            x_values = data[:, 0]
            y_values = data[:, 1]
            plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', label='Data Points')
            plt.xlabel('Time')
            plt.ylabel('Process Value')
            plt.title('Plot of ' + filechoice)
            plt.axvspan(shutter_data[2][0],shutter_data[3][0])
            plt.show()
        elif('Graph, show, and save' in user_input):
            for file_name in file_list:
                if not ('Setpoint' in file_name):
                    print(file_name)
            filechoice = input("What file would you like to graph? \n")
            #Load and graph selected files
            graph_path = pathlib.Path(Useful_directory_path + filechoice) 
            data = np.loadtxt(graph_path,skiprows = 1)
            x_values = data[:, 0]
            y_values = data[:, 1]
            plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', label='Data Points')
            plt.xlabel('Time')
            plt.ylabel('Process Value')
            plt.title('Plot of ' + filechoice)
            plt.axvspan(shutter_data[2][0],shutter_data[3][0])
            plt.show()
            plt.savefig(filechoice + '.png')
        elif('Check set points' in user_input):
            for file_name in file_list:
                if('Setpoint' in file_name):
                    print(file_name)
            filechoice = input("What file would you like to check? \n")
            f = open(Useful_directory_path + filechoice)
            for line in f:
                print(line)
        elif('Exit' in user_input):
            break
            

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input folder")
    args = parser.parse_args()
    mbeparser(args.input)