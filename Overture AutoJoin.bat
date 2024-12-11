@echo off
title Overture AutoJoin
setlocal enabledelayedexpansion

rem Check for admin rights, and request if not an administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting admin privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

rem Define URLs and paths
set python_installer_url=https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe
set python_install_dir=%ProgramFiles%\Python39
set python_exe=%python_install_dir%\python.exe
set pip_exe=%python_install_dir%\Scripts\pip.exe


rem Check if Python is installed and its version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not in PATH. Attempting to install Python...
    curl -L -o "%installer_dir%python_installer.exe" %python_installer_url%
    if errorlevel 1 (
        echo Failed to download Python installer! Exiting.
        pause
        exit /b
    )
    start /wait "" "%installer_dir%python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    if exist "%python_exe%" (
        echo Python installed successfully.
    ) else (
        echo Python installation failed! Attempting to add Python manually to system PATH...
        setx PATH "%python_install_dir%;%PATH%"
        python --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo Failed to set Python in PATH. Please restart and try again.
            pause
            exit /b
        ) else (
            echo Python added to PATH successfully.
        )
    )
) else (
    for /f "tokens=2 delims= " %%i in ('python --version') do (
        set python_version=%%i
        if "!python_version!"=="3.13.0" (
            echo Found Python version 3.13.0. Uninstalling...
            rmdir /s /q "%python_install_dir%"
            echo Please reinstall with the correct version.
            pause
            exit /b
        )
    )
)


rem Check for pip and install if not available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. This should be installed with Python.
    echo Please ensure that you run the Python installer correctly.
    echo Attempting to install pip using get-pip.py...
    curl -L -o "%installer_dir%get-pip.py" https://bootstrap.pypa.io/get-pip.py
    if errorlevel 1 (
        echo Failed to download get-pip.py! Exiting.
        pause
        exit /b
    )
    "%python_exe%" "%installer_dir%get-pip.py"
    if errorlevel 1 (
        echo Failed to install pip! Please ensure Python is installed correctly.
        pause
        exit /b
    ) else (
        echo pip installed successfully.
    )
)


rem Install required Python modules
set "modules=requests"
for %%m in (%modules%) do (
    "%python_exe%" -c "import %%m" >nul 2>&1
    if %errorlevel% neq 0 (
        echo Installing missing module %%m...
        "%pip_exe%" install %%m
        if errorlevel 1 (
            echo Warning: Skipped installation of %%m due to an error.
        ) else (
            echo Module %%m installed successfully.
        )
    )
)

python %0\..\data.py