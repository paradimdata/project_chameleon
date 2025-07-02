=========================
Bruker X-Ray Diffraction
=========================

This module contains functions for Bruker X-Ray Diffraction data. Functions have been developed for three different forms of Bruker X-Ray data: Bruker .raw/.uxd files, Bruker .brml files, and Bruker .raw/.uxd/.csv background and data files. These file types correspond to the following functions: ``brukerrawconverter``, ``brml_converter``, and ``brukerrawbackground``. These functions have been designed for Bruker files, and may not work for XRD file types that are not Bruker file types. 

Bruker Raw Converter 
--------------------
``brukerrawconverter`` takes a Bruker .raw or .uxd file as an input, extracts the data from the file, and writes it into a .csv or .txt file. Here is an example of how the function ``brukerrawconverter`` can be used:

.. code-block:: python

   from project_chameleon.brukerrawconverter import brukerrawconverter
   brukerrawconverter('example_file.raw','new_file.csv')

In this example, the file 'example_file.raw' is the Bruker raw file that holds the XRD data. 'new_file.csv' is the CSV file that the data will be added to. The CSV should be empty before data is written. If no file exists with the name 'new_file.csv', a file will be created with that name. The function extracts data and metadata from the file given. Here is a list of the metadata values extracted from the file:

- Generator Current 
- Generator Voltage 
- Scan Type 
- Start 2 Theta 
- Start Angle 
- Start Theta 
- Steps 
- Step Size 
- Time Per Step 
- Used Lambda 

Bruker BRML Converter 
---------------------
``brml_converter`` takes a Bruker .brml file as an input, extracts the data from the file, and writes it into a .csv or .txt file. Here is an example of how the function ``brml_converter`` can be used:

.. code-block:: python

   from project_chameleon.brml_converter import brml_converter
   brukerrawconverter('example_file.brml','new_file.csv')

In this example, the file 'example_file.brml' is the Bruker .brml file that holds the XRD data. 'new_file.csv' is the CSV file that the data will be added to. The CSV should be empty before data is written. If no file exists with the name 'new_file.csv', a file will be created with that name. The function extracts data and metadata from the file given. Here is a list of the metadata values extracted from the file:

- Anode 
- kα1
- kα2
- Lower Discriminator Value 
- Upper Dicriminator Value 
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
- Time Per Step

Bruker Background 
-----------------
``brukerrawbackground`` takes two input files: one is a file containing data from a XRD scan, and the other is a file containing background data associated with the XRD scan. These files can be either Bruker .raw files, Bruker .uxd files, or .csv files. The function returns three plots saved as .png files and one .csv file, all in a folder. The first plot is of just the sample data. The second plot is of just the background data. The third plot is of the sample data with the background data subtracted. The .csv file holds the background subtracted data. Here is an example of how the function ``brukerrawbackground`` can be used:

.. code-block:: python

   from project_chameleon.brukerrawbackground import brukerrawbackground
   brukerrawbackground('test_background.csv','test_sample.csv', 'test_out')

In this example, the file 'test_background.csv' is the .csv file holding the background data from the XRD scan. 'test_sample.csv' is the .csv holding the data from the XRD scan of the sample. 'test_out' is the name of the folder that will hold the new files generated, as well as the beginning of the name of the files generated. For example, the plot of the sample XRD scan is named 'test_out_raw_data.png'. When this function is run, the user must input a multiplier for the background data. 

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