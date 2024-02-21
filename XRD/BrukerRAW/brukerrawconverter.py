import argparse
import sys
import xylib
import os

#Function gets the metadata and writes it to a file. Used in main function
def export_metadata(f, meta):
    """
    A function to extract metadata from files
    """
    for i in range(meta.size()):
        key = meta.get_key(i)
        value = meta.get(key)
        f.write('# %s: %s\n' % (key, value.replace('\n', '\n#\t')))

#Converts input file into a text file title "output_file.txt"
def brukerrawconverter(input_file, output_file):
    """
    A function that takes an input file, extracts the data from the input, and writes it to the output file.
    This function should work for all file types that the xylib library can handle, but it is primarily being used for Bruker RAW and Bruker XRD formats here.

    args: first argument is input_file. Input_file is one of the supported file types. Second arguemnt is output_file. Output_file is a string that will be used for the name of the output file that is created in the function
    return: does not return anything. Saves output_file as a text file
    exceptions: will throw an exception if the input_file is not a file
    """

    #Check if input is a file
    if os.path.isfile(input_file) is False:
        raise ValueError("ERROR: bad input. Expected file")
    
    #Load input file and create output text file
    d = xylib.load_file(input_file)
    f = open(output_file,"w+")
    f.write('# exported by xylib from a %s file\n' % d.fi.name)
    nb = d.get_block_count()

    #Iterate through the raw file and rewrite columns in the text file
    for i in range(nb):
        block = d.get_block(i)
        if nb > 1 or block.get_name():
            f.write('\n### block #%d %s\n', i, block.get_name())
        else:
            export_metadata(f, block.meta)
    
        ncol = block.get_column_count()
        # column 0 is pseudo-column with point indices, we skip it
        col_names = [block.get_column(k).get_name() or ('column_%d' % k)
                     for k in range(1, ncol+1)]
        f.write('# ' + '\t'.join(col_names) + '\n')
        nrow = block.get_point_count()
        for j in range(nrow):
            values = ["%.6f" % block.get_column(k).get_value(j)
                      for k in range(1, ncol+1)]
            f.write('\t'.join(values) + '\n')

if __name__ == '__main__':
    brukerrawconverter()