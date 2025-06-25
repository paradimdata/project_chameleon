=============================
Installing Project Chameleon
=============================

Docker Image
------------
The quickest way to deploy OpenMSIStream programs is to use the public `Docker image<https://github.com/paradimdata/project_chameleon/blob/main/Dockerfile>`. 

The image is built off of the python:3.12-slim (Debian Linux) base image, and contains a complete install of Project Chameleon. Running the Docker image as-is will drop you into a bash terminal as the user (who has sudo privileges) in their home area. 

If you want to install Project Chameleon on your own system instead of running a Docker container, though, we recommend using a minimal installation of the conda open source package and environment management system. The instructions below start with installation of conda and outline all the necessary steps to run OpenMSIStream programs.

Quick start with miniconda3
---------------------------

Installation and requirements
-----------------------------

Running in Jupyter Notebooks
----------------------------

