=========================
Bruker X-Ray Diffraction
=========================

This module contains functions for Bruker X-Ray Diffraction (XRD) data. Functions have been developed for three different forms of Bruker X-Ray data: Bruker `.raw`/`.uxd` files, Bruker `.brml` files, and Bruker `.raw`/`.uxd`/`.csv` background and data files. These file types correspond to the following functions: ``brukerrawconverter``, ``brml_converter``, and ``brukerrawbackground``. These functions are specifically designed for Bruker files and may not work with XRD file types that are not in a Bruker format.

Bruker Raw Converter 
--------------------
``brukerrawconverter`` takes a Bruker `.raw` or `.uxd` file as input, extracts data from the file, and writes it to a `.csv` or `.txt` file. Here is an example of how the function can be used:

.. code-block:: python

   from project_chameleon.brukerrawconverter import brukerrawconverter
   brukerrawconverter('example_file.raw', 'new_file.csv')

In this example, `'example_file.raw'` is the Bruker raw file that contains the XRD data. `'new_file.csv'` is the CSV file to which the data will be written. The CSV file should be empty before data is written. If no file with the name `'new_file.csv'` exists, one will be created. The function extracts both data and metadata from the input file. Below is a list of metadata values extracted:

- Generator Current  
- Generator Voltage  
- Scan Type  
- Start 2 Theta  
- Start Angle  
- Start Theta  
- Steps  
- Step Size  
- Time per Step  
- Used Lambda  

Bruker BRML Converter 
---------------------
``brml_converter`` takes a Bruker `.brml` file as input, extracts data from the file, and writes it to a `.csv` or `.txt` file. Here is an example of how the function can be used:

.. code-block:: python

   from project_chameleon.brml_converter import brml_converter
   brml_converter('example_file.brml', 'new_file.csv')

In this example, `'example_file.brml'` is the Bruker BRML file that contains the XRD data. `'new_file.csv'` is the CSV file to which the data will be written. The CSV file should be empty before data is written. If no file with the name `'new_file.csv'` exists, one will be created. The function extracts both data and metadata from the input file. Below is a list of metadata values extracted:

- Anode  
- Kα1  
- Kα2  
- Lower Discriminator Value  
- Upper Discriminator Value  
- Generator Current  
- Generator Voltage  
- Goniometer Radius  
- Sample Rotation  
- Primary Soller Slit  
- BRML File Name  
- BSML File Name  
- Start Time  
- End Time  
- Scan Type  
- Start 2 Theta  
- Start Angle  
- Start Beam Translation  
- Start Phi  
- Start Theta  
- Steps  
- Step Size  
- Total Time per Step  
- Time per Step  

Bruker Background 
-----------------
``brukerrawbackground`` takes two input files: one containing XRD scan data, and the other containing background data associated with the scan. These files can be Bruker `.raw`, `.uxd`, or `.csv` files. The function returns three plots saved as `.png` files and one `.csv` file, all stored in a folder.

- The first plot shows the sample data.  
- The second plot shows the background data.  
- The third plot shows the sample data with the background subtracted.  
- The `.csv` file contains the background-subtracted data.  

Here is an example of how the function can be used:

.. code-block:: python

   from project_chameleon.brukerrawbackground import brukerrawbackground
   brukerrawbackground('test_background.csv', 'test_sample.csv', 'test_out')

In this example:
- `'test_background.csv'` is the file containing background data from the XRD scan.
- `'test_sample.csv'` is the file containing the sample scan data.
- `'test_out'` is the name of the folder where output files will be saved and also serves as a prefix for the filenames.

For example, the plot of the sample XRD scan is saved as `'test_out_raw_data.png'`. When this function is executed, the user must also input a multiplier for the background data.


Below is more information on the main functions, as well as some of the helper functions.


.. automodule:: brukerrawconverter
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main

.. automodule:: brml_converter
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main

.. automodule:: brukerrawbackground
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main
