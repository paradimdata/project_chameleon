from brukerrawconverter import brukerrawconverter
from BackgroundSub_Gui import MainWindow
from BackgroundSub_Gui import MPLCanvas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import xylib

file_type = input("Which file would you like to graph? \n 1 == .csv \n 2 == .raw \n")

if file_type == 1:
    Background = pd.read_csv(input("Please input the name of your background file (include .csv) \n"))
    Sample = pd.read_csv(input("Please input the name of your sample file (include .csv) \n"))
elif file_type == 2:
    background_input = input("Please input the name of your background file (do not include .raw) \n")
    sample_input = input("Please input the name of your sample file (do not include .raw) \n")
    background_name = background_input + 'text.txt'
    sample_name = sample_input + 'text.txt'
    brukerrawconverter(background_input + '.raw', background_name)
    brukerrawconverter(sample_input + '.raw', sample_name)
    Background = pd.read_csv(background_name, sep=' ', header=None, names=['Time','Measurement'])
    Sample = pd.read_csv(sample_name, sep=' ', header=None, names=['Time','Measurement'])

plt.plot(Background.iloc[:,0], Background.iloc[:,1], label='Background')
plt.plot(Sample.iloc[:,0], Sample.iloc[:,1], label='Sample')
plt.legend()
plt.title('Raw Data')
plt.xlabel('Two Theta (Degrees)')
plt.ylabel('Intensity (Arb. Units)')
plt.show()

mult = 0.019
back_adj= Background.copy()
back_adj.iloc[:,1] = back_adj.iloc[:,1].apply(lambda x: x*mult) 

fig, ax = plt.subplots()

plt.plot(back_adj.iloc[:,0], back_adj.iloc[:,1], label='Adjusted Background')
plt.plot(Sample.iloc[:,0], Sample.iloc[:,1], label='Sample')
plt.legend(loc='upper left')
plt.title('Background Adjusted Raw Data')
plt.xlabel('Two Theta (Degrees)')
plt.ylabel('Intensity (Arb. Units)')

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

raw_diff.to_csv('SAMPLE_backgroundSubtracted.csv')