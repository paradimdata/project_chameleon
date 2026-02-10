.. Project Chameleon documentation master file, created by
   sphinx-quickstart on Fri May 31 11:47:08 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=============================================
Project Chameleon
=============================================

.. image:: ../../ChameleonLogo.png
   :width: 400

**Project Chameleon** provides data processing tools for files commonly found in materials science research. More information is available on the introduction page for users. Project Chameleon is maintained as part of the **Platform for the Accelerated Research, Analysis, and Discovery of Interfaced Materials (PARADIM)**, funded by the **National Science Foundation**.

.. image:: https://img.shields.io/badge/Python-3.12-blue
   :alt: Python
.. image:: https://img.shields.io/github/license/paradimdata/project_chameleon
   :alt: License 
.. image:: https://readthedocs.org/projects/project-chameleon/badge/?version=latest
   :target: https://project-chameleon.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Project Chameleon is free and open source. It can be found on `Github <https://github.com/paradimdata/project_chameleon>`_. It can also be found as a docker image in the Github repository.

Getting support
---------------
Users encountering any trouble using Project Chameleon can email contact@paradim.org for assistance. For more substantive discussions that may include suggestions on changes to OpenMSIStream as it exists, users are encouraged to create new issues on the `GitHub repository <https://github.com/paradimdata/project_chameleon/pulls>`_.

Reporting Issues or Problems
----------------------------
Users should report issues or problems encountered with OpenMSIStream by creating new Issues on the `GitHub repository <https://github.com/paradimdata/project_chameleon/issues>`_.

Contributing to Project Chameleon
---------------------------------
Users can contribute to OpenMSIStream by forking or cloning the `GitHub repository <https://github.com/paradimdata/project_chameleon>`_ and `creating Pull Requests <https://github.com/paradimdata/project_chameleon/pulls>`_ from their own forks or branches.

.. image:: ../../PARADIM_LOGO.png
   :width: 400

---

.. toctree::
   :maxdepth: 2
   :caption: Introduction to Chameleon

   introduction/introduction
   introduction/installing_chameleon
   introduction/instructions_and_specifications
 
.. toctree::
   :maxdepth: 2
   :caption: Data Types

   data/arpes
   data/brukerrawconverter
   data/hs2converter
   data/mbeparser
   data/non4dstem
   data/ppmsmpms
   data/rheedconverter
   data/jeolsem

.. toctree::
   :maxdepth: 2
   :caption: Existing Implementation

   implementation/api
   implementation/docker
   implementation/plugin

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
