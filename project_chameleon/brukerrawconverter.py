import argparse
import xylib
import os

#Function gets the metadata and writes it to a file. Used in main function
def export_metadata(f, meta):
    """
   ``export_metadata`` is a function that extracts metadata from the raw Bruker files. This function was taken from the package xylib for use in this function.

   :args: this function has two inputs: ``f`` and ``meta``. ``f`` is a file that can be written to. ``meta`` is the section of data that the metadata needs to be extracted from. 

   :return: this function does not return anything. Metadata exported is writen to the file ``f``.

   :exceptions: none
    """
    for i in range(meta.size()):
        key = meta.get_key(i)
        value = meta.get(key)
        f.write('# %s: %s\n' % (key, value.replace('\n', '\n#\t')))

#Converts input file into a text file title "output_file.txt"
def brukerrawconverter(input_file, output_file, cps = None):
    """
    ``brukerrawconverter`` is a function that takes an input file, extracts the data from the input, and writes it to the output file. This function extracts all data as well as metadata from the sample files. 
    This function has been designed for Bruker .raw and Bruker .UXD files, but may work for other file formats that can be deciphered by xylib. 

    :args: this function has two inputs: ``input_file`` and ``output_file``. ``input_file`` should be a Bruker .raw or Bruker .UXD file. ``Output_file`` is a string that will be used for the name of the output file that is created in the function
    
    :return: does not return anything. Saves ``output_file`` as a text file.
    
    :exceptions: will throw an exception if the ``input_file`` is not a file.
    """

    #Check if input is a file
    if os.path.isfile(input_file) is False:
        raise ValueError("ERROR: bad input. Expected file")
    if not (str(input_file).endswith('.raw') or str(input_file).endswith('.uxd') or str(input_file).endswith('.RAW')):
        raise ValueError("ERROR: bad input. Expected .raw file or .uxd file.")
    if not (str(output_file).endswith('.txt') or str(output_file).endswith('.csv')):
        raise ValueError("ERROR: Output file should be a text file.")
    if os.path.getsize(input_file) < 10:
        raise ValueError("ERROR: This size of file cannot be handled by this function. File too small.")
    if not cps in [True, False, None]:
        raise ValueError("ERROR: cps variable may only contain values 'True', 'False', or 'None'.")
    
    # Default tab separated, but understand CSV
    sep = '\t'
    if str(output_file).endswith(".csv"):
        sep = ','

    #Load input file and create output text file
    d = xylib.load_file(input_file)
    f = open(output_file,"w+")
    f.write('# exported by xylib from a %s file\n' % d.fi.name)
    nb = d.get_block_count()

    #If there is more than one block, cps defaults to true, otherwise defaults to false
    if not cps and nb > 1:
        cps = True
    else:
        cps = False

    #Iterate through the raw file and rewrite columns in the text file
    for i in range(nb):
        block = d.get_block(i)
        #Get step size
        if cps == True:
            step_size = block.meta.get(block.meta.get_key(10))
        if i > 0:
            f.write("\n")
        export_metadata(f, block.meta)

        ncol = block.get_column_count()
        # column 0 is pseudo-column with point indices, we skip it
        col_names = [block.get_column(k).get_name() or ('column_%d' % k)
                    for k in range(1, ncol+1)]
        f.write('# ' + sep.join(col_names) + '\n')
        nrow = block.get_point_count()
        #Get actualy values and process them if necessary 
        for j in range(nrow):
            values = ["%.6f" % block.get_column(k).get_value(j)
                    for k in range(1, ncol+1)]
            print(values[1])
            if cps:
                values[1] = str(float(values[1])/float(step_size))
            f.write(sep.join(values) + '\n')
    f.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    brukerrawconverter(args.input, args.output)
