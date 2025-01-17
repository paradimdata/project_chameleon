import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from adjustText import adjust_text

def get_element_peaks(element, df):
    """
    ``get_element_peaks()`` is a helper function for the SEM plotting functions. This function extracts the energy values of the peak of the element that was input.

    :args: ``element`` should be an element from the periodic table. ``df`` should be a pandas data frame containing periodic elements and their energy peaks. 

    :return: ''result'' is the integer values of the energy peaks. ''element_name'' is the name of the element input.

    :exception: None
    """

    data = df
    data.columns = data.columns.str.strip()
    result = data.loc[data['Element'] == element].values[0][2:]
    result = [x for x in result if str(x)[0].isdigit() and x < 20]
    result = np.around(np.array(result), 2)  # Assuming you want integers
    result = result*100
    result = [int(x) for x in result]
    element_name = np.full(len(result), element, dtype=object).tolist()
    
    return result, element_name

def sem_base_plot(file_name, output_file, color = None, label = None):
    """
    ``sem_base_plot()`` is a function that converts JEOL SEM .EMSA files into a plot. This plot displays the number of counts at each energy level.

    :args: ``file_name`` should be a .EMSA file. ``output_file`` should be a string which will be the name of the output .png file. 

    :return: this function does not return anything. The output is saved as an image file.

    :exception: `file_name` must be an .EMSA file. `file_name` must be a file. `output_file` must end with '.png'.
    """

    #Make sure inputs are of correct type
    if not str(file_name).endswith('.EMSA'):
        raise ValueError("ERROR: bad input. Expected .EMSA file")
    if not str(output_file).endswith('.png'):
        raise ValueError("ERROR: please make your output file a .png file")
    if not os.path.isfile(file_name):
        raise ValueError("ERROR: Input should be a file. Check if your file exists.")

    x = []
    y = []

    # Set black as default color
    if not color:
        color = 'Black'

    with open(file_name,"rb") as f:
        data = f.read()
    data = str(data)
    data = data.split("\\r\\n")
    for i in data:
        if ',' in i:
            x.append(float(i.split(',')[0]))  # Convert first value to float
            y.append(float(i.split(',')[1]))  # Convert second value to float

    # Convert to numpy arrays (optional, for efficiency)
    x = np.array(x)
    y = np.array(y)

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(20, 6))  # Set figure size here
    bars = ax.bar(x, y, width=0.025, color = color)

    if label == None:
        ax.set_title('Plot of ' + str(file_name))
    else:
        ax.set_title(str(label))
    ax.set_ylabel('Counts')
    ax.set_xlabel('keV')
    ax.set_xlim(0, 14)

    plt.savefig(output_file)

#Current working function
def sem_spectra_peak_labeler(input_file, output_file, elements_in_plot = ''):
    """
    ``sem_spectra_peak_labeler()`` is a function that converts JEOL SEM .EMSA files into a plot. This plot displays the number of counts at each energy level, and labels the peaks with the expected elements.

    :args: ``file_name`` should be a .EMSA file. ``output_file`` should be a string which will be the name of the output .png file. ``elements_in_plot`` is a comma separated string containing the elements that are expected to be in the plot.

    :return: this function does not return anything. The output is saved as an image file.

    :exception: `file_name` must be an .EMSA file. `file_name` must be a file. `output_file` must end with '.png'.
    """

    elements = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]

    #Make sure inputs are of correct type
    if not str(input_file).endswith('.EMSA'):
        raise ValueError("ERROR: bad input. Expected .EMSA file")
    if not str(output_file).endswith('.png'):
        raise ValueError("ERROR: please make your output file a .png file")
    if not os.path.isfile(input_file):
        raise ValueError("ERROR: Input should be a file. Check if your file exists.")
    for element in elements_in_plot:
        if element not in elements:
            raise ValueError("ERROR: elements should be real elements. Make sure all elements are correct.")

    x = []
    y = []
    r_final = []
    e_final = []
    row_indices = []
    col_indices = []
    elements = elements_in_plot.split(',')
    with open(input_file,"rb") as f:
        data = f.read()
    data = str(data)
    data = data.split("\\r\\n")
    for i in data:
        if ',' in i:
            x.append(float(i.split(',')[0]))  # Convert first value to float
            y.append(float(i.split(',')[1]))  # Convert second value to float

    # Convert to numpy arrays (optional, for efficiency)
    x = np.array(x)
    y = np.array(y)

    plt.figure(figsize=(20,6))
    plt.bar(x,y,align='center',width=0.025)
    plt.xlabel('keV')
    plt.ylabel('Counts')
    plt.title(input_file)
    plt.xlim(0, 14)
    
    
    peaks, _ = find_peaks(y, height=20, distance = 15)
    peak_heights = _['peak_heights']
    unknown_peaks = []
    
    input_file = 'Emissions Spectra Data - Sheet2.csv'
    data_for_peaks = pd.read_csv(input_file, header=0)
    if elements_in_plot:
        for element in elements:
            r, e = get_element_peaks(element, data_for_peaks)
            r_final = r_final + r
            e_final = e_final + e

    index = 0
    for peak in peaks:
        start, end = peak - 3, peak + 3
        in_range = any(start <= num <= end for num in r_final)
        if not in_range:
            unknown_peaks.append((peak,peak_heights[index]))
        index+=1
    sorted_peaks = sorted( unknown_peaks, key=lambda x: x[1])
    sorted_peaks = sorted_peaks[-5:]
    sorted_peaks = [list(t) for t in sorted_peaks]
    for peak in sorted_peaks:
        peak[0] = peak[0]/100

    data_for_peaks.columns = data_for_peaks.columns.str.strip()
    data_for_peaks.iloc[:, 1:] = data_for_peaks.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    for peak in sorted_peaks:
        numeric_data = data_for_peaks.iloc[:, 1:]
        indices = np.where((numeric_data >= peak[0] - 0.03) & (numeric_data <= peak[0] + 0.03))
        if len(indices[0]) > 0:
            row_indices.append(indices[0]) 
            col_indices.append(indices[1])
        elif len(indices[0]) == 0:
            indices = np.where((numeric_data >= peak[0] - 0.04) & (numeric_data <= peak[0] + 0.04))
            row_indices.append(indices[0]) 
            col_indices.append(indices[1])

    unknown_elements = []
    unknown_x = []
    for idx, value in enumerate(row_indices):
        holder_array = []
        for a in range(len(value)):
            if data_for_peaks.iloc[row_indices[idx][a],0] not in holder_array:
                holder_array.append(data_for_peaks.iloc[row_indices[idx][a],0])
        unknown_elements.append(str(holder_array))

    print(unknown_elements)
    for z in sorted_peaks:
        unknown_x.append(int(z[0] * 100))
    
    for i, j in enumerate(r_final):
        plt.text(x[j], y[j], f"{e_final[i]}", color="green")
        
    # Create red labels and adjust them with arrows
    count = 0
    for k, l in enumerate(unknown_x):
        count += 1
        plt.plot([], [], 'ro', label=f"{count}: {unknown_elements[k]}")
        plt.text(x[l], y[l], f"{count}", color="red")

    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.savefig(output_file)
    plt.show()