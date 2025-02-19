# HTTYD-point-printer
takes the positions generated during a HTTYD demo, renders and prints them. 

Requires blendplot to generate the .obj files. 
Blend plot was forked into cafeciaojoe because the requirements file needed updating. 

You need to run with sudo becuase of file permissions on Mac. Be sure to change directory to the root of the project before running the script "terminal_interface.py". Else it will not find the "rendered_views_file".

Currently working on mac, with a conda environment, see thermal_printer_httyd_environment.yml