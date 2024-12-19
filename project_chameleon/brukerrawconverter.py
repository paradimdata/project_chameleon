import argparse
import xylib
import os

#Function gets the metadata and writes it to a file. Used in main function
def export_metadata(f, meta):
    """
   ``export_metadata`` is a function that extracts metadata from the raw Bruker files. This function was taken from the package xylib for use in this function.

   :args: ``f`` is a file that can be written to. ``meta`` is the section of data that the metadata needs to be extracted from. 

   :return: this function does not return anything. Metadata exported is writen to the file ``f``.

   :exceptions: This function has no exceptions.
    """
    for i in range(meta.size()):
        key = meta.get_key(i)
        value = meta.get(key)
        f.write('# %s: %s\n' % (key, value.replace('\n', '\n#\t')))

#Converts input file into a text file title "output_file.csv"
def brukerrawconverter(input_file, output_file, cps = None):
    """
    ``brukerrawconverter`` is a function that extracts data and metadata from the raw data file, and puts it into a .csv output file. The function does not alter the data, only extracts it. This function has been designed for Bruker .raw and Bruker .UXD files using xylib, but may work for other file formats that can be deciphered by xylib. ``brukerrawconverter`` utilizes the functionality of ``export_metadata``.

    :args: ``input_file`` is a Bruker .raw or Bruker .UXD file. ``Output_file`` is a string or path that ends in '.csv'. ``cps`` is a boolean True/False value that allows the user to control if data headers are collected at the top (True), or integrated into data (False). This input is optional.
    
    :return: does not return anything. Saves ``output_file`` as a .csv file.
    
    :exceptions: ``input_file`` must be a file. ``input_file`` must be one of the expected file types. ``output_file`` must end with '.txt' or '.csv'. ``cps`` must be 'True', 'False', or 'None'.
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

    #Put all headers at the start
    if cps == True:
        for i in range(nb):
            block = d.get_block(i)
            f.write('# block ' + str(i) + '\n')
            export_metadata(f, block.meta)
    #Iterate through the raw file and rewrite columns in the text file
    for i in range(nb):
        block = d.get_block(i)
        if cps == True:
            step_size = block.meta.get(block.meta.get_key(10))
        #Put headers with blocks
        if cps == False:
            if i > 0:
                f.write("\n")
            export_metadata(f, block.meta)

        ncol = block.get_column_count()
        # column 0 is pseudo-column with point indices, we skip it
        col_names = [block.get_column(k).get_name() or ('column_%d' % k)
                    for k in range(1, ncol+1)]
        if cps == False or i == 0:
            f.write('# ' + sep.join(col_names) + '\n')
        nrow = block.get_point_count()
        for j in range(nrow):
            values = ["%.6f" % block.get_column(k).get_value(j)
                    for k in range(1, ncol+1)]
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
