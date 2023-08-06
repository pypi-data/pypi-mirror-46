~~~~~~~~~~~~~~~~~~~~~~~
ofxstatement-be-argenta
~~~~~~~~~~~~~~~~~~~~~~~

This is a plugin for the tool `ofxstatement`_. It parses the 
``Argenta_iban_date.xlsx`` file exported from the Belgian bank Argenta and 
writes it as an OFX file.

Installation
============

You need Python 3 installed. 
You can install this plugin and ofxstatement by running: 

  $ pip install ofxstatement-be-argenta

Usage
=====

With ``ofxstatement``:

  $ ofxstatement convert -t argenta Argenta_iban_date.xlsx output.ofx

.. code-block::

   $ ofxstatement --help
   usage: ofxstatement [-h] [--version] [-d]
                    {convert,list-plugins,edit-config} ...

   Tool to convert proprietary bank statement to OFX format.

   optional arguments:
     -h, --help            show this help message and exit
     --version             show current version
     -d, --debug           show debugging information

   action:
     {convert,list-plugins,edit-config}
       convert             convert to OFX
       list-plugins        list available plugins
       edit-config         open configuration file in default editor

.. code-block::

   $ ofxstatement convert --help
   usage: ofxstatement convert [-h] -t TYPE input output

   positional arguments:
     input                 input file to process
     output                output (OFX) file to produce

   optional arguments:
     -h, --help            show this help message and exit
     -t TYPE, --type TYPE  input file type. This is a section in config file, or
                           plugin name if you have no config file.

With ``ofx-argenta-convert``:

.. code-block::

    $ py ofx-argenta-convert Argenta_iban_date.xlsx
    [INFO] Statement has been written to .\iban-today.ofx
    [INFO] Original file has been renamed to .\iban-today.xlsx

Acknowledgments
===============

- Credit to `kedder`_ for writing `ofxstatement`_.  
- Credit to `themalkolm`_ for writing the plugin `ofxstatement-seb`_ for parsing xlsx. I forked this project from it.

.. _ofxstatement: https://github.com/kedder/ofxstatement
.. _kedder: https://github.com/kedder
.. _themalkolm: https://github.com/themalkolm
.. _ofxstatement-seb: https://github.com/themalkolm/ofxstatement-seb
