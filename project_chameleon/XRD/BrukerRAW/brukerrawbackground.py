from brukerrawconverter import brukerrawconverter
from BackgroundSub_Gui import MainWindow
from BackgroundSub_Gui import MPLCanvas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import xylib
import csv

def brukerrawbackground(background_input, sample_input):

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
    plt.savefig(sample_input + 'raw_data.png')

    mult = input("Please input your multiplier \n")
    back_adj= Background.copy()
    back_adj.iloc[:,1] = back_adj.iloc[:,1].apply(lambda x: x*mult) 

    fig, ax = plt.subplots()

    plt.plot(back_adj.iloc[:,0], back_adj.iloc[:,1], label='Adjusted Background')
    plt.plot(Sample.iloc[:,0], Sample.iloc[:,1], label='Sample')
    plt.legend(loc='upper left')
    plt.title('Background Adjusted Raw Data')
    plt.xlabel('Two Theta (Degrees)')
    plt.ylabel('Intensity (Arb. Units)')
    plt.savefig(sample_input + 'background_adjusted.png')

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
    plt.savefig(sample_input + 'background_subtracted.png')

    raw_diff.to_csv(sample_input + '_backgroundSubtracted.csv')