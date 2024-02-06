import os
import pathlib
import shutil
import matplotlib.pyplot as plt
import numpy as np

def mbeparser(file_folder):
    useless_folder = os.path.join(directory_path, "useless")
    useful_folder = os.path.join(directory_path, "useful")
    for folder in [useless_folder, useful_folder]:
        os.makedirs(folder, exist_ok=True)
    for filename in os.listdir(directory_path):
    filepath = os.path.join(directory_path, filename)

        # Sort files into folders based on name
        if ('Alarm' in file_name) or ('Proportional' in file_name) or ('Integral' in file_name) or ('Derivative' in file_name) or ('Max' in file_name) or ('Min' in file_name) or ('UT1' in file_name): 
            shutil.move(filepath, os.path.join(useless_folder, filename))
        else:  
            shutil.move(filepath, os.path.join(useful_folder, filename))
            
    Useful_directory_path = file_folder + 'Useful/'
    file_list = os.listdir(Useful_directory_path)
    for file_name in file_list:
        print(file_name)
    user_input = input("Which file would you like to graph? ")
    graph_path = pathlib.Path(Useful_directory_path + user_input) 
    data = np.loadtxt(graph_path,skiprows = 1)
    x_values = data[:, 0]
    y_values = data[:, 1]
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', label='Data Points')
    plt.xlabel('Time')
    plt.ylabel('Process Value')
    plt.title('Plot of ' + user_input)
    plt.show()
    
    