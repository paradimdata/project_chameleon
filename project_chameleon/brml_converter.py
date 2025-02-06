import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import argparse
import zipfile
import shutil
import time
import os

def brml_converter(input_file, output_file):
    """
    ``brml_converter`` is a function that extracts data and metadata from the raw data file, and puts it into a .csv output file. The function does not alter the data, only extracts it. This function has been designed for Bruker .brml files.

    :args: ``input_file`` is a Bruker .brml file. ``Output_file`` is a string or path that ends in '.csv' or '.txt. 
    
    :return: does not return anything. Saves ``output_file`` as a .csv/.txt file.
    
    :exceptions: ``input_file`` must be a file. ``input_file`` must be one of the expected file types. ``output_file`` must end with '.txt' or '.csv'. 
    """
    # Check input values for correct types
    if os.path.isfile(input_file) is False:
        raise ValueError("ERROR: bad input. Expected file")
    if not (str(input_file).endswith('.brml')):
        raise ValueError("ERROR: bad input. Expected .brml file.")
    if not (str(output_file).endswith('.txt') or str(output_file).endswith('.csv')):
        raise ValueError("ERROR: Output file should be a text file.")
    if os.path.getsize(input_file) < 10:
        raise ValueError("ERROR: This size of file cannot be handled by this function. File too small.")
    
    # Initialize variables
    extract_to = "holder"
    string_array = []  

    # Bruker brml files can be treated like zip files. Here ZipFile is used to extract data from compressed to readable format. Data is put into a folder called 'holder'. Within the folder, there are a series of .xml files holding data and metadata.
    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # Establish .xml file strucutre
    tree = ET.parse(extract_to + '/experiment0/RawData0.xml')
    root = tree.getroot()

    # Extract main data from the xml file. Held in the 'Datum' header
    for Datum in root.iter('Datum'):
        string_array.append(Datum.text.split(','))

    voltage_value = root.find(".//Voltage").attrib.get("Value") # Voltage value
    current_value = root.find(".//Current").attrib.get("Value") # Current value
    scan_type = root.find(".//ScanInformation").attrib.get("ScanName") # Scan name
    theta2_value = root.find(".//Start").text # Start 2Theta, Start angle value

    beam_translation = root.find(".//InfoData[@LogicName='BeamTranslation']")
    position_value = beam_translation.find("./Position").attrib.get("Value")
    virtual_position_value = beam_translation.find("./VirtualPosition").attrib.get("Value") # Start beam translation value

    phi_drive = root.find(".//InfoData[@LogicName='Phi']")
    position_value = phi_drive.find("./Position").attrib.get("Value") # Phi value

    theta_axis = root.find(".//ScanAxisInfo[@AxisId='Theta']")
    theta_value = theta_axis.find("./Start").text # Theta value

    measurement_points = root.find(".//MeasurementPoints").text
    scan_steps = root.find(".//SubScanInfo").attrib.get("Steps") # Steps value

    two_theta_axis = root.find(".//ScanAxisInfo[@AxisId='TwoTheta']")
    increment_value = two_theta_axis.find("./Increment").text # Step size value
 
    # Find all SubScanInfo elements and extract and store MeasuredTimePerStep and PlannedTimePerStep values
    subscan_infos = root.findall(".//SubScanInfo")
    subscan_data = [
        {
            "MeasuredTimePerStep": subscan.get("MeasuredTimePerStep"),
            "PlannedTimePerStep": subscan.get("PlannedTimePerStep"),
        }
        for subscan in subscan_infos
    ]

    # If there are multiple scans we want to find the start and stop angles for each scan. Theres only one stop value, but multiple start values. First start value is repeated.
    if len(subscan_data) > 1:
        two_theta_starts = [
            scan_axis.find("Start").text
            for scan_axis in root.findall(".//ScanAxisInfo[@AxisId='TwoTheta']")
        ]
        two_theta_stop = root.find(".//ScanAxisInfo[@AxisId='TwoTheta']")
        two_theta_stop_value = two_theta_stop.find("./Stop").text

    # Read file creation date/time
    ti_m = os.path.getmtime(input_file)
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ti_m))

    # Open file to write. Write individual lines
    f = open(output_file,"w+")
    f.write('# exported by project chameleon from a bruker brml file' + '\n')

    f.write('# FILE: ' + str(input_file) + '\n')
    f.write('# DATE_AND_TIME: ' + str(end_time) + '\n')

    f.write('# GENERATOR_CURRENT: ' + str(current_value) + '\n')
    f.write('# GENERATOR_VOLTAGE: ' + str(voltage_value) + '\n')
    f.write('# SCAN_TYPE: ' + str(scan_type) + '\n')
    f.write('# START_2THETA: ' + str(theta2_value) + '\n')
    f.write('# START_ANGLE: ' + str(theta2_value) + '\n')
    f.write('# START_BEAM_TRANSLATION: ' + str(virtual_position_value) + '\n')
    f.write('# START_PHI: ' + str(position_value) + '\n')
    f.write('# START_THETA: ' + str(theta_value) + '\n')
    f.write('# STEPS: ' + str(scan_steps) + '\n')
    f.write('# STEP_SIZE: ' + str(increment_value) + '\n')

    # If there is no VCT we only need to print 2 lines. If there is VCT we need to print a block for each subscan
    if len(subscan_data) <= 1:
        f.write('# TOTAL_TIME_PER_STEP: ' + str(subscan_data[0]["MeasuredTimePerStep"]) + '\n') # Total time
        f.write('# TIME_PER_STEP: ' + str(subscan_data[0]["PlannedTimePerStep"]) + '\n') # Time per step
    else:
        # Find start values
        two_theta_starts = [
            scan_axis.find("Start").text
            for scan_axis in root.findall(".//ScanAxisInfo[@AxisId='TwoTheta']")
        ]
        
        # Crop repeated start value, add end value
        two_theta_values = two_theta_starts[1:] + [two_theta_stop_value]

        # Create VCT blocks
        f.write('# # # VARIABLE_COUNT_TIME # # # ' + '\n')
        for i in range(len(two_theta_values) - 1):
            f.write('# SUB_SCAN_START: ' + str(two_theta_values[i]) + '\n')
            f.write('# SUB_SCAN_END: ' + str(two_theta_values[i + 1]) + '\n')
            f.write('# TOTAL_TIME_PER_STEP: ' + str(subscan_data[i]["MeasuredTimePerStep"]) + '\n')
            f.write('# TIME_PER_STEP: ' + str(subscan_data[i]["PlannedTimePerStep"]) + '\n')
            f.write('#' + '\n')

    # Write data
    f.write('# column_1	   column_2' + '\n')
    for row in string_array:
        f.write(str(row[2]) + '	           ' + str(row[4]) + '\n')
    f.close()

    # Remove directory, files aren't needed after data is extracted
    shutil.rmtree(extract_to)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    brml_converter(args.input, args.output)