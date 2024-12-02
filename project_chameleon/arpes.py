import os.path
import os
import re
import time
import htmdec_formats
import h5py
import subprocess
import traceback
import argparse
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from configparser import ParsingError
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import Border, Side
from openpyxl.styles import Font, Alignment
from PyQt5.QtWidgets import QApplication, QLabel, QTextEdit, QVBoxLayout, QWidget

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def build_arpes_workbook(workbook_name):
    """
    ``build_arpes_workbook`` is a function that creates an excel file with a specific premade format. This format is used to hold ARPES data. The function is primarily used to create a new workbook for data to be put into.

    :args: This function has one input: ``workbook_name``. ``workbook_name`` is a string or path.

    :return: Does not return anything. Creates an excel file with a premade format. 

    :exceptions: Will throw an exception if the input does not end with '.xlsx'.
    
    """
    #Error handling
    if not str(workbook_name).endswith('.xlsx'):
        raise ValueError("ERROR: workbook_name input must end with '.xlsx'")
    
    #Open the workbook
    wb = Workbook()
    ws = wb.active
    #Row labels, column values
    row_1 = ['Colored Labels','','','Colored Labels','Alignment Maps','Hi-Stat Map','"Good" High-Stat Scan','"Good" High-Stat Scan','Mono Lamp Change','Mono Lamp Change',
             'Slit Change','Slit Change','Theta Offset:','0','Phi Offset:','0','Omega Offset:','0']
    row_2 = ['Scan Number/File Name','Date','Time Start', 'Time End', 'Notes/Comments','FS Position','(X,Y,Z)','Theta(encoder)','Theta(true)','Phi(encoder)','Phi(true)',
             'Omega(Manipulator,approx)','Omega(true)','Kinetic Energy Range(eV)','Step Size(meV)','Temperature(K)[Diode A,Diode B]','Run Mode','Acquisition Mode',
             '[# of Sweeps, Layers]','Pass Energy','Analyzer Slit','Pressure(Torr)','Photon Energy(eV)']
    first_col = 1
    last_col = 28
    row_1_last_col = 19
    row_2_last_col = 24
    end_col = 14

    thin_border = Border(
        top=Side(style='thin'),
        bottom=Side(style='thin')
    ) 
    #Set column widths
    for col in range(first_col, last_col + 1):
        col_letter = get_column_letter(col)
        ws.column_dimensions[col_letter].width = 20
    #Set borders on cells
    for col in range(first_col, end_col + 1):
            cell = ws.cell(row=2, column=col)
            cell.border = thin_border
    #Put values in cells, make bold and centered. Column 1 then column 2
    for col in range(first_col, row_1_last_col):
        if row_1[col - 1] == '':
            continue
        else:
            cell = ws.cell(row=1, column=col)
            cell.value = row_1[col-1] 
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
    for col in range(first_col, row_2_last_col):
        cell = ws.cell(row=2, column=col)
        cell.value = row_2[col-1] 
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')
    #Set background colors
    fill_color1 = PatternFill(start_color="FFA07A", end_color="FFA07A", fill_type="solid")#Light orange
    fill_color2 = PatternFill(start_color="D8BFD8", end_color="D8BFD8", fill_type="solid")#Light purple
    fill_color3 = PatternFill(start_color="66CDAA", end_color="66CDAA", fill_type="solid")#Light green
    fill_color4 = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")#Light blue
    fill_color5 = PatternFill(start_color="FFFACD", end_color="FFFACD", fill_type="solid")#light yellow
    fill_color6 = PatternFill(start_color="FFB6C1", end_color="FFB6C1", fill_type="solid")#light red
    fill_grey = fill_color = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")
    #Merge cells
    ws.merge_cells('A1:B1')
    ws.merge_cells('G1:H1')
    ws.merge_cells('I1:J1')
    ws.merge_cells('K1:L1')
    ws.merge_cells('A3:A4')
    ws.merge_cells('B3:I4')
    #Apply colors to cells
    ws['E1'].fill = fill_color1
    ws['F1'].fill = fill_color2
    ws['G1'].fill = fill_color3
    ws['I1'].fill = fill_color4
    ws['K1'].fill = fill_color5
    ws['A5'].fill = fill_color6
    ws['M1'].fill = fill_grey
    #Aditional cells to be formated
    cell = ws['A3']
    cell.value = 'Initial Notes/Sample Information'
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell = ws['A5']
    cell.value = 'Initial Start:'
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    #Save and close workbook
    wb.save(workbook_name)

def get_wavenote_values(wavenote_file):
    """
    ``get_wavenote_values`` is a function that extracts values from the wave note of the .pxt file using HTMDEC. This function does not extract all values. It extracts file name, date, start time, end time, comments, theta, phi, kinetic energy range, step size, run mode, acquisition mode, # of sweeps, pass energy, and photon energy.

    :args: This function has one input: ``wavenote_file``. ``wavenote_file`` is a string or path.

    :return: Returns an array that holds values from the wave note of the .pxt file.

    :exceptions: Will throw an exception if the input does not end with '.pxt'.
    
    """
    #Initialization and error handling
    if not wavenote_file.endswith('.pxt'):
        raise ValueError("ERROR: input file must end with '.pxt'")
    if os.path.isfile(wavenote_file) is False:
        raise ValueError("ERROR: bad input. Expected file")

    lines = []

    #Get date modified from wavenote file for the end time 
    ti_m = os.path.getmtime(wavenote_file)
    m_ti = time.ctime(ti_m) 
    if ':' in m_ti.split(' ')[3]:
        end_time = m_ti.split(' ')[3]
    else:
        end_time = m_ti.split(' ')[4]
    #Read .pxt, write to file, read lines from file, split up lines for relevant data
    try:
        dataset = htmdec_formats.ARPESDataset.from_file(wavenote_file)
        lines = dataset._metadata.split("\n")
        lines[20] = lines[20].split('\\')
        for l in lines[20]:
            if '.pxt' in l:
                scan_number = l
        if lines[35]:
            scan_type = 'Add Dimension'
        elif len(dataset.run_mode_info) > 0:
            scan_type = 'Manipulator Scan'
        else:
            scan_type = 'Normal Mode'
            
    #[File, Start Date, Start Time, End Time, Comments, Kinetic Energy Range, Step Size, Run Mode, Acquisition Mode, # of sweeps, Pass Energy, Photon Energy]
        r =[scan_number,lines[28].split('=')[1],lines[29].split('=')[1],end_time, lines[27].split('=')[1],
        '[' + lines[11].split('=')[1] + ',' + lines[12].split('=')[1] + ']',lines[13].split('=')[1],
        scan_type,lines[8].split('=')[1], '[' + lines[5].split('=')[1] + ',' + str(dataset.num_layers) + ']',lines[4].split('=')[1],lines[6].split('=')[1]]
        return r
    except ParsingError as e:
        print(f"An error occurred while parsing the configuration: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"An unexpected error occurred in get_wavenote_values: {e}")
        traceback.print_exc()



def get_varian_values(varian_file, date_time = None):
    """
    ``get_varian_values`` is a function that extracts values from the varian .log file. This function does not extract all values. It extracts (x,y,z), theta, phi, analyzer slit.

    :args: This function has two inputs: ``varian_file`` and ``date_time``. ``varian_file`` is a string or path.``date_time`` is an array that only holds a date and a time.

    :return: Returns an array that holds values from the varian file.

    :exceptions: Will throw an exception if the input does not end with '.log'.
    
    """
    #Initialization and error handling
    if not varian_file.endswith('.log'):
        raise ValueError("ERROR: input file must end with '.log'")
    if os.path.isfile(varian_file) is False:
        raise ValueError("ERROR: bad input. Expected file")
    
    varian_lines = []
    time_found = 0

    #Make sure the date in date_time matches the date of the log file. If not, find the log file that does match
    if date_time:
        varian_folder = os.listdir(os.path.dirname(varian_file))
        #Make dates the same format
        if '/' in varian_file:
            varian_name = varian_file.split('/')[-1].split('.')[0]
        else: 
            varian_name = varian_file.split('.')[0]
        varian_name = varian_name.replace('-','/')
        if varian_name != date_time[0]:
            for item in varian_folder:
                if '.log' in item:
                    if item.split('.')[0].replace('-','/') == date_time[0]:
                        varian_file = os.path.join(os.path.dirname(varian_file), item)
                        break
                    else:
                        continue
                        
    #Open log, read lines
    with open(varian_file, 'r') as file:
        varian_lines = file.readlines()
    varian_lines = varian_lines[1:]
    #If time is given, align varian values to time, otherwise take first row
    if date_time == None:
        #[(x,y,z),Theta,Phi,Analyzer Slit](Theta and Phi no longer used)
        return ['(' + str(Decimal(varian_lines[1].replace(' ','').replace('\n','').split("\t")[2]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ',' + 
                        str(Decimal(varian_lines[1].replace(' ','').replace('\n','').split("\t")[4]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ',' + 
                        str(Decimal(varian_lines[1].replace(' ','').replace('\n','').split("\t")[6]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ')',
                        varian_lines[1].replace(' ','').replace('\n','').split("\t")[8],varian_lines[1].replace(' ','').replace('\n','').split("\t")[10],
                        varian_lines[1].replace(' ','').replace('\n','').split("\t")[14]]
    else:
        while time_found < 1:
            length = len(varian_lines)
            #Once length is 5 or less just look through all the items. Should avoid missing on edge cases
            if length <= 5:
                if length == 0:
                    raise ValueError("ERROR: Error in varian log file. Time cannot be found")
                for item in varian_lines:
                    if (get_sec(date_time[1]) >= get_sec(item.replace(' ','').replace('\n','').split("\t")[0][10:18]) - 30) and (get_sec(date_time[1]) <= get_sec(item.replace(' ','').replace('\n','').split("\t")[0][10:18]) + 30):
                        return ['(' + str(Decimal(item.replace(' ','').replace('\n','').split("\t")[2]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ',' + 
                        str(Decimal(item.replace(' ','').replace('\n','').split("\t")[4]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ',' + 
                        str(Decimal(item.replace(' ','').replace('\n','').split("\t")[6]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ')',
                        item.replace(' ','').replace('\n','').split("\t")[8],item.replace(' ','').replace('\n','').split("\t")[10],
                        item.replace(' ','').replace('\n','').split("\t")[14]]
            middle = length // 2
            if (get_sec(date_time[1]) > get_sec(varian_lines[middle].replace(' ','').replace('\n','').split("\t")[0][10:18]) + 30): 
                #If the time is more than 30 seconds greater than the middle, take higher half of array
                varian_lines = varian_lines[middle:]
            elif (get_sec(date_time[1]) < get_sec(varian_lines[middle].replace(' ','').replace('\n','').split("\t")[0][10:18]) - 30):
                #If the time is more than 30 seconds less than the middle, take lower half of array
                varian_lines = varian_lines[:middle]
            elif (get_sec(date_time[1]) >= get_sec(varian_lines[middle].replace(' ','').replace('\n','').split("\t")[0][10:18]) - 30) and (get_sec(date_time[1]) <= get_sec(varian_lines[middle].replace(' ','').replace('\n','').split("\t")[0][10:18]) + 30):
                return ['(' + str(Decimal(varian_lines[middle].replace(' ','').replace('\n','').split("\t")[2]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ',' + 
                        str(Decimal(varian_lines[middle].replace(' ','').replace('\n','').split("\t")[4]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ',' + 
                        str(Decimal(varian_lines[middle].replace(' ','').replace('\n','').split("\t")[6]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ')',
                        varian_lines[middle].replace(' ','').replace('\n','').split("\t")[8],varian_lines[middle].replace(' ','').replace('\n','').split("\t")[10],
                        varian_lines[middle].replace(' ','').replace('\n','').split("\t")[14]]



def get_jaina_values(jaina_file, date_time = None):
    """
    ``get_jaina_values`` is a function that extracts values from the jaina .log file. This function does not extract all values. It extracts temperature(Diode A,Diode B) and pressure.

    :args: This function has two inputs: ``jaina_file`` and ``date_time``. ``jaina_file`` is a string or path.``date_time`` is an array that only holds a date and a time.

    :return: Returns an array that holds values from the jaina file.

    :exceptions: Will throw an exception if the input does not end with '.log'.
    
    """
    #Initialization and error handling
    if not jaina_file.endswith('.log'):
        raise ValueError("ERROR: input file must end with '.log'")
    if os.path.isfile(jaina_file) is False:
        raise ValueError("ERROR: bad input. Expected file")
    
    jaina_lines = []
    time_found = 0
    
    #Make sure the date in date_time matches the date of the log file. If not, find the log file that does match
    if date_time:
        jaina_folder = os.listdir(os.path.dirname(jaina_file))
        if '/' in jaina_file:
            jaina_name = jaina_file.split('/')[-1].split('.')[0]
        else: 
            jaina_name = jaina_file.split('.')[0]
        jaina_name = jaina_name.replace('-','/')
        if jaina_name != date_time[0]:
            for item in jaina_folder:
                if '.log' in item:
                    if item.split('.')[0].replace('-','/') == date_time[0]:
                        jaina_file = os.path.join(os.path.dirname(jaina_file), item)
                        break
                    else:
                        continue

    with open(jaina_file, 'r') as file:
        jaina_lines = file.readlines()
    jaina_lines = jaina_lines[1:]
    #If time is given, align varian values to time, otherwise take first row
    if date_time == None:
        #[(Diode A,Diode B), Pressure]
        return ['[' + jaina_lines[1].replace(' ','').replace('\n','').split("\t")[1] + ',' + jaina_lines[1].replace(' ','').replace('\n','').split("\t")[2] + ']',jaina_lines[1].replace(' ','').replace('\n','').split("\t")[14]]
    else:
        #Binary search method to find the time closest to the time submitted in date_time
        while time_found < 1:
            length = len(jaina_lines)
            #Once length is 5 or less just look through all the items. Should avoid missing on edge cases
            if length <= 5:
                if length == 0:
                    raise ValueError("ERROR: Error in jaina log file. Time cannot be found")
                for item in jaina_lines:
                    if (get_sec(date_time[1]) >= get_sec(item.replace(' ','').replace('\n','').split("\t")[0][10:18]) - 30) and (get_sec(date_time[1]) <= get_sec(item.replace(' ','').replace('\n','').split("\t")[0][10:18]) + 30):
                        return ['[' + item.replace(' ','').replace('\n','').split("\t")[1] + ',' + 
                                item.replace(' ','').replace('\n','').split("\t")[2] + ']',item.replace(' ','').replace('\n','').split("\t")[14]]
            middle = length // 2
            if (get_sec(date_time[1]) > get_sec(jaina_lines[middle].replace(' ','').replace('\n','').split("\t")[0][10:18]) + 30): 
                #If the time is more than 30 seconds greater than the middle, take higher half of array
                jaina_lines = jaina_lines[middle:]
            elif (get_sec(date_time[1]) < get_sec(jaina_lines[middle].replace(' ','').replace('\n','').split("\t")[0][10:18]) - 30):
                #If the time is more than 30 seconds less than the middle, take lower half of array
                jaina_lines = jaina_lines[:middle]
            elif (get_sec(date_time[1]) >= get_sec(jaina_lines[middle].replace(' ','').replace('\n','').split("\t")[0][10:18]) - 30) and (get_sec(date_time[1]) <= get_sec(jaina_lines[middle].replace(' ','').replace('\n','').split("\t")[0][10:18]) + 30):
                return ['[' + jaina_lines[middle].replace(' ','').replace('\n','').split("\t")[1] + ',' + jaina_lines[middle].replace(' ','').replace('\n','').split("\t")[2] + ']',jaina_lines[middle].replace(' ','').replace('\n','').split("\t")[14]]

def insert_scan_row(wavenote_file,jaina_file,varian_file,workbook_name):
    """
    ``insert_scan_row`` is a function that extracts values from a .pxt wave note file, a jaina log file, a varian log file, and inserts all of the values into the first open row of the workbook ``workbook_name``.

    :args: This function has four inputs: ``wavenote_file``,``jaina_file``,``varian_file``, and ``workbook_name``. ``wavenote_file`` is a string or a path. ``jaina_file`` is a string or path. ``varian_file`` is a string or a path. ``workbook_name`` is a string or a path.

    :return: Does not return anything. Inserts values into the workbook ``workbook_name``.

    :exceptions: Will throw an exception if the input ``wavenote_file`` does not end with '.pxt'. Will throw an exception if the input ``jaina_file`` does not end with '.log'. Will throw an exception if the input ``varian_file`` does not end with '.log'. Will throw an exception if the input ``workbook_name`` does not end with '.xlsx'.
    
    """
    #Initialization and error handling
    if not str(workbook_name).endswith('.xlsx'):
        raise ValueError("ERROR: workbook_name input must end with '.xlsx'")
    if not jaina_file.endswith('.log'):
        raise ValueError("ERROR: jaina_file must end with '.log'")
    if not varian_file.endswith('.log'):
        raise ValueError("ERROR: varian_file must end with '.log'")
    if not wavenote_file.endswith('.pxt'):
        raise ValueError("ERROR: wavenote_file must end with '.pxt'")

    first_col = 1
    last_col = 24
    starting_row = 6
    starting_cell = 0
    #Read wavenote, extract start and end time for jaina,varian if wavenote does not return error
    w = get_wavenote_values(wavenote_file)
    if w != None:
        date = w[1]
        time = w[2]
        date = date.replace('-','/').replace('\n','').replace('\n','')
        time = time.replace('\n','')
        j = get_jaina_values(jaina_file,[date,time])
        v = get_varian_values(varian_file,[date,time])
    #Make the workbook and open it
    wb = wb = load_workbook(filename = workbook_name)
    ws = wb.active
    #Find first open row
    while starting_cell == 0:
        cell = ws.cell(row=starting_row, column=first_col)
        if not cell.value:
            starting_cell = 1
        else:
            starting_row += 1
    #Make the row "Error" if wavenote cant be read
    if w == None:
        ws.row_dimensions[starting_row].height = 40
        for col in range(first_col, last_col):
            cell = ws.cell(row=starting_row, column=1)
            cell.value = 'Error' 
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center',wrapText=True)
    else:
        #[Scan, Date, Start time, End time, Notes/Comments, '', (X,Y,Z), Theta, '', Phi, '', '', '', Kinetic Energy, Step size, Temp[A,B], Run mode, Acquisition mode,
        # # of sweeps, Pass energy, Analyzer slit, Pressure, Photon Energy]
        row = [w[0],w[1],w[2],w[3],w[4],'',v[0],v[1],'',v[2],'','','',w[5],w[6],j[0],w[7],w[8],w[9],w[10],v[3],j[1],w[11]]
        #Insert values into rows
        ws.row_dimensions[starting_row].height = 40
        for col in range(first_col, last_col):
            #For the notes column make the font smaller
            if col == 5:
                cell = ws.cell(row=starting_row, column=col)
                cell.value = row[col-1] 
                cell.font = Font(bold=False, size = 8)
                cell.alignment = Alignment(horizontal='center', vertical='center',wrapText=True)
            else:
                cell = ws.cell(row=starting_row, column=col)
                cell.value = row[col-1] 
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center',wrapText=True)
    #Close workbook
    wb.save(workbook_name)

def arpes_folder_workbook(folder_name, workbook_name):
    """
    ``arpes_folder_workbook`` is a function that creates a workbook, looks through the folder to see how many scans there are, extracts values from .pxt, jaina, and varian files for each scan, and creates a row with the extracted values for each scan. This function calls build_arpes_workbook and insert_scan_row.

    :args: This function has two inputs: ``folder_name`` and ``workbook_name``. ``folder_name`` is a string or a path. ``workbook_name`` is a string or a path.

    :return: Does not return anything. Creates a workbook will a row for each .pxt file in the folder.

    :exceptions: Will throw an exception if the input``folder_name`` is not a directory. Will throw an exception if the input ``workbook_name`` does not end with '.xlsx'.
    
    """
    #Initialization and error handling
    if not os.path.isdir(folder_name):
        raise ValueError("ERROR: folder_name input must be a directory")
    if os.listdir(folder_name) == 0:
        raise ValueError("ERROR: bad input. Data folder should contain files")
    if not str(workbook_name).endswith('.xlsx'):
        raise ValueError("ERROR: workbook_name input must end with '.xlsx'")

    jaina_logs = []
    varian_logs = []
    #Set directory paths based on directory structure, get all files from directories
    wavenote_directory = folder_name + '/'
    jaina_directory = folder_name + '/../../../.././ARPES Log Data/Jaina Cadillac/'
    varian_directory = folder_name + '/../../../.././ARPES Log Data/Varian Cadillac/'
    wavenote_names = os.listdir(wavenote_directory)
    jaina_names = os.listdir(jaina_directory)
    varian_names = os.listdir(varian_directory)
    #Organize .pxt files to be in the correct order
    for name in wavenote_names:
        if not '.pxt' in name:
            wavenote_names.remove(name)
    sorted_waves = sorted(
        wavenote_names,
        key=lambda x: float(re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", x)[-1]) if re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", x) else 0
        )   
    #Make sure files in directories are just the files we want
    for f in jaina_names:
        if f.endswith('.log'):
            jaina_logs = jaina_logs + [jaina_directory + f]
    for f in varian_names:
        if f.endswith('.log'):
            varian_logs = varian_logs + [varian_directory + f]
    #Build the workbook
    build_arpes_workbook(workbook_name)
    #Insert rows into workbook
    for f in sorted_waves:
        if f.endswith('.pxt'):
            insert_scan_row(wavenote_directory + f,jaina_logs[0],varian_logs[0],workbook_name)
    

def single_log_grapher(log_file, scan_folder, log_type, value):
    """
    ``single_log_grapher`` is a function that take a single Varian or Jaina log file from an ARPES scan folder and plots it. The entire log time is graphed and the individual ARPES scans are represented by the different color segements in the plot.

    :args: This function has four inputs: ``log_file``, ``scan_folder``,``log_type`, and ``value``. ``log_file`` is a string or a path to the log file that will be graphed. ``scan_folder`` is a string or a path to the folder that contains the scans that happen during the log time.``log_type`` is a string that is either Varian or Jaina.``value`` is a string that is the log value that will be graphed.
    
    :return: Does not return anything. Displays, plots, and creates a .png file of the plot.
    
    :exceptions: Will throw an exception if the input``log_file`` is not a .log file. Will throw an exception if the input ``scan_folder`` is not a directory. Will throw an exception if the input ``log_type`` is not a valid log type. Will throw an exception if the input ``value`` is not a valid value.
    """

    if not log_file.endswith('.log'):
        raise ValueError("ERROR: log file must end with '.log'")
    if os.path.isfile(log_file) is False:
        raise ValueError("ERROR: bad input. Expected file")
    if not os.path.isdir(scan_folder):
        raise ValueError("ERROR: scan folder must be a folder")
    if os.listdir(scan_folder) == 0:
        raise ValueError("ERROR: bad input. Data folder should contain files")
    if log_type.lower() != 'jaina' and log_type.lower() != 'varian':
        raise ValueError("ERROR: Log type must be Jaina or Varian")
    if not (value in jaina_values or value in varian_values):
        raise ValueError("ERROR: Value must be a Jaina or Varian value")

    value_index = 0
    log_lines = []  
    colors = ['red', 'blue', 'orange', 'green', 'purple', 'yellow', 'brown', 'pink', 'light blue', 'beige', 'light green']
    jaina_values = ['Timestamp', 'DiodeA', 'DiodeB', 'Heater', 'HeaterSetPoint', 'HeaterRange', 'OutputMode', 'RampMode', 'RampRate', 
                    'ZoneRampRate', 'CryoTemp', 'CryoLSetPt', 'CryoHSetPt', 'IG_Val', 'ARPES_IG', 'ARPES_PG1', 'ARPES_PG2', 
                    'Mono_IG', 'Mono_PG1', 'Mono_PG2', 'SD_IG', 'SD_PG1', 'SD_PG2', 'TC_IG', 'TC_PG1', 'TC_PG2']
    varian_values = ['Timestamp', 'X_status', 'X', 'Y_status', 'Y', 'Z_status', 'Z', 'Theta_status', 'Theta', 'Phi_status', 
                     'Phi', 'Omega', 'ManipLimitCheck', 'ManipSES', 'ARPES_Slit']
    
    #Assign the right type of variables based on the file type
    if log_type.lower() == 'jaina':
        values = jaina_values
    elif log_type.lower() == 'varian':
        values = varian_values
    else:
        raise ValueError("Invalid log type")

    # Find value index so we know which value we are graphing
    for i, item in enumerate(values):
        if item == value:
            value_index = i
            break
    else:
        raise ValueError(f"Value '{value}' not found in log type '{log_type}'")

    with open(log_file, 'r') as file:
        log_lines = file.readlines()

    # Extracting value data and time data
    value_data = [line.split()[value_index + 1] for line in log_lines]  # Assuming space-separated logs
    time_data = [line.split()[1] for line in log_lines[1:]]  # Assuming 'Timestamp' is first column
    # Convert time data to seconds
    new_time = [get_sec(item) for item in time_data if item]
    length = len(log_lines) - 2
    log_start_date = log_lines[1].split()[0][:10]
    log_end_date = log_lines[length].split()[0][:10]
    adjusted_log_start_date = log_start_date[6:10] + '-' + log_start_date[0:2] + '-' + log_start_date[3:5]
    adjusted_log_end_date = log_end_date[6:10] + '-' + log_end_date[0:2] + '-' + log_end_date[3:5]

    # Filter .pxt files
    waves = [os.path.join(scan_folder, name) for name in os.listdir(scan_folder) if name.endswith('.pxt')]

    segment_times = []

    for item in waves:
        try:
            end_time = os.path.getmtime(item)
            scan_end = datetime.fromtimestamp(end_time)
            dataset = htmdec_formats.ARPESDataset.from_file(item)
            
            log_file_path = os.path.join(os.path.dirname(item), "log_data_holder.txt")
            with open(log_file_path, "w") as f:
                f.write(dataset._metadata)
            f.close()
            with open(log_file_path, 'r') as file:
                lines = file.readlines()
            os.remove(log_file_path)

            # Start date, start time, [End data, end time]
            scan_end_str = scan_end.strftime('%Y-%m-%d %H:%M:%S')
            scan_times = [lines[28].split('=')[1].strip(), lines[29].split('=')[1].strip(), scan_end_str.split(' ')]

            # Handle segment times
            if scan_times[0] == adjusted_log_start_date and scan_times[2][0] == adjusted_log_end_date:
                segment_times.append((scan_times[1], scan_times[2][1]))
            elif scan_times[0] == adjusted_log_start_date:
                segment_times.append((scan_times[1], '23:59:59'))
            elif scan_times[2][0] == adjusted_log_end_date:
                segment_times.append(('00:00:01', scan_times[2][1]))
                
        except Exception as e:
            print(f"An unexpected error occurred in single log grapher item loop: {e}")
    
    # Convert time and value data into numpy arrays
    x_values = np.array(new_time) / 3600
    y_values = np.array(value_data[1:], dtype=float)  # Ensure y_values are all numeric
    
    previous_end_time = None
    first_start_time = get_sec(segment_times[0][0]) / 3600
    if x_values[0] < first_start_time:
        # There is a gap before the first segment
        gap_mask = (x_values < first_start_time)
        plt.plot(x_values[gap_mask], y_values[gap_mask], linestyle='-', color='grey', label='Initial Gap')
        plt.scatter(x_values[gap_mask], y_values[gap_mask], color='grey', edgecolor='grey')

    for i, (start_time, end_time) in enumerate(segment_times):
        start_sec = get_sec(start_time) / 3600
        end_sec = get_sec(end_time) / 3600

        if previous_end_time is not None and start_sec > previous_end_time:
            gap_mask = (x_values > previous_end_time) & (x_values < start_sec)
            plt.plot(x_values[gap_mask], y_values[gap_mask], linestyle='-', color='grey', label='Gap')
            plt.scatter(x_values[gap_mask], y_values[gap_mask], color='grey', edgecolor='grey')

        segment_mask = (x_values >= start_sec) & (x_values <= end_sec)
        x_segment = x_values[segment_mask]
        y_segment = y_values[segment_mask]

        plt.plot(x_segment, y_segment, linestyle='-', color=colors[i], label=f'Scan {i+1}')
        plt.scatter(x_segment, y_segment, color=colors[i], edgecolor=colors[i])

        previous_end_time = end_sec

    # Final segment for values greater than the last end time
    final_mask = x_values >= get_sec(segment_times[-1][1]) / 3600
    x_segment = x_values[final_mask]
    y_segment = y_values[final_mask]

    # Plot legend and save the figure
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.xlabel('Time (hours)')
    plt.ylabel('Y Values')
    
    plt.savefig('plot.png', bbox_inches='tight', dpi=500)
    plt.show()

def arpes_previewer(pxt_file):
    """
    ``previewer`` is a function that takes a pxt file as an input and displays the data and metadata from that file.

    :args: This function has one input: ``pxt_file``. ``pxt_file`` is an ARPES .pxt file that contains data from an ARPES scan.

    :return: Does not return anything. Displays data and metadata from the file.

    :exceptions: Will throw an exception if the input``pxt_file`` is not a .pxt file.
    """

    if not pxt_file.endswith('.pxt'):
        raise ValueError("ERROR: input file must end with '.pxt'")
    if os.path.isfile(pxt_file) is False:
        raise ValueError("ERROR: bad input. Expected file")
    if os.path.getsize(pxt_file) < 10:
        raise ValueError("ERROR: This size of file cannot be handled by this function. File too small.")

    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    command = [
        "htmdec-formats", 
        "pxt-to-hdf5", 
        pxt_file, 
        "data_holder.hdf5"
    ]
    # Execute the command
    subprocess.run(command, check=True)
    filename = "data_holder.hdf5"
    with h5py.File(filename, "r") as f:
        a_group_key = list(f.keys())[0]
        data = list(f[a_group_key])
        data = list(f[a_group_key])
        array = np.array(data)
        dimensions = array.shape
        ds_obj = f[a_group_key]      # returns as a h5py dataset object
        ds_arr = f[a_group_key][()]  # returns as a numpy array
    ds_arr = np.squeeze(ds_arr)
    os.remove(filename)
    plt.imshow(ds_arr, cmap='gray', interpolation='nearest')
    plt.title('Greyscale Intensity Map')
    plt.show()

    dataset = htmdec_formats.ARPESDataset.from_file(pxt_file)
    log_file_path = os.path.join(os.path.dirname(pxt_file), "log_data_holder.txt")
    with open(log_file_path, "w") as f:
        f.write(dataset._metadata)
    f.close()
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
    os.remove(log_file_path)

    display_label = pxt_file.split('/')
    if len(display_label) > 1:
        final_label = display_label[-1]
    else:
        final_label = display_label
    label = QLabel(final_label + ' Metadata')
    # Create a QTextEdit for displaying multi-line text
    text_edit = QTextEdit()
    text_edit.setPlainText(''.join(lines))  # Join list of lines into a single string
    # Add widgets to layout
    layout.addWidget(label)
    layout.addWidget(text_edit)
    window.setLayout(layout)
    # Show the window
    window.show()
    app.exec_()

def main():
    parser = argparse.ArgumentParser(description="Process some input files for background and sample data")
    parser.add_argument("folder_name", help="the input file for the background data")
    parser.add_argument("workbook_name", help="the input file for the sample data")
    args = parser.parse_args()
    arpes_folder_workbook(args.folder_name, args.workbook_name)

if __name__ == "__main__":
    main()