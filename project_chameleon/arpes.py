import os.path
import os
import time
import htmdec_formats
from decimal import Decimal, ROUND_HALF_UP
from configparser import ParsingError
from pandas import DataFrame
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import Border, Side
from openpyxl.styles import Font, Alignment

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
    if not workbook_name.endswith('.xlsx'):
        raise ValueError("ERROR: workbook_name input must end with '.xlsx'")
    #Open the workbook
    wb = Workbook()
    ws = wb.active
    #Row labels, column values
    row_1 = ['Colored Labels','','','Colored Labels','Alignment Maps','Hi-Stat Map','"Good" High-Stat Scan','"Good" High-Stat Scan','Mono Lamp Change','Mono Lamp Change',
             'Slit Change','Slit Change','Theta Offset:','0','Phi Offset:','0','Omega Offset:','0']
    row_2 = ['Scan Number/File Name','Date','Time Start', 'Time End', 'Notes/Comments','FS Position','(X,Y,Z)','Theta(encoder)','Theta(true)','Phi(encoder)','Phi(true)',
             'Omega(Manipulator,approx)','Omega(true)','Kinetic Energy Range(eV)','Step Size(meV)','Temperature(K)[Diode A,Diode B]','Run Mode','Acquisition Mode',
             '# of Sweeps','Pass Energy','Analyzer Slit','Pressure(Torr)','Photon Energy(eV)']
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
        if row_1[col] == '':
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
    lines = []
    if not wavenote_file.endswith('.pxt'):
        raise ValueError("ERROR: input file must end with '.pxt'")
    #Create new file to hold output from HTMDEC 
    data_file = os.path.join(os.path.dirname(wavenote_file), "data_holder.txt")
    #Get date modified from wavenote file for the end time 
    ti_m = os.path.getmtime(wavenote_file)
    m_ti = time.ctime(ti_m) 
    #Read .pxt, write to file, read lines from file, split up lines for relevant data
    try:
        dataset = htmdec_formats.ARPESDataset.from_file(wavenote_file)
        with open(data_file, "w") as f:
            l = f.write(dataset._metadata)
        with open(data_file, 'r') as file:
            lines = file.readlines()
        lines[20] = lines[20].split('\\')
        for l in lines[20]:
            if '.pxt' in l:
                scan_number = l
                #[File, Date, Start Time, End Time, Comments, Theta, Phi, Kinetic Energy Range, Step Size, Run Mode, Acquisition Mode, # of sweeps, Pass Energy, Photon Energy]
        return [scan_number,lines[28].split('=')[1],lines[29].split('=')[1],m_ti.split(' ')[4], lines[27].split('=')[1],
                lines[40].split('=')[1], lines[41].split('=')[1],'[' + lines[11].split('=')[1] + ',' + lines[12].split('=')[1] + ']',lines[13].split('=')[1],
                lines[35],lines[8].split('=')[1], lines[5].split('=')[1],lines[4].split('=')[1],lines[6].split('=')[1]]
    except ParsingError as e:
        print(f"An error occurred while parsing the configuration: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_varian_values(varian_file, date_time = None):
    """
    ``get_varian_values`` is a function that extracts values from the varian .log file. This function does not extract all values. It extracts (x,y,z), theta, phi, analyzer slit.

    :args: This function has two inputs: ``varian_file`` and ``date_time``. ``varian_file`` is a string or path.``date_time`` is an array that only holds a date and a time.

    :return: Returns an array that holds values from the varian file.

    :exceptions: Will throw an exception if the input does not end with '.log'.
    
    """
    #Initialization and error handling
    varian_lines = []
    count = 0
    time_found = 0
    if not varian_file.endswith('.log'):
        raise ValueError("ERROR: input file must end with '.log'")
    #Open log, read lines
    with open(varian_file, 'r') as file:
        varian_lines = file.readlines()
    length = len(varian_lines) - 1
    #Pre processing to make values easier to manage
    while count < length:
        varian_lines[count] = varian_lines[count].replace(' ','')
        varian_lines[count] = varian_lines[count].replace('\n','')
        varian_lines[count] = varian_lines[count].split("\t")
        count = count + 1
    count = 2
    #If time is given, align varian values to time, otherwise take first row
    if date_time == None:
        #[(x,y,z),Theta,Phi,Analyzer Slit](Theta and Phi no longer used)
        return ['(' + varian_lines[1][2] + ',' + varian_lines[1][4] + ',' + varian_lines[1][6] + ')',varian_lines[1][8],varian_lines[1][10],varian_lines[1][14]]
    else:
        while time_found < 1:
            if (get_sec(date_time[1]) > get_sec(varian_lines[count][0][10:18]) - 60) and (get_sec(date_time[1]) < get_sec(varian_lines[count][0][10:18])):
                time_found = 1
                #[(x,y,z),Theta,Phi,Analyzer Slit](Theta and Phi no longer used)
                return ['(' + str(Decimal(varian_lines[count][2]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ',' + 
                        str(Decimal(varian_lines[count][4]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ',' + 
                        str(Decimal(varian_lines[count][6]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) + ')',
                        varian_lines[count][8],varian_lines[count][10],varian_lines[count][14]]
            else:
                count = count + 1

def get_jaina_values(jaina_file, date_time = None):
    """
    ``get_jaina_values`` is a function that extracts values from the jaina .log file. This function does not extract all values. It extracts temperature(Diode A,Diode B) and pressure.

    :args: This function has two inputs: ``jaina_file`` and ``date_time``. ``jaina_file`` is a string or path.``date_time`` is an array that only holds a date and a time.

    :return: Returns an array that holds values from the jaina file.

    :exceptions: Will throw an exception if the input does not end with '.log'.
    
    """
    #Initialization and error handling
    jaina_lines = []
    count = 0
    time_found = 0

    if not jaina_file.endswith('.log'):
        raise ValueError("ERROR: input file must end with '.log'")
    #Open and read lines from file
    with open(jaina_file, 'r') as file:
        jaina_lines = file.readlines()
    length = len(jaina_lines) - 1 
    #Preprocessing of lines to make values more manageable
    while count < length:
        jaina_lines[count] = jaina_lines[count].replace(' ','')
        jaina_lines[count] = jaina_lines[count].replace('\n','')
        jaina_lines[count] = jaina_lines[count].split("\t")
        count = count + 1
    count = 2
    #If time is given, align varian values to time, otherwise take first row
    if date_time == None:
        #[(Diode A,Diode B), Pressure]
        return ['[' + jaina_lines[1][1] + ',' + jaina_lines[1][2] + ']',jaina_lines[1][14]]
    else:
        while time_found < 1:
            if (get_sec(date_time[1]) > get_sec(jaina_lines[count][0][10:18]) - 60) and (get_sec(date_time[1]) < get_sec(jaina_lines[count][0][10:18])):
                time_found = 1
                #[(Diode A,Diode B), Pressure]
                return ['[' + jaina_lines[count][1] + ',' + jaina_lines[count][2] + ']',jaina_lines[count][14]]
            else:
                count = count + 1

def insert_scan_row(wavenote_file,jaina_file,varian_file,workbook_name):
    """
    ``insert_scan_row`` is a function that extracts values from a .pxt wave note file, a jaina log file, a varian log file, and inserts all of the values into the first open row of the workbook ``workbook_name``.

    :args: This function has four inputs: ``wavenote_file``,``jaina_file``,``varian_file``, and ``workbook_name``. ``wavenote_file`` is a string or a path. ``jaina_file`` is a string or path. ``varian_file`` is a string or a path. ``workbook_name`` is a string or a path.

    :return: Does not return anything. Inserts values into the workbook ``workbook_name``.

    :exceptions: Will throw an exception if the input ``wavenote_file`` does not end with '.pxt'. Will throw an exception if the input ``jaina_file`` does not end with '.log'. Will throw an exception if the input ``varian_file`` does not end with '.log'. Will throw an exception if the input ``workbook_name`` does not end with '.xlsx'.
    
    """
    #Initialization and error handling
    if not workbook_name.endswith('.xlsx'):
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
        date = date.replace('-','/')
        date = date.replace('\n','')
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
            starting_row = starting_row + 1
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
        row = [w[0],w[1],w[2],w[3],w[4],'',v[0],w[5],'',w[6],'','','',w[7],w[8],j[0],w[9],w[10],w[11],w[12],v[3],j[1],w[13]]
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
    ``arpes_folder_workbook`` is a function that creates a workbook, looks through the folder to see how many scans there are, extracts values from .pxt, jaina, and varian files for each scan, and creates a row with the extracted values for each scan. 

    :args: This function has two inputs: ``folder_name`` and ``workbook_name``. ``folder_name`` is a string or a path. ``workbook_name`` is a string or a path.

    :return: Does not return anything. Creates a workbook will a row for each .pxt file in the folder.

    :exceptions: Will throw an exception if the input``folder_name`` is not a directory. Will throw an exception if the input ``workbook_name`` does not end with '.xlsx'.
    
    """
    #Initialization and error handling
    if not os.path.isdir(folder_name):
        raise ValueError("ERROR: folder_name input must be a directory")
    if not workbook_name.endswith('.xlsx'):
        raise ValueError("ERROR: workbook_name input must end with '.xlsx'")

    jaina_logs = []
    varian_logs = []
    #Set directory paths based on directory structure, get all files from directories
    wavenote_directory = folder_name + '/ARPES Data Files/'
    jaina_directory = folder_name + '/Cadillac Equipment Readings/Server 1 Jaina/'
    varian_directory = folder_name + '/Cadillac Equipment Readings/Server 2 Varian/'
    wavenote_names = os.listdir(wavenote_directory)
    jaina_names = os.listdir(jaina_directory)
    varian_names = os.listdir(varian_directory)
    #Organize .pxt files to be in the correct order
    for name in wavenote_names:
        if not 'moly' in name:
            wavenote_names.remove(name)
    sorted_waves = sorted(wavenote_names, key=lambda x: int(x.split('_')[2].split('.')[0]))
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