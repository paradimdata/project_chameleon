import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from adjustText import adjust_text

def get_element_peaks(element, df):
    data = df
    data.columns = data.columns.str.strip()
    result = data.loc[data['Element'] == element].values[0][2:]
    result = [x for x in result if str(x)[0].isdigit() and x < 20]
    result = np.around(np.array(result), 2)  # Assuming you want integers
    result = result*100
    result = [int(x) for x in result]
    element_name = np.full(len(result), element, dtype=object).tolist()
    
    return result, element_name

def sem_base_plot(file_name, output_file, color, label = None):

    x = []
    y = []

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
def sem_spectra_peak_labeler(file_name, output_file, elements_in_plot = ''):
    
    input_file = file_name
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
    plt.title(file_name)
    plt.xlim(0, 14)
    
    #Get all peaks from data
    peaks, _ = find_peaks(y, height=20, distance = 15)
    peak_heights = _['peak_heights']
    unknown_peaks = []
    #Load input file containing spectra data and put it into a data frame
    input_file = 'Emissions Spectra Data - Sheet2.csv'
    data_for_peaks = pd.read_csv(input_file, header=0)
    #From given elements, find their peaks and save them
    if elements_in_plot:
        for element in elements:
            r, e = get_element_peaks(element, data_for_peaks)
            r_final = r_final + r
            e_final = e_final + e
    #Compare all peaks and peaks of given elements. Find 5 largest peaks that are not given.
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

    #from 5 largest peaks, find any energies that are within .01 of a peak. Save the elements that have the energies closest to the peak.
    data_for_peaks.columns = data_for_peaks.columns.str.strip()
    data_for_peaks.iloc[:, 1:] = data_for_peaks.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    for peak in sorted_peaks:
        numeric_data = data_for_peaks.iloc[:, 1:]
        indices = np.where((numeric_data >= peak[0] - 0.01) & (numeric_data <= peak[0] + 0.01))
        if len(indices[0]) > 0:
            row_indices.append(indices[0]) 
            col_indices.append(indices[1])
        elif len(indices[0]) == 0:
            indices = np.where((numeric_data >= peak[0] - 0.02) & (numeric_data <= peak[0] + 0.02))
            row_indices.append(indices[0]) 
            col_indices.append(indices[1])

    #Get elements from values that are close to unidentified peaks
    unknown_elements = []
    unknown_x = []
    for idx, value in enumerate(row_indices):
        holder_array = []
        for a in range(len(value)):   
            holder_array.append(data_for_peaks.iloc[row_indices[idx][a],0])
        unknown_elements.append(str(holder_array))
    for z in sorted_peaks:
        unknown_x.append(int(z[0] * 100))
    
    #Created labels with arrows
    green_texts = []
    for i, j in enumerate(r_final):
        green_texts.append(
            plt.text(
                x[j], y[j], f"{e_final[i]}",  
                ha="center", va="bottom", color='green', fontsize=14
            )
        )
    adjust_text(green_texts, arrowprops=dict(arrowstyle='->', color='green', lw=0.5), min_distance=20, only_move='y+')
    # Create red labels and adjust them with arrows
    red_texts = []
    for k, l in enumerate(unknown_x):
        red_texts.append(
            plt.text(
                x[l], y[l], f"{unknown_elements[k]}",  # Use i as the index for the element
                ha="center", va="bottom", color='red', fontsize=14
            )
        )
    adjust_text(red_texts, arrowprops=dict(arrowstyle='->', color='red', lw=0.5), min_distance=20, only_move='y+')

    plt.savefig(output_file)
    plt.show()