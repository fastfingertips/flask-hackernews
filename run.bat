@echo off

rem Set the paths for the main Python file and requirements file
set MAIN_FILE_PATH=app/main.py
set REQS_FILE_PATH=requirements.txt

rem Check if the main Python file exists
if not exist %MAIN_FILE_PATH% goto :err_main_file_missing

rem Check if the requirements file exists
if not exist %REQS_FILE_PATH% goto :err_reqs_file_missing

:check_venv
rem Check if virtualenv is installed
where virtualenv >nul 2>nul
if %errorlevel% neq 0 (
  echo Installing virtualenv...
  pip install virtualenv
  if %errorlevel% neq 0 (
    echo Failed: Installing virtualenv. Exiting.
    exit /b %errorlevel%
  )
)
echo Checked: environment builder.

rem Check if venv folder exists
if not exist venv (
  echo Creating virtual environment folder...
  virtualenv venv
  if %errorlevel% neq 0 (
    echo Failed: Creating virtual environment folder. Exiting.
    exit /b %errorlevel%
  )
)
echo Checked: environment folder.

:activate_venv
call venv\Scripts\activate
if errorlevel 1 (
  echo Failed to activate virtual environment. Exiting.
  exit /b %errorlevel%
)
echo Checked: virtual environment.

:launch_pip
rem Install Python dependencies using pip
title Launching pip
pip install -r %REQS_FILE_PATH% >nul 2>nul &rem --force
if not %ERRORLEVEL% == 0 goto :err_pip_install
goto :launch_python

:launch_python
rem Launch the Flask application using the specified Python interpreter
title Launching python
python %MAIN_FILE_PATH% %*
if not %ERRORLEVEL% == 0 goto :err_launch_python

rem If everything is successful, exit gracefully
exit /b 0

:err_main_file_missing
title Launch failed - Main file not found
echo Main file not found: %MAIN_FILE_PATH%
echo exit code: 1
pause
exit /b 1

:err_reqs_file_missing
title Launch failed - Requirements file not found
echo Requirements file not found: %REQS_FILE_PATH%
echo exit code: 1
pause
exit /b 1

:err_pip_install
title Launch failed - Pip installation failed
echo Pip installation failed for requirements file: %REQS_FILE_PATH%
echo exit code: %ERRORLEVEL%
pause
exit /b %ERRORLEVEL%

:err_launch_python
title Launch failed - Python script failed
echo Python script failed: %MAIN_FILE_PATH%
echo exit code: %ERRORLEVEL%
pause
exit /b %ERRORLEVEL%