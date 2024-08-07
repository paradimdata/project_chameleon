import os.path
import os
import subprocess
import htmdec_formats
from configparser import ParsingError
from pandas import DataFrame
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import Border, Side
from openpyxl.styles import Font, Alignment

def build_arpes_workbook(workbook_name):
    if not workbook_name.endswith('.xlsx'):
        raise ValueError("ERROR: workbook_name input must end with '.xlsx'")

    wb = Workbook()
    ws = wb.active

    row_1 = ['Colored Labels','Colored Labels','Alignment Maps','Hi-Stat Map','"Good" High-Stat Scan','"Good" High-Stat Scan','Mono Lamp Change','Mono Lamp Change','Slit Change','Slit Change','Theta Offset:','0','Phi Offset:','0',
             'Omega Offset:','0']
    row_2 = ['Scan Number/File Name','Time Start','Notes/Comments','FS Position','(X,Y,Z)','Theta(encoder)','Theta(true)','Phi(encoder)','Phi(true)',
             'Omega(Manipulator,approx)','Omega(true)','Kinetic Energy Range(eV)','Step Size(meV)','Temperature(K)[Diode A,Diode B]','Run Mode','Acquisition Mode',
             '# of Sweeps','Pass Energy','Analyzer Slit','Pressure(Torr)','Photon Energy(eV)']

    first_col = 1
    last_col = 26
    row_1_last_col = 16
    row_2_last_col = 21
    end_col = 12

    thin_border = Border(
        top=Side(style='thin'),
        bottom=Side(style='thin')
    ) 

    for col in range(first_col, last_col + 1):
        col_letter = get_column_letter(col)
        ws.column_dimensions[col_letter].width = 20

    for col in range(first_col, end_col + 1):
            cell = ws.cell(row=2, column=col)
            cell.border = thin_border

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

    fill_color1 = PatternFill(start_color="FFA07A", end_color="FFA07A", fill_type="solid")#Light orange
    fill_color2 = PatternFill(start_color="D8BFD8", end_color="D8BFD8", fill_type="solid")#Light purple
    fill_color3 = PatternFill(start_color="66CDAA", end_color="66CDAA", fill_type="solid")#Light green
    fill_color4 = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")#Light blue
    fill_color5 = PatternFill(start_color="FFFACD", end_color="FFFACD", fill_type="solid")#light yellow
    fill_color6 = PatternFill(start_color="FFB6C1", end_color="FFB6C1", fill_type="solid")#light red
    fill_grey = fill_color = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")

    ws.merge_cells('A1:B1')
    ws.merge_cells('E1:F1')
    ws.merge_cells('G1:H1')
    ws.merge_cells('I1:J1')
    ws.merge_cells('A3:A4')
    ws.merge_cells('B3:I4')
    
    ws['C1'].fill = fill_color1
    ws['D1'].fill = fill_color2
    ws['E1'].fill = fill_color3
    ws['G1'].fill = fill_color4
    ws['I1'].fill = fill_color5
    ws['A5'].fill = fill_color6
    ws['K1'].fill = fill_grey

    cell = ws['A3']
    cell.value = 'Initial Notes/Sample Information'
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell = ws['A5']
    cell.value = 'Initial Start:'
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal='center', vertical='center')

    wb.save(workbook_name)

def get_wavenote_values(wavenote_file):
     
    lines = []

    if not wavenote_file.endswith('.pxt'):
        raise ValueError("ERROR: input file must end with '.pxt'")
    data_file = os.path.join(os.path.dirname(wavenote_file), "data_holder.txt")
     
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
        return [scan_number,lines[28].split('=')[1] + ':' + lines[29].split('=')[1],lines[27].split('=')[1],
                '[' + lines[11].split('=')[1] + ',' + lines[12].split('=')[1] + ']',lines[13].split('=')[1],lines[35],lines[8].split('=')[1],
                lines[5].split('=')[1],lines[4].split('=')[1],lines[6].split('=')[1]]
    except ParsingError as e:
        print(f"An error occurred while parsing the configuration: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_varian_values(varian_file):

    varian_lines = []
    count = 0

    if not varian_file.endswith('.log'):
        raise ValueError("ERROR: input file must end with '.log'")
   
    with open(varian_file, 'r') as file:
        varian_lines = file.readlines()
    length = len(varian_lines) - 1
    while count < length:
        varian_lines[count] = varian_lines[count].replace(' ','')
        varian_lines[count] = varian_lines[count].replace('\n','')
        varian_lines[count] = varian_lines[count].split("\t")
        count = count + 1

    return ['(' + varian_lines[1][2] + ',' + varian_lines[1][4] + ',' + varian_lines[1][6] + ')',varian_lines[1][8],varian_lines[1][10],varian_lines[1][14]]

def get_jaina_values(jaina_file):

    jaina_lines = []
    count = 0

    if not jaina_file.endswith('.log'):
        raise ValueError("ERROR: input file must end with '.log'")
   
    with open(jaina_file, 'r') as file:
        jaina_lines = file.readlines()
    length = len(jaina_lines) - 1 
    while count < length:
        jaina_lines[count] = jaina_lines[count].replace(' ','')
        jaina_lines[count] = jaina_lines[count].replace('\n','')
        jaina_lines[count] = jaina_lines[count].split("\t")
        count = count + 1

    return ['[' + jaina_lines[1][1] + ',' + jaina_lines[1][2] + ']',jaina_lines[1][14]]

def insert_scan_row(wavenote_file,jaina_file,varian_file,workbook_name):
    if not workbook_name.endswith('.xlsx'):
        raise ValueError("ERROR: workbook_name input must end with '.xlsx'")

    first_col = 1
    last_col = 21
    starting_row = 6
    starting_cell = 0

    w = get_wavenote_values(wavenote_file)
    j = get_jaina_values(jaina_file)
    v = get_varian_values(varian_file)

    wb = wb = load_workbook(filename = workbook_name)
    ws = wb.active

    while starting_cell == 0:
        cell = ws.cell(row=starting_row, column=first_col)
        if not cell.value:
            starting_cell = 1
        else:
            starting_row = starting_row + 1

    if w == None:
        ws.row_dimensions[starting_row].height = 40
        for col in range(first_col, last_col):
            cell = ws.cell(row=starting_row, column=1)
            cell.value = 'Error' 
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center',wrapText=True)
    else:
        row = [w[0],w[1],w[2],'',v[0],v[1],'',v[2],'','','',w[3],w[4],j[0],w[5],w[6],w[7],w[8],v[3],j[1]]

        ws.row_dimensions[starting_row].height = 40
        for col in range(first_col, last_col):
            cell = ws.cell(row=starting_row, column=col)
            cell.value = row[col-1] 
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center',wrapText=True)

    wb.save(workbook_name)

def arpes_folder_workbook(folder_name, workbook_name):

    jaina_logs = []
    varian_logs = []

    wavenote_directory = folder_name + '/ARPES Data Files/'
    jaina_directory = folder_name + '/Cadillac Equipment Readings/Server 1 Jaina/'
    varian_directory = folder_name + '/Cadillac Equipment Readings/Server 2 Varian/'

    wavenote_names = os.listdir(wavenote_directory)
    jaina_names = os.listdir(jaina_directory)
    varian_names = os.listdir(varian_directory)

    for f in jaina_names:
        if f.endswith('.log'):
            jaina_logs = jaina_logs + [jaina_directory + f]

    for f in varian_names:
        if f.endswith('.log'):
            varian_logs = varian_logs + [varian_directory + f]

    build_arpes_workbook(workbook_name)

    for f in wavenote_names:
        if f.endswith('.pxt'):
            insert_scan_row(wavenote_directory + f,jaina_logs[0],varian_logs[0],workbook_name)
    

    
