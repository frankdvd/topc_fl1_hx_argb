@echo off
REM Change the path below to the folder that contains your script (main.py).
REM Example: cd /d "C:\Codes\topc_fl1_hx_argb"
cd /d "C:\your\script\path"

REM Run without opening a console window using pythonw.exe
REM Ensure pythonw.exe is in PATH or use the full path to pythonw.exe
pythonw.exe main.py

REM Exit the batch file
exit /b 0
