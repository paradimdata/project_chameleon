---
title: 'Project Chameleon: A Python Package for Interoperability in Experimental Materials Science Research Data'
tags:
  - Python
  - FAIR Data
  - materials science
  - crystal growth
  - reflection high-energy electron diffraction
  - angle-resolved photoemission spectroscopy
  - molecular beam epitaxy
  - scanning transmission electron microscopy
  - x-ray diffraction
authors:
  - name: Peter Cauchy
    orcid: 0009-0007-1155-0509
    affiliation: "1, 2, 3, 4"
  - name: David Elbert
    orcid: 0000-0002-2292-180X
    affiliation: "1, 2"
  - name: Tyrel McQueen
    orcid: 0000-0002-8493-4630
    affiliation: "1, 2, 3, 4"
affiliations:
 - name: PARADIM, William H. Miller III Department of Physics and Astronomy, Johns Hopkins University, Baltimore 21218, MD
   index: 1
   ror: 04pw1zg89
 - name: Hopkins Extreme Materials Institute, Johns Hopkins University, Baltimore, MD 21218
   index: 2
   ror: 02ed2th17
 - name: Department of Chemistry, Johns Hopkins University, Baltimore 21218, MD
   index: 3
 - name: Department of Materials Science and Engineering, Johns Hopkins University, Baltimore 21218, MD
   index: 4
date: 13 August 2025
bibliography: paper.bib
---

# Summary

Project Chameleon is a versatile Python package for extensible data transformation and interoperability. Chameleon streamlines analysis and combination of scientific data from different sources and provides a foundational pillar for implementation of the FAIR (Findable, Accessible, Interoperable, and Reusable) data principles [@wilkinson:2016]. In the context of FAIR, interoperability refers to the ability of diverse datasets, tools, and systems to seamlessly interact, integrate, and exchange data. Interoperability ensures that scientific data can be readily combined or used alongside related datasets, software, and analytical tools across different domains and disciplines.  

A central barrier to interoperability arises from heterogeneous data formats and differing metadata conventions encoded in the varied file formats of different laboratories. Project Chameleon transformations eliminate this barrier to provide effective interoperability that facilitates comprehensive analyses and machine learning that accelerate scientific discovery and enhance reproducibility of scientific findings.

Project Chameleon provides a collection of conversion scripts accessed through a REST API that enables researchers to simply convert specialized, often manufacturer-specific file formats for data such as RHEED electron diffraction patterns, scanning transmission electron microscopy (STEM) arrays, molecular beam epitaxy (MBE) logs, magnetic property measurement system analyses (PPMS/MPMS), and X-ray diffraction patterns into universally accessible formats like CSV for tabular data and PNG for image data. These universal formats provide the research community the ability to use open and readily available tools to analyze and visualize data from different instruments or laboratories. The API for Project Chameleon provides a function-based, user-friendly interface that allows simple conversions of some common file types. The API is also designed to handle multiple input and output types, including raw bytes, JSON, and URLs, giving flexibility in how it can be implemented. Project Chameleon itself leverages several open source packages for conversion and processing of specialized formats [@savitzky:2021; @pena:2025; @wojdyr:2025; @htmdec:2025].

# Statement of need

The U.S. interagency Materials Genome Initiative [@mgi:2021; @brinson:2024; @odegard:2023; @depablo:2019; @nasem:2024] demands a leap in FAIR-compliant data to accelerate materials discovery, AI/ML applications, high-throughput experimentation, advanced digital twins, and growing interest in autonomous laboratories and manufacturing.  

Fundamental research in materials science, chemistry, and solid-state physics, however, depends on structure and property characterizations that use a wide range of techniques including, but not limited to, diffraction, microscopy, and spectroscopy. While these methods are a common thread in modern science, they rely on a wide variety of laboratory instrumentation developed by a wide range of manufacturers, creating a multitude of data formats demanding use of specialized analysis tools. The wide variation in data formats hinders FAIR interoperability; the inability to combine data from different sources or reproduce analyses done in different labs thwarts Open Science and MGI goals.  

Project Chameleon was designed to be used by materials science researchers, but is applicable to any field of research using instrumental characterization tools. Project Chameleon is already in use in the NSF PARADIM Materials Innovation Platform (Cornell and Johns Hopkins universities) as well as the McQueen Lab at Johns Hopkins where the ARPES, Bruker RAW, Bruker BRML, 4D STEM, Non-4D STEM, RHEED, MBE, PPMS/MPMS, Laue HS2, and JEOL SEM functions have been implemented. These functions are used in the lab file server for McQueen Lab and to create FAIR datasets published with DOIs in the PARADIM Data Portal [@paradim:2025], allowing for the download of the raw file or converted file without any work done on the user’s end.  

# Related Work

The value of project chameleon (PC) relative to existing alternatives is its versatility, and its focus on experimental (not computational) file formats. Existing FAIR/data-model/workflow tools are tailored primarily for computational work, or only support a small subset of experimental data types. Other data-type-specific tools do exist, but again do not capture the breadth and depth of what is needed. For example, GSAS-II is a commonly used x-ray diffraction data analysis tool that is capable of importing and exporting several formats, and Hyperspy is commonly used for the visualization and processing of EM/4D-STEM data, which is a distinct set of formats. The value of PC is in being able to convert any of these formats (and many others; e.g. all formats of xylib are supported, PC calls xylib as a backend for certain conversions) with a single plugin, with a unified API interface. PC is further openly deployable, in contrast to vendor-specific (and vendor-locked-in and licensed) development kits.

# Acknowledgements

We acknowledge contributions and support from Maggie Eminizer, Matt Turk, Ali Rachidi, Steve Zeltman, Ben Redemann, Abby Neil, and Evan Crites.

# References
