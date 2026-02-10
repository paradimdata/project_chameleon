===============================
Instructions and Specifications
===============================

This page provides detailed specifications and instructions on Project Chameleon

API JS Format
-------------
This is the current format for calling the Project Chameleon API using JS. 

.. code-block:: javascript

    $.ajax({
        url: finalEndpoint,
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "access-token": "nschakJJdEsIQUfADFerH6aGjyz706f114C3c8leXhM"
        },
        data: JSON.stringify(Object.assign({
            "input_url": downloadUrl,
            "output": outputFileName,
            "output_type": "raw"
        }, extraData)),
        dataType: "json"
    }).done(function(resp) {
        switch (endpoint) {
            case 'option1': 
                mimeType = 'image/png';
                break; 
            case 'option2': 
                mimeType = 'text/plain';
                break;
            case 'option3': 
                mimeType = 'text/plain';
                break;
            case 'option4': 
                mimeType = 'text/plain';
                break;
            case 'option7': 
                mimeType = 'application/zip';
            case 'option8': 
                mimeType = 'text/plain';
                break;
            default: 
                mimeType = 'application/octet-stream';  
        }
        console.log("Server Response:", resp); 
        const byteCharacters = atob(resp);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], {type: mimeType});
        let mimeType;

        var file = new FileModel();
        file.uploadToItem(view.item, blob, outputFileName, mimeType);
        $('.modal').girderModal('close');
        //location.reload();
    }).fail(function(xhr, status, error) {
        console.error("Error:", error);
        // Display error message in the dialog box
        view.$('.g-validation-failed-message').html(`<div class="alert alert-danger">Error: ${error}</div>`);
        view.$('.g-submit-create-chameleon').girderEnable(true); // Re-enable the submit button
    });

API Specification
-----------------

Documentation of possible input and output keys for the stable API of Project Chameleon

Input Keys

endpoint_id: [GENERATED] A string that contains the address the endpoint where chameleon is being hosted. Not input by the user. Generated within the code.
opa_json: [GENERATED] A dictionary copy of the data being passed into the POST call. Not input by the user. Generated within the code.
X-Auth-Access-Token: [OPTIONAL] A string associated with the endpoint that will be used as a key for access.
Access-Token: [OPTIONAL] A string associated with the endpoint that will be used as a token for access.
input_file: [OPTIONAL] A string or path that directs to a file being passed into the POST call.
input_folder: [OPTIONAL] A string or path that directs to a folder being passed into the POST call.
input_url: [OPTIONAL] A string that is a URL that is a download link for a file being passed into the POST call.
input_url_access_token_header: [OPTIONAL] If set to a header value, access token is sent with the request to acquire the input_url.
output_file: [OPTIONAL] A string or path to a file that will hold the output of the function executed in the POST call. The file should not yet exist to make sure data is not overwritten.
output_folder: [OPTIONAL] A string or path to a folder that will hold the output of the function executed in the POST call. The folder should not yet exist to make sure data is not overwritten.
input_bytes: [OPTIONAL] A string of raw bytes that are generated from the file that will be processed in the POST call.
folder_bytes: [OPTIONAL] A string of raw bytes that are generated from the folder that will be processed in the POST call.
output_type: [REQUIRED] A string that defines the form of the output. Must be one of 'raw', or 'JSON'.
output_dest: [OPTIONAL] A string that defines the form of the output. Must be one of 'caller', 'file', or 'folder'. Defaults to 'caller'. If 'file' or 'folder' is selected, 'output_file' or 'output_folder' must be included depending on the POST call. 
file_input_type: [OPTIONAL] A string that defines the file extension of the file to be processed. 
value_name: [CONDITIONAL] FOR PPMS ONLY. An integer that defines which type of PPMS file you are processing. Defaults to option 1. Options can be seen in the ppmsmpms.py file.
background_file_bytes: [CONDITIONAL] FOR BRUKERBACKGROUND ONLY. A string or path that directs to the background file being passed into the POST call.
background_file_name: [CONDITIONAL] FOR BRUKERBACKGROUND ONLY. A string of raw bytes that are generated from the background file that will be processed in the POST call.
background_file_url: [CONDITIONAL] FOR BRUKERBACKGROUND ONLY. A string that is a URL that is a download link for the background file being passed into the POST call.

Aditional Notes:
Although input_file, input_folder, input_url, input_bytes, and folder_bytes are all optional, it is required to have just one of them in the POST call.

Output Keys

{'status': 'ok', 'message': 'Files processed successfully'} : Return for output_dest 'file' 
{'status': 'ok', 'message': 'Files processed successfully'} : Return for output_dest 'folder'
{ 'status': 'ok', 'message': 'Files processed successfully', 'file_data': base64.b64encode(f.read()), 'file_name': os.path.basename(output_file)} : Return for output_dest 'JSON'

XYLIB Install Instructions for an ARM Machine
---------------------------------------------

These instructions were written from an installation of XYLIB in a conda environment. For best results, it is suggested that a conda environment is used when following these instructions and that all commands are executed inside a conda environment.

Instructions
------------

1. Install Homebrew (Brew) and add it to PATH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the following command:

.. code-block:: bash

   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

After the install completes, run the following commands (these are generated
by the installer and can be copied from the output):

.. code-block:: bash

   (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/pcauchy1/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"

2. Install pip in your environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Command (for a conda environment):

.. code-block:: bash

   conda install pip

3. Verify Python version
^^^^^^^^^^^^^^^^^^^^^^^^

Make sure you have Python 3.5 or later installed.

Check your Python version:

.. code-block:: bash

   python --version

If you need to update Python:

.. code-block:: bash

   conda update python

4. Install Xcode command line tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the following command. If they are already installed, you will receive a
message saying so.

.. code-block:: bash

   xcode-select --install

5. Install cmake
^^^^^^^^^^^^^^^^

.. code-block:: bash

   brew install cmake

6. Install git or GitHub Desktop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Either git or GitHub Desktop can be used to clone the xylib repository.
Git may already be installed.

Check git installation:

.. code-block:: bash

   git --version

7. Install swig
^^^^^^^^^^^^^^^^

.. code-block:: bash

   brew install swig

8. Install zlib and export flags
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

zlib may already be installed. If so, Homebrew will indicate this.

.. code-block:: bash

   brew install zlib

Export the required flags:

.. code-block:: bash

   export LDFLAGS="-L/opt/homebrew/opt/zlib/lib"
   export CPPFLAGS="-I/opt/homebrew/opt/zlib/include"

9. Install wxWidgets
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   brew install wxwidgets

10. Clone the xylib repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Clone the repository and change into the xylib directory.

11. Install boost (manual installation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

XYLIB requires Boost version 1.78. This version is not available via Homebrew
and must be installed manually.

Download and install Boost:

.. code-block:: bash

   curl -LO https://boostorg.jfrog.io/artifactory/main/release/1.78.0/source/boost_1_78_0.tar.gz
   tar -xvzf boost_1_78_0.tar.gz
   cd boost_1_78_0
   ./bootstrap.sh
   ./b2 install --prefix=/opt/homebrew/opt/boost@1.78

After completing these commands, change back to your xylib directory.

12. Run cmake
^^^^^^^^^^^^^

From the xylib directory:

.. code-block:: bash

   cmake .

13. Build the setup.py file
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python setup.py build_ext \
     --include-dirs=/opt/homebrew/opt/boost@1.78/include \
     --library-dirs=/opt/homebrew/opt/boost@1.78/lib

14. Install xylib
^^^^^^^^^^^^^^^^^

Make sure you are still in the xylib directory.

.. code-block:: bash

   pip install .

Troubleshooting
---------------

If the installation does not work, try the following steps.

1. Clean up Homebrew files
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   brew cleanup

2. Reset boost-related flags
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   export CXXFLAGS="-I/opt/homebrew/include"
   export LDFLAGS="-L/opt/homebrew/lib"

3. Explicitly set boost paths
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   export BOOST_INCLUDEDIR=/opt/homebrew/include
   export BOOST_LIBRARYDIR=/opt/homebrew/lib

4. Restart
^^^^^^^^^^

Restart your terminal and your system.


Expected ARPES File Structure
-----------------------------
Main Folder 
    -Analysis
    -ARPES Log Data
        -Jaina Cadillac
            -All Jaina logs here
        -System Cameras
        -Varian Cadillac
            -All Varian logs here
    -ARPES Raw Data
        -Material 
            -Secondary Material 
                -Sample Folder
                    -All scans
    -Data - Other

Example structure

PARADIM 290 - Falson - NbO
    -Analysis
    -ARPES Log Data
        -Jaina Cadillac
            -2024-07-13.log
            -2024-07-14.log
            -2024-07-15.log
            -.....
        -System Cameras
        -Varian Cadillac
            -2024-07-13.log
            -2024-07-14.log
            -2024-07-15.log
            -.....
    -ARPES Raw Data
        -NbO
            -Al2O3_0001
                -JF24020
                    -JF_24020.png
                    -JF24020_0001.pxt
                    -JF24020_0002.pxt
                    -JF24020_0003.pxt
                    -......
            -NbO_STO_111
                -JF24041
                    -JF_24041.png
                    -JF24041_0001.pxt
                    -JF24041_0002.pxt
                    -JF24041_0003.pxt
                    -......
    -Data - Other

Notes
-There are three folder names that cannot be change: ARPES Log Data, Varian Cadillac, and Jaina Cadillac. All other folder names can vary.
-No matter folder names, folder structure must stay the same. Within the raw data folder, the .pxt files must be 3 folders deeper. 
-There are three folders currently uninvolved: Analysis, System Cameras, and Data - Other. This folders have no affect on the program. Their names can be adjusted, data within those folders can be arranged in any way. They can even be removed and it will not affect the program. 


XYLIB Install Instructions for MacOS
------------------------------------
These instructions were written based on a Mac with an M1 chip and macOS Sonoma 14.1. If you have different specifications instructions may vary slightly

1) Download and install homebrew(brew):
https://docs.brew.sh/Installation

2) Download and install a C++ compiler:
For this instruction set Xcode was used. Other C++ compilers should work as well
https://developer.apple.com/documentation/safari-developer-tools/installing-xcode-and-simulators

3) Download and install MacOS cmake:
There are multiple ways to install cmake. It is recommended to simply use the command "brew install make" in a terminal.
https://cmake.org/download/
(make sure cmake is added to path for all users)

4) Install the boost version 1.76:
Boost can be installed using the command "brew install boost@1.76" in a terminal window. It is important that the boost version downloaded and installed is 1.76. Newer versions will not work for xylib. 

5) Set boost headers:
Some of the boost headers need to be adjusted to the C compiler knows where to find them. Used the commands below to point the compiler to the right headers.
export LDFLAGS="-L/opt/homebrew/opt/boost@1.76/lib"
export CPPFLAGS="-I/opt/homebrew/opt/boost@1.76/include"
The path to the boost files may be different on a different chip. If the path to your boost folder is not the same you can use the command "brew --prefix boost" to figure out where your boost folder is located. 

6) Download and unzip the xylib package:
Next you are going to want to download the xylib package from the GitHub. The version used can be found here: https://github.com/wojdyr/xylib/releases/tag/v1.6. Once the package has be downloaded, unzip it and cd into the new folder in your terminal window. 

7) Configure xylib compilation:
Run: "./configure --without-gui" in the xylib folder you just cd'ed into.

8) compile with xylib:
Run: "make"

9)Install swig with brew:
Run: "brew install swig"

10)Install the xylib python binding:
Run: pip install xylib-py

We recommend that you create a virtual environment of some kind to contain your xylib install. Xylib has conflicts with other packages so be aware. For this version xylib was installed in a conda environment. 


XYLIB Install Instructions for Windows
--------------------------------------
1) Download and install windows cmake:
https://cmake.org/download/
(make sure cmake is added to path for all users)

2) Download and install git:
https://git-scm.com/download/win
(make sure git wrappers are added to path -- defaults should do this)

3) Download and install the MSVC build tools (not full ide):
https://docs.microsoft.com/en-us/visualstudio/install/build-tools-container?view=vs-2017

(you can adjust end of url to change version, the below is written assuming 2017...)

Download: https://aka.ms/vs/15/release/vs_buildtools.exe

From command prompt:
vs_buildtools.exe --wait --passive --norestart --nocache --installPath "%ProgramFiles%\Microsoft Visual Studio\2017\BuildTools" --add Microsoft.VisualStudio.Workload.MSBuildTools --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.Component.VC.Runtime.UCRTSDK --add Microsoft.VisualStudio.Component.Windows81SDK

3) Download the header files, development files, and corresponding Release DLLs:
https://www.wxwidgets.org/downloads/

Put in c:\wxWidgets

4) Download Boost header files:
https://boostorg.jfrog.io/artifactory/main/release/1.78.0/source/
unzip in c:\Boost

5) Download prebuilt SWIG:

http://www.swig.org/download.html
unzip to c:\SWIG

6) To build python wheels:
download python 3.5 or later (x86 or x86-64 for 32-bit and 64-bit respectively) executable installers from https://www.python.org/downloads/windows/ . Install python (Make sure to add python to path). Wheels must be built for each major version (3.5/3.6/3.7/...) and each architecture (x86/x64) separately.

7) REBOOT

8) Download and build zlib dll:
https://www.zlib.net/zlib1211.zip
Open msvc prompt
cd zlib

For 32-bit, use 32-bit msvc prompt and do:
# assembly accelerated versions incompatible with SAFESEH, so don't use
nmake -f win32/Makefile.msc  

For 64-bit, use 64-bit msvc prompt and do:
nmake -f win32/Makefile.msc AS=ml64 LOC="-DASMV -DASMINF -I."  OBJA="inffasx64.obj gvmat64.obj inffas8664.obj"

9) Build XYLIB:
goto c: root
git clone https://github.com/wojdyr/xylib.git
cd xylib
# For 32-bit build with 32-bit msvc prompt
cmake -G "Visual Studio 15 2017" -A Win32 -DZLIB_ROOT=c:\zlib -DwxWidgets_ROOT_DIR=c:\wxWidgets -DwxWidgets_LIB_DIR=c:\wxWidgets\lib\vc14x_dll -B build_winx86
cd build_winx86
msbuild ALL_BUILD.vcxproj -p:configuration=release

# For 64-bit build with 64-bit msvc prompt
cmake -G "Visual Studio 15 2017" -A x64 -DZLIB_ROOT=c:\zlib -DwxWidgets_ROOT_DIR=c:\wxWidgets -DwxWidgets_LIB_DIR=c:\wxWidgets\lib\vc14x_x64_dll -B build_winx64
cd build_winx64
msbuild ALL_BUILD.vcxproj -p:configuration=release

10) Build python binary wheels
From separate admin command prompt, do:
pip install --upgrade setuptools wheel
then back in msvc console
set path=c:\swig;%PATH%
set include=c:\boost;%INCLUDE%
python setup.py bdist_wheel
