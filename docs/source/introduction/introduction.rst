==================================
Introduction to Project Chameleon
==================================

Project Chameleon is a collection of Python programs and modules that facilitate the processing of data commonly found in the field of material science.

What Project Chameleon provides
-------------------------------
In the field of material science research, there are some materials and measurements that generate unothordox file types. Unorothodox file types that are unable to be opened or processed by means that are commonly accessible can slow down workflows that include these files, or obstruct them entirely. Project Chameleon simplifies the process of opening and processing these files by extracting the useful data or converting files to different types without altering the data contained in the file. Project Chameleon provides programs that convert difficult to access files to more easily digestable files. Other programs in Chameleon allow for specific data to be extract from data sources that give excessive amounts of data. All files output by Project Chameleon are accessible through software that is default on both Mac and Windows operating systems.

The main programs offered by Project Chameleon process files from:

* :doc:`Angle-Resolved Photoemission Spectroscopy <../data/arpes>`
* :doc:`Bruker X-Ray Diffraction <../data/brukerrawconverter>`
* :doc:`Laue hs2 X-Ray Diffraction <../data/hs2converter>`
* :doc:`JEOL Scanning Electron Microscopy <../data/jeolsem>`
* :doc:`Molecular Beam Epitaxy <../data/mbeparser>`
* :doc:`Scanning Transmission Electron Microscopy <../data/non4dstem>`
* :doc:`Physical/Magnetic Property Management System <../data/ppmsmpms>`
* :doc:`Reflection High-Energy Electron Diffraction <../data/rheedconverter>`

Next Steps
----------
Users can proceed next to the :doc:`installation instructions <installing_chameleon>` to start working with Project Chameleon. The installation page also includes basic examples of how to use Chameleon in a Jupyter Notebook.

The section for data types provides links to the documents describing the functionality of each program with specific instructions for how to run them, as well as descriptions of the the different use cases for each program.

There are two exisitng implementations of Project Chameleon: a Docker image implementation, and a Girder implementation. More information on the Docker Image can be found :doc:`here <docker>`. More information about the Girder implementation can be found :doc:`here <plugin>`. 

Users seeking support, wishing to report issues, or wanting to contribute to Project Chameleon should do so in the `Github repository found here<https://github.com/paradimdata/project_chameleon/tree/main>`. Any problems found should be raised as issues in the repository. Anyone wishing to contribute to the project should create a pull request or create a fork. 

Acknowledgements 
----------
Financial support for the development of Project Chameleon has been provided as a part of the Platform for Accelerated Realization, Analysis, and Discovery of Interfaced Materials (PARADIM). 