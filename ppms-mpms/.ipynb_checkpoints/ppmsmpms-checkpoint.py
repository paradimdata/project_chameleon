import numpy as np
metadata_limit = 0
limit_holder = 0
array = []
count = 0

def ppmsmpmaparser(inputfile, outputfile):

    datafile = open(outputfile,'w')
    
    with open(inputfile, 'r', encoding='latin-1') as fp:
        size = len(fp.readlines())
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        
    while metadata_limit < 1:
        if ('TITLE' in lines[count]):
            datafile.write(lines[count] + '\n')  
        elif ('Time Stamp' in lines[count]):
            header = lines[count].split(',')
            metadata_limit += 1
            limit_holder = count
        else:
            continue
        count += 1

    while count < size:
        array.append(lines[count].split(','))
        count += 1
    
    datafile.write(header[0] + ', ' + header[4] + ', ' + header[5] + ', ' + header[6] + '\n')
    count = limit_holder
    while count < size:
        if ('Error' in array[count][1]):
            continue
        else:
            datafile.write(array[count][0] + ', ' + array[count][4] + ', ' + array[count][5] + ', ' + array[count][6] + '\n')
            count += 1




