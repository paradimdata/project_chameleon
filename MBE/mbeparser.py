import os
import pathlib
import shutil
import matplotlib.pyplot as plt
import numpy as np

def mbeparser(file_folder):
    
    #Start by creating two folders to sort all of the mbe text files into and add them into the current file folder. Useful folder will contain all the files that contain useful data. Useless folder will contain only files that contain no relevant data. 
    useless_folder = os.path.join(file_folder, "useless")
    useful_folder = os.path.join(file_folder, "useful")
    for folder in [useless_folder, useful_folder]:
        os.makedirs(folder, exist_ok=True)
        
    #Iterate through all the file names in the main folder so that they can be sorted.
    for filename in os.listdir(file_folder):
    filepath = os.path.join(file_folder, filename)

        # Sort files into folders based on name. There are a couple of key words that appear in file names that we can use to sort the files. 
        if ('Alarm' in file_name) or ('Proportional' in file_name) or ('Integral' in file_name) or ('Derivative' in file_name) or ('Max' in file_name) or ('Min' in file_name) or ('UT1' in file_name): 
            shutil.move(filepath, os.path.join(useless_folder, filename))
        else:  
            shutil.move(filepath, os.path.join(useful_folder, filename))

    #After files have been sorted, move into the useful folder and list all the useful files
    Useful_directory_path = file_folder + 'Useful/'
    file_list = os.listdir(Useful_directory_path)
    for file_name in file_list:
        print(file_name)

    #Let user decide which file/files they would like to graph
    user_input = input("Which file would you like to graph? ")

    #Load and graph selected files
    graph_path = pathlib.Path(Useful_directory_path + user_input) 
    data = np.loadtxt(graph_path,skiprows = 1)
    x_values = data[:, 0]
    y_values = data[:, 1]
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', label='Data Points')
    plt.xlabel('Time')
    plt.ylabel('Process Value')
    plt.title('Plot of ' + user_input)
    plt.show()
    
    