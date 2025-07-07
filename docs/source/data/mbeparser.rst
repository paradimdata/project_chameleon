=======================
Molecular Beam Epitaxy
=======================

This module contains the functions for Molecular Beam Epitaxy (MBE) data. Of these functions, ``mbeparser`` is the main functions, and the others are econdary helper functions. The main function, ``mbeparser``, was designed to sort MBE data, as well as allow users to plot data. These functions were designed based on the specific file structure from the MBE system for which this module was designed. The file structure that holds the data consists of only text files, so these functions may not work for data different file types or structures. 

MBE Parser 
----------
``mbeparser`` takesa a folder containing .txt files from an MBE run, sorts the file into useful files containing data and useless files containing no data, and then allows the user to either plot a file, plot and save a file, or check a parameter value. Here is an example of how the function can be used:

.. code-block:: python

   from project_chameleon.brukerrawconverter import brukerrawconverter
   brukerrawconverter('example_file.raw','new_file.csv')


.. automodule:: mbeparser
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main