==================================
JEOL Scanning Electron Microscopy
==================================

This module constains the functions for Scanning Electron Microscopy (SEM) data. There are two main functions, and one helper function in this module. ``sem_base_plot`` is designed to handle JEOL SEM EMSA files, and give a clean base plot. ``sem_spectra_peak_labeler`` is also deisgned to handle JEOL SEM EMSA files. but instead of a clean base plot, it gives a plot with the the peaks of expected elements labeled. All peaks that aren't labeled by expected elements are given a label containing possiblities for the element causing the peak. ``get_element_peaks`` is a helper function that extracts peak data for an element from a pandas data frame. 

.. automodule:: jeol_sem_converter
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main
