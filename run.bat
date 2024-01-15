@echo off

set MAIN_FILE_PATH=app/main.py
set REQS_FILE_PATH=requirements.txt
if not defined PYTHON set PYTHON=python

if not exist %MAIN_FILE_PATH% goto :err
if not exist %REQS_FILE_PATH% goto :launch_py

:launch_pip
title Launching pip
pip install -r %REQS_FILE_PATH%
if not %ERRORLEVEL% == 0 goto :err
goto :launch_py

:launch_py
title Launching python
%PYTHON% %MAIN_FILE_PATH% %*
if not %ERRORLEVEL% == 0 goto :err

:err
title Launch failed
echo exit code: %ERRORLEVEL%
pause
