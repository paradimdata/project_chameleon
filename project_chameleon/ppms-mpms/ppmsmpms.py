import numpy as np
import sys
import argparse
import os

def ppmsmpmsparser(inputfile, outputfile):
    """
    A function to allow users to parse their ppms and mpms data more efficiently. Allows users to separate out relevant columns for 4 different mpms and ppms file types. Relevant columns are saved from the input file into the output file.

    args: Takes a .dat file or path as an input for inputfile and a name for as an input for outputfile
    return: this fucntion does not return anything. It saves outputs into a file called outputfile
    exceptions: will throw an exception if the input file is not a file
    """

    #Error if the input file is not a file
    if os.path.isfile(inputfile) is False:
        raise ValueError("ERROR: bad input. Expected file")

    #Initialize values and open file
    metadata_limit = 0
    limit_holder = 0
    array = []
    count = 0
    datafile = open(outputfile,'w')

    #Read size of file and lines in file
    with open(inputfile, 'r', encoding='latin-1') as fp:
        size = len(fp.readlines())
    with open(inputfile, 'r', encoding='latin-1') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    #Find where the header is and where the data starts
    while metadata_limit < 1:  
        if ('Time Stamp' in lines[count]):
            header = lines[count].split(',')
            metadata_limit += 1
            limit_holder = count
        else:
            count += 1

    #Take user input to choose which loop to enter
    user_input = input("Which file type is this? \n Heat Capacity \n AC Magnetic Susceptibility \n 4-Probe Resistivity \n Thermal Transport \n") 

    #4-PROBE LOOP
    if('4-Probe Resistivity' in user_input):
        datafile.write(header[1] + ', ' + header[3] + ', ' + header[4] + ', ' + header[6] + ', ' + header[8] + ', ' + header[10] + '\n')
        count = limit_holder
        count += 1  
        
        while count < size:
            new_line = lines[count].split(',')
            if ('Error' in new_line[0]):
                continue
            else:
                datafile.write(new_line[1] + ', ' + new_line[3] + ', ' + new_line[4] + ', ' + new_line[6] + ', ' + new_line[8] + ', ' + new_line[10] + '\n')
                count += 1

    #HEAT CAPACITY LOOP
    elif('Heat Capacity' in user_input):
        datafile.write(header[0] + ', ' + header[5] + ', ' + header[7] + ', ' + header[9] + ', ' + header[10] + ', ' + header[18] + ', ' + header[28] + '\n')
        count = limit_holder
        count += 1  
        
        while count < size:
            new_line = lines[count].split(',')
            if ('Error' in new_line[1]):
                continue
            else:
                datafile.write(new_line[0] + ', ' + new_line[5] + ', ' + new_line[7] + ', ' + new_line[9] + ', ' + new_line[10] + ', ' + new_line[18] + ', ' + new_line[28] + '\n')
                count += 1

    #AC MAGNETIC SUSCEPTIBILITY LOOP
    elif('AC Magnetic Susceptibility' in user_input):
        datafile.write(header[1] + ', ' + header[2] + ', ' + header[3] + ', ' + header[4] + ', ' + header[5] + ', ' + header[6] + ', ' + header[8] + ', ' + header[9] + '\n')
        count = limit_holder
        count += 1  
        
        while count < size:
            new_line = lines[count].split(',')
            if ('Error' in new_line[0]):
                continue
            else:
                datafile.write(new_line[1] + ', ' + new_line[2] + ', ' + new_line[3] + ', ' + new_line[4] + ', ' + new_line[5] + ', ' + new_line[6] + ', ' + new_line[8] + ', ' + new_line[9] +'\n')
                count += 1

    #THERMAL TRANSPORT LOOP
    elif('Thermal Transport' in user_input):
        datafile.write(header[1] + ', ' + header[4] + ', ' + header[5] + ', ' + header[6] + ', ' + header[8] + ', ' + header[10] + ', ' + header[12] + '\n')
        count = limit_holder
        count += 1  
        
        while count < size:
            new_line = lines[count].split(',')
            if ('Error' in new_line[0]):
                continue
            else:
                datafile.write(new_line[1] + ', ' + new_line[4] + ', ' + new_line[5] + ', ' + new_line[6] + ', ' + new_line[8] + ', ' + new_line[10] + ', ' + new_line[12] + '\n')
                count += 1

    #IF THERE IS A TYPO
    else:
        print('Please pick one of the file types')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    ppmsmpmsparser(args.input, args.output)


