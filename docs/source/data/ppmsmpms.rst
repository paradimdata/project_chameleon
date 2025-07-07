=============================================
Physical/Magnetic Property Management System
=============================================

This module contains the function for Physical/Magnetic Property Management System (PPMS/MPMS) data. The function in this module takes a PPMS/MPMS .dat file, detects the measurement type for the file, and extracts the relevant metadata and columns of data from the .dat file. The measurement types were created based on the measurement types of the given PPMS/MPMS machine. 


PPMS/MPMS Parser
----------------
``ppmsmpmsparser`` takes a PPMS/MPMS .dat file as an input, extracts the data from the file, and writes it into a .csv file. Here is an example of how the function ``ppmpsmpmsparser`` can be used: 

.. code-block:: python

   from project_chameleon.ppmsmpms import ppmpsmpmsparser
   ppmpsmpmsparser('measurement.dat','data.csv')

In this example, the file 'measurement.dat' is the file that holds the PPMS/MPMS data. 'data.csv' is the CSV file that the data will be added to. The CSV should be empty before data is written. If no file exists with the name 'data.csv', one will be created witht that name. No meta data is extracted or displayed as part of this function. 


Below is more information on the main function.


.. automodule:: ppmsmpms
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main