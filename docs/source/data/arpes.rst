==========================================
Angle-Resolved Photoemission Spectroscopy
==========================================

This module contains all functions for Angle-Resolved Photoemission Spectroscopy (ARPES) data. Of the functions below, the higher level functions are ``arpes_folder_workbook`` and `single_log_grapher`. All other functions are helper functions for the main functions. The functions have been designed to read from .log log files and .pxt Cadillac files. All functions that take a folder input are designed for a specific folder structure. The structure is as follows:

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

The folder structure can be easily changed for personal use if necessary.

ARPES Folder Workbook 
---------------------
 The main function ``arpes_folder_workbook`` takes a folder as an input, extracts data from .pxt files in the folder, and writes the data into a .xlsx file. Here is an example of how the main function, ``arpes_folder_workbook``, can be used: 

.. code-block:: python

   from project_chameleon.arpes import arpes_folder_workbook
   arpes_folder_workbook('Example/Folder/Path/XXX', 'example_excel_file.xlsx')

In this example, the example folder 'XXX' holds the .pxt files that data will be extracted from. When looking at the file structure, it should be one of the sample folders from the ARPES raw data section of the file structure. The example excel file should be empty before data is added. If no .xlsx file exists with the name 'example_excel_file.xlsx', one will be created with that name. Once data is initially written, more can be added in the same file if new data files need to be added. The function extracts the following data from the .pxt and .log files:

- Scan Number/File Name
- Date 
- Scan Start Time 
- Scan End Time 
- Notes/Comments added to the scan 
- (X,Y,Z) coordinate for the scan 
- Theta(encoder) value 
- Phi(encoder) value 
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

Below are more details on both the main and helper functions that are a part of the ARPES file. 

.. automodule:: arpes
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main