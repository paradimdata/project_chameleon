=======================
Chameleon Girder Plugin
=======================

If you are using the free and open source web-based data management platform Girder, Project Chameleon can also be implemented as a plugin within Girder. If you are working on getting started with Girder, or looking for more information on it, you can refer to the `primary Girder Github repository <https://github.com/girder/girder>`_. 

Installation and Requirements
-----------------------------
These install instructions will assume that you already have Girder running in a virtual environment of some kind. If you are not sure how to get girder running, check the documentation in the Girder Github repo. After you get Girder running, download the `Chameleon plugin repository <https://github.com/paradimdata/chameleon_plugin>`_ either through Github desktop or from the Github webpage. Once the repository is downloaded, enter the directory in your virtual environment. Once in the `chameleon_plugin` repository, run the following commands:

.. code-block:: bash

       cd girder_chameleon/web_client

To enter the `web_client` folder in the `chameleon_plugin` repo.

.. code-block:: bash

       npm run build -i    
    
To build the plugin using npm.

.. code-block:: bash

       cd girder_chameleon/web_client

To return to the top level of the repository.

.. code-block:: bash

       pip install -e . 

Finally install the project in the virtual environment, which will in turn add the plugin to Girder. If everything has been done correctly you should see the Girder instance automatically reload when the plugin is installed. Plugins that are installed in Girder will also show, and 'Chameleon' should now be included. Once the Chameleon plugin is installed, it can be modified in the Girder webpage. When you open Girder, navigate to the plugins tab in the admin console and you should see Chameleon as one of the options. There should be a gear icon that is clickable, and when clicked it should take you to a settings page where some features of the plugin can be customized. Not all functions that are part of Project Chameleon are currently included in the plugin. Here is a list of functions that are included:

 - RHEED images
 - PPMS/MPMS
 - Bruker Raw 
 - Bruker BRML
 - Non 4D STEM 
 - HS2 
 - JEOL SEM 

The plugin can be easily modified and rebuilt for futher customization. A working instance of this plugin can be seen on the PARADIM Data Portal. 

