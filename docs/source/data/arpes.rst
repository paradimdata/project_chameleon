==========================================
Angle-Resolved Photoemission Spectroscopy
==========================================

This module contains all functions for Angle-Resolved Photoemission Spectroscopy (ARPES) data. Of the functions listed below, the higher-level functions are ``arpes_folder_workbook`` and ``single_log_grapher``. All other functions are helper functions for these main functions. The functions are designed to read from `.log` log files and `.pxt` Cadillac files. All functions that take a folder as input are designed for a specific folder structure, which is as follows:

.. code-block:: python

   Main Folder 
      - Analysis
      - ARPES Log Data
         - Jaina Cadillac
            - All Jaina logs here
         - System Cameras
         - Varian Cadillac
            - All Varian logs here
      - ARPES Raw Data
         - Material 
            - Secondary Material 
                  - Sample Folder
                     - All scans
      - Data - Other

This folder structure can be easily customized for personal use if necessary.

ARPES Folder Workbook 
---------------------
The main function, ``arpes_folder_workbook``, takes a folder as input, extracts data from `.pxt` files in the folder, and writes the data into a `.xlsx` file. Here is an example of how the function can be used: 

.. code-block:: python

   from project_chameleon.arpes import arpes_folder_workbook
   arpes_folder_workbook('Example/Folder/Path/XXX', 'example_excel_file.xlsx')

In this example, the folder `'XXX'` holds the `.pxt` files from which data will be extracted. When referencing the file structure, it should correspond to one of the sample folders in the ARPES Raw Data section. The example Excel file should be empty before data is added. If no `.xlsx` file exists with the name `'example_excel_file.xlsx'`, one will be created. Once data is initially written, more can be appended to the same file if new data files need to be included.

The function extracts the following data from the `.pxt` and `.log` files:

- Scan Number/File Name  
- Date  
- Scan Start Time  
- Scan End Time  
- Notes/Comments added to the scan  
- (X, Y, Z) coordinates for the scan  
- Theta (encoder) value  
- Phi (encoder) value  
- Kinetic Energy Range  
- Step Size  
- Temperature (Diode A, Diode B)  
- Run Mode  
- Acquisition Mode  
- Number of Sweeps and Layers  
- Pass Energy  
- Analyzer Slit  
- Pressure  
- Photon Energy  


Below are more details on both the main and helper functions included in the ARPES module.


.. automodule:: arpes
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main
