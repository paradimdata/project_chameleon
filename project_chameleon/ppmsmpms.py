import numpy as np
import argparse
import os
import csv

def ppmsmpmsparser(inputfile, outputfile, user_input = None):
    """
    ``ppmsmpmsparser()`` is a function that allows users to separate out relevant columns for 4 different mpms and ppms file types. Relevant columns are saved from the input file into the output file. The user also has the option to pick between 4 different kinds of files: heat capacity, magnetic suceptibility, 4-prode resistivity, and thermal transport.

    :args: ``inputfile`` should be a string or path to a PPMS/MPMS file ending with '.dat'. ``outputfile`` should be a string ending with '.txt' or '.csv' which will be the name of the final output file. ``user_input`` allows the user to select their input file type as a function argument rather than while the file is running. This input is optional.

    :return: this fucntion does not return anything. It saves outputs into a file called ``outputfile``.

    :exceptions: `input_file` must be a file. `input_file` must end with '.dat'. `output_file` must end with '.txt' or '.csv'. `user_input` must be one of the possible values.
    """

    # Error if the inputs are not of the correct type or within correct bounds
    if os.path.isfile(inputfile) is False:
        raise ValueError("ERROR: bad input. Expected file")
    if not inputfile.endswith('.dat'):
        raise ValueError("ERROR: bad input. Expected .dat file")
    if os.path.getsize(inputfile) < 10:
        raise ValueError("ERROR: This size of file cannot be handled by this function. File too small.")
    if not str(outputfile).endswith('.txt') or str(outputfile).endswith('.csv'):
        raise ValueError("ERROR: outputfile should be a .csv file.")
    if user_input not in ['1', '2', '3', '4'] and user_input is not None:
        raise ValueError("ERROR: User Input should be 1, 2, 3, 4, or None")

    #Initialize values and open file
    metadata_limit = 0
    limit_holder = 0
    count = 0
    datafile = open(outputfile,'w')

    #Read size of file and lines in file
    with open(inputfile, 'r', encoding='latin-1') as fp:
        size = len(fp.readlines())
    with open(inputfile, 'r', encoding='latin-1') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    # Find where the header is and where the data starts so we know where to actually start reading from
    while metadata_limit < 1:  
        if ('Time Stamp' in lines[count]):
            header = lines[count].split(',')
            metadata_limit += 1
            limit_holder = count
        else:
            count += 1

    # Optional user input here based on function input. We want this to be able to run as a function either with or without user input
    if user_input == None:
        user_input = input("Which file type is this? \n (1)Heat Capacity \n (2)AC Magnetic Susceptibility \n (3)4-Probe Resistivity \n (4)Thermal Transport \n (Input the number of your choice) \n") 
    if user_input not in ['1', '2', '3', '4'] and user_input is not None:
        raise ValueError("ERROR: User Input should be 1, 2, 3, 4, or None")

    #4-PROBE LOOP
    if('3' in user_input):
        datafile.write(header[1] + ', ' + header[3] + ', ' + header[4] + ', ' + header[6] + ', ' + header[8] + ', ' + header[10] + '\n') # Relevant lines for 4-Probe file
        count = limit_holder + 1
        
        while count < size: # We count for the size for the file
            new_line = lines[count].split(',')
            if ('Error' in new_line[0]):
                continue
            else:
                datafile.write(new_line[1] + ', ' + new_line[3] + ', ' + new_line[4] + ', ' + new_line[6] + ', ' + new_line[8] + ', ' + new_line[10] + '\n') 
                count += 1
        datafile.close()

    #HEAT CAPACITY LOOP
    elif('1' in user_input):
        datafile.write(header[0] + ', ' + header[5] + ', ' + header[7] + ', ' + header[9] + ', ' + header[10] + ', ' + header[18] + ', ' + header[28] + '\n') # Relevant lines for Heat Capacity file
        count = limit_holder + 1
        
        while count < size: # We count for the size for the file
            new_line = lines[count].split(',')
            if ('Error' in new_line[1]):
                continue
            else:
                datafile.write(new_line[0] + ', ' + new_line[5] + ', ' + new_line[7] + ', ' + new_line[9] + ', ' + new_line[10] + ', ' + new_line[18] + ', ' + new_line[28] + '\n')
                count += 1
        datafile.close()

    #AC MAGNETIC SUSCEPTIBILITY LOOP
    elif('2' in user_input):
        datafile.write(header[1] + ', ' + header[2] + ', ' + header[3] + ', ' + header[4] + ', ' + header[5] + ', ' + header[6] + ', ' + header[8] + ', ' + header[9] + '\n') # Relevant lines for Magnetic Susceptibility file
        count = limit_holder + 1
        
        while count < size: # We count for the size for the file
            new_line = lines[count].split(',')
            if ('Error' in new_line[0]):
                continue
            else:
                datafile.write(new_line[1] + ', ' + new_line[2] + ', ' + new_line[3] + ', ' + new_line[4] + ', ' + new_line[5] + ', ' + new_line[6] + ', ' + new_line[8] + ', ' + new_line[9] +'\n')
                count += 1
        datafile.close()

    #THERMAL TRANSPORT LOOP
    elif('4' in user_input):
        datafile.write(header[1] + ', ' + header[4] + ', ' + header[5] + ', ' + header[6] + ', ' + header[8] + ', ' + header[10] + ', ' + header[12] + '\n') # Relevant lines for Thermal Transport file
        count = limit_holder + 1
        
        while count < size: # We count for the size for the file
            new_line = lines[count].split(',')
            if ('Error' in new_line[0]):
                continue
            else:
                datafile.write(new_line[1] + ', ' + new_line[4] + ', ' + new_line[5] + ', ' + new_line[6] + ', ' + new_line[8] + ', ' + new_line[10] + ', ' + new_line[12] + '\n')
                count += 1
        datafile.close()

    #IF THERE IS A TYPO
    else:
        print('Please pick one of the file types')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    ppmsmpmsparser(args.input, args.output)
