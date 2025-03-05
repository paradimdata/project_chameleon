from datetime import datetime
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import argparse
import zipfile
import shutil
import time
import pytz
import os
import re

def convert_to_datetime(timestamp):
    timestamp = re.sub(r"(\.\d{6})\d+", r"\1", timestamp)  # Trim to 6 decimal places
    dt = datetime.fromisoformat(timestamp)
    est = pytz.timezone("US/Eastern")
    return dt.astimezone(est).strftime("%Y-%m-%d %H:%M:%S")

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

    namespaces = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

    # Bruker brml files can be treated like zip files. Here ZipFile is used to extract data from compressed to readable format. Data is put into a folder called 'holder'. Within the folder, there are a series of .xml files holding data and metadata.
    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # Establish .xml file strucutre
    tree = ET.parse(extract_to + '/Experiment0/RawData0.xml')
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

    bsml_file_element = root.findall(".//InfoItem[@Name='BsmlFileName']")
    bsml_filepath = bsml_file_element[0].attrib.get('Value')
    bsml_file = bsml_filepath.split("\\")[-1] # BSML file name

    goniometer_radius_element = root.findall(".//Radius")
    goniometer_radius_value = goniometer_radius_element[0].attrib.get('Value') # Goniometer radius

    rotation_speed_element = root.findall(".//RotationSpeed")
    rotation_speed_value = rotation_speed_element[0].attrib.get('Value') # Sample rotation

    tube_material_element = root.findall(".//TubeMaterial")
    tube_material_value = tube_material_element[0].text # Anode 

    wavelength_alpha1_element = root.findall(".//WaveLengthAlpha1")
    wavelength_alpha1_value = wavelength_alpha1_element[0].attrib.get('Value') # ka1

    wavelength_alpha2_element = root.findall(".//WaveLengthAlpha2")
    wavelength_alpha2_value = wavelength_alpha2_element[0].attrib.get('Value') # ka2

    lower_discriminator_element = root.findall(".//LowerDiscriminator")
    lower_discriminator_value = lower_discriminator_element[0].attrib.get('Value') # Lower discriminator value

    upper_discriminator_element = root.findall(".//UpperDiscriminator")
    upper_discriminator_value = upper_discriminator_element[0].attrib.get('Value') # Upper discriminator value

    axial_divergence_element = root.find(".//InfoData[@xsi:type='SollerInfoData']/AxialDivergence", namespaces)
    axial_divergence_value = axial_divergence_element.attrib.get("Value") # Primary soller
 
    secondary_axial_divergence = root.find(".//SecondaryTracks//InfoData[@xsi:type='SollerInfoData']/AxialDivergence", namespaces)
    if secondary_axial_divergence is not None:
        secondary_axial_divergence_value = secondary_axial_divergence.attrib.get("Value") # Secondary soller (does not exist in all scans)

    time_started = convert_to_datetime(root.find("TimeStampStarted").text) # Start time
    time_finished = convert_to_datetime(root.find("TimeStampFinished").text) # End time

    # Find all SubScanInfo elements
    subscan_infos = root.findall(".//SubScanInfo")

    # Extract and store MeasuredTimePerStep and PlannedTimePerStep values
    subscan_data = [
        {
            "MeasuredTimePerStep": subscan.get("MeasuredTimePerStep"),
            "PlannedTimePerStep": subscan.get("PlannedTimePerStep"),
            "Steps": subscan.get("Steps")
        }
        for subscan in subscan_infos
    ]

    # If there are multiple scans, get TwoTheta value
    if len(subscan_data) > 1:
        two_theta_starts = [
            scan_axis.find("Start").text
            for scan_axis in root.findall(".//ScanAxisInfo[@AxisId='TwoTheta']")
        ]

    # Generate text time to hold data. Block to present data in a more organized fashion
    f = open(output_file,"w+")
    f.write('# exported by project chameleon from a bruker brml file' + '\n')
    f.write('#' + '\n')

    f.write('# # # INSTRUMENT_PARAMETERS # # # ' + '\n')
    f.write('# ANODE: ' + str(tube_material_value) + '\n')
    f.write('# kα1: ' + str(wavelength_alpha1_value) + '\n')
    f.write('# kα2: ' + str(wavelength_alpha2_value) + '\n')
    f.write('# LOWER_DISCRIMINATOR_VALUE: ' + str(lower_discriminator_value) + '\n')
    f.write('# UPPER_DISCRIMINATOR_VALUE: ' + str(upper_discriminator_value) + '\n')
    f.write('# GENERATOR_CURRENT: ' + str(current_value) + '\n')
    f.write('# GENERATOR_VOLTAGE: ' + str(voltage_value) + '\n')
    f.write('#' + '\n')

    f.write('# # # STAGE_PARAMETERS # # # ' + '\n')
    f.write('# GONIOMETER_RADIUS: ' + str(goniometer_radius_value) + '\n')
    f.write('# SAMPLE_ROTATION: ' + str(rotation_speed_value) + '\n')
    f.write('# PRIMARY_SOLLER_SLIT: ' + str(axial_divergence_value) + '\n')
    if secondary_axial_divergence is not None: # Only print secondary soller if it exists
        f.write('# SECONDARY_SOLLER_SLIT: ' + str(secondary_axial_divergence_value) + '\n')
    f.write('#' + '\n')

    f.write('# # # SCAN_PARAMETERS # # # ' + '\n')
    f.write('# BRML_FILE: ' + str(input_file) + '\n')
    f.write('# BSML_FILE: ' + str(bsml_file) + '\n')
    f.write('# START_TIME: ' + str(time_started) + '\n')
    f.write('# END_TIME: ' + str(time_finished) + '\n')
    f.write('# SCAN_TYPE: ' + str(scan_type) + '\n')
    f.write('# START_2THETA: ' + str(theta2_value) + '\n')
    f.write('# START_ANGLE: ' + str(theta2_value) + '\n')
    f.write('# START_BEAM_TRANSLATION: ' + str(virtual_position_value) + '\n')
    f.write('# START_PHI: ' + str(position_value) + '\n')
    f.write('# START_THETA: ' + str(theta_value) + '\n')
    if len(subscan_data) <= 1: # If there is only one scan, print steps
        f.write('# STEPS: ' + str(scan_steps) + '\n')
    else: # If there are multiple scans, print steps and step sizes for all scans
        scan_steps = 0
        for i in range(len(subscan_data)):
            scan_steps = scan_steps + int(subscan_data[i]["Steps"])
        f.write('# STEPS: ' + str(scan_steps) + '\n')
    f.write('# STEP_SIZE: ' + str(increment_value) + '\n')

    if len(subscan_data) <= 1: # If there is one scan, print only time measurements
        f.write('# TOTAL_TIME_PER_STEP: ' + str(subscan_data[0]["MeasuredTimePerStep"]) + '\n')
        f.write('# TIME_PER_STEP: ' + str(subscan_data[0]["PlannedTimePerStep"]) + '\n')
    else: # If there are multiple scans, print variable time measurements for each scan
        f.write('#' + '\n')
        two_theta_starts = [
            scan_axis.find("Start").text
            for scan_axis in root.findall(".//ScanAxisInfo[@AxisId='TwoTheta']")
        ]
        two_theta_stop = root.find(".//ScanAxisInfo[@AxisId='TwoTheta']")
        two_theta_stop_value = two_theta_stop.find("./Stop").text
        
        two_theta_values = two_theta_starts[1:] + [two_theta_stop_value]

        f.write('# # # VARIABLE_COUNT_TIME # # # ' + '\n')
        for i in range(len(two_theta_values) - 1):
            f.write('# SUB_SCAN_START: ' + str(two_theta_values[i]) + '\n')
            f.write('# SUB_SCAN_END: ' + str(two_theta_values[i + 1]) + '\n')
            f.write('# TOTAL_TIME_PER_STEP: ' + str(subscan_data[i]["MeasuredTimePerStep"]) + '\n')
            f.write('# TIME_PER_STEP: ' + str(subscan_data[i]["PlannedTimePerStep"]) + '\n')
            f.write('#' + '\n')

    # Print data
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