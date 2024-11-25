import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from adjustText import adjust_text

def get_element_peaks(element):
    input_file = 'Emissions Spectra Data - Sheet2.csv'
    data = pd.read_csv(input_file, header=0)
    data.columns = data.columns.str.strip()
    result = data.loc[data['Element'] == element].values[0][2:]
    result = [x for x in result if str(x)[0].isdigit() and x < 20]
    result = np.around(np.array(result), 2)  # Assuming you want integers
    result = result*100
    result = [int(x) for x in result]
    element_name = np.full(len(result), element, dtype=object).tolist()
    
    return result, element_name

def sem_spectra_grapher(file_name, output_file, elements_in_plot = ''):
    
    input_file = file_name
    x = []
    y = []
    r_final = []
    e_final = []
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
    
    peaks, _ = find_peaks(y, height=20, distance = 15)
    
    if elements_in_plot:
        for element in elements:
            r, e = get_element_peaks(element)
            r_final = r_final + r
            e_final = e_final + e
    
    plt.figure(figsize=(20,6))
    barplot = plt.bar(x,y,align='center',width=0.025)
    texts = []
    for i, r in enumerate(r_final):
        texts.append(
            plt.text(
                x[r], y[r], f"{e_final[i]}",  # Use i as the index for the element
                ha="center", va="bottom", color='red', fontsize=14
            )
        )
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red',lw=0.5))
    plt.xlabel('keV')
    plt.ylabel('Counts')
    plt.title(file_name)
    plt.xlim(0, 15)
    plt.savefig(output_file)