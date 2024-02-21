import numpy as np

def ppmsmpmaparser(inputfile, outputfile):

    metadata_limit = 0
    limit_holder = 0
    array = []
    count = 0

    datafile = open(outputfile,'w')
    
    with open(inputfile, 'r', encoding='latin-1') as fp:
        size = len(fp.readlines())
    with open(inputfile, 'r', encoding='latin-1') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        
    while metadata_limit < 1:  
        if ('Time Stamp' in lines[count]):
            header = lines[count].split(',')
            metadata_limit += 1
            limit_holder = count
        else:
            count += 1

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
    ppmsmpmaparser()


