=======================
Molecular Beam Epitaxy
=======================

This module contains the functions for Molecular Beam Epitaxy (MBE) data. These functions allow for MBE data to be more quickly oraginzed and plotted. Of the two functions in this module, ``mbeparser`` operates primarily as the main function, and ``find_shutter_values`` operates primarily as a helper function. These functions were designed based on the specific file structure from the MBE system for which this module was designed. The file structure that holds the data consists of only text files, so these functions may not work for data with a different file structure. 

.. automodule:: mbeparser
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main