=============================================
Physical/Magnetic Property Management System
=============================================

This module contains a function for handling Physical/Magnetic Property Management System (PPMS/MPMS) data. The function takes a PPMS/MPMS `.dat` file, detects its measurement type, and extracts relevant metadata and data columns. The measurement types are based on the specific configurations of the PPMS/MPMS machine used.

PPMS/MPMS Parser
----------------
``ppmsmpmsparser`` takes a PPMS/MPMS `.dat` file as input, extracts the data, and writes it to a `.csv` file. Here is an example of how the function ``ppmsmpmsparser`` can be used: 

.. code-block:: python

   from project_chameleon.ppmsmpms import ppmsmpmsparser
   ppmsmpmsparser('measurement.dat', 'data.csv')

In this example, `'measurement.dat'` is the input file containing the PPMS/MPMS data. `'data.csv'` is the CSV file where the extracted data will be saved. The CSV file should be empty before writing. If a file named `'data.csv'` does not already exist, one will be created. No metadata is extracted or displayed by this function.


Below is more information on the main function:


.. automodule:: ppmsmpms
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main
