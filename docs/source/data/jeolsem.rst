==================================
JEOL Scanning Electron Microscopy
==================================

This module contains the functions for Scanning Electron Microscopy (SEM) data. There are two main functions ``sem_base_plot`` and ``sem_spectra_peak_labeler``. ``sem_base_plot`` is designed to handle JEOL SEM .EMSA files, and give a clean base plot, containing counts at each energy level with no labels. ``sem_spectra_peak_labeler`` is also deisgned to handle JEOL SEM .EMSA files. but instead of a clean base plot, it gives a plot with the the peaks of expected elements labeled. All peaks that aren't labeled by expected elements are given a label containing possiblities for the element causing the peak. ``get_element_peaks`` is a helper function that extracts peak data for an element from a pandas data frame. These functions were written for JEOL files and may not work correctly for other SEM data.

SEM Base Plot 
-------------
``sem_base_plot`` takes a JEOL SEM .EMSA file as an input, extracts the data from the file, and creates a plot of counts vs energy level that is saved to a .png file. Here is an example of how the function ``sem_base_plot`` can be used:

.. code-block:: python

   from project_chameleon.jeol_sem_converter import sem_base_plot
   sem_base_plot('jeol_sem.EMSA', 'jeol_sem.png')

In this example, the file 'jeol_sem.EMSA' is the raw JEOL SEM file that hold the energy count data. 'jeol_sem.png' is the image file that the plot of the data will be saved to. This function does not extract any metadata and only creates a plot of the data. 

.. automodule:: jeol_sem_converter
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main
