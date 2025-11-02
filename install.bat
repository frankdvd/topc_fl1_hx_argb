@echo off
SETLOCAL

REM ===== Default script path =====
SET "DEFAULT_SCRIPT_PATH=C:\Codes\topc_fl1_hx_argb\main.py"

REM ===== Ask user for the script path =====
set /p SCRIPT_PATH=Please enter the full path to your main.py script [default: %DEFAULT_SCRIPT_PATH%]: 

REM ===== If input is empty, use default =====
IF "%SCRIPT_PATH%"=="" SET "SCRIPT_PATH=%DEFAULT_SCRIPT_PATH%"

REM ===== Check if the file exists =====
if not exist "%SCRIPT_PATH%" (
    echo File not found: %SCRIPT_PATH%
    pause
    exit /b 1
)

REM ===== Automatically find pythonw.exe =====
FOR /F "tokens=*" %%A IN ('where pythonw.exe 2^>nul') DO SET "PYTHONW_PATH=%%A"

IF NOT DEFINED PYTHONW_PATH (
    echo pythonw.exe not found. Please make sure Python is installed and in PATH.
    pause
    exit /b 1
)

REM ===== Task names =====
SET "TASK_NAME=MainBoardLED_Pink"
SET "TASK_NAME_WAKE=MainBoardLED_Pink_Wake"

REM ===== Delete existing tasks if they exist =====
schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1
schtasks /Delete /TN "%TASK_NAME_WAKE%" /F >nul 2>&1

REM ===== Create task for logon (boot/startup) =====
schtasks /Create /TN "%TASK_NAME%" /RL HIGHEST /F /SC ONLOGON /TR "\"%PYTHONW_PATH%\" \"%SCRIPT_PATH%\""

REM ===== Create task for sleep/wake trigger =====
REM Using Kernel-Power Event ID 1 (resume from sleep/hibernate)
schtasks /Create /TN "%TASK_NAME_WAKE%" /RL HIGHEST /F /SC ONEVENT /EC "System" /MO "*[System[(EventID=1)]]" /TR "\"%PYTHONW_PATH%\" \"%SCRIPT_PATH%\""

echo.
echo Installation complete! Tasks created:
echo - %TASK_NAME% (Logon/Startup trigger)
echo - %TASK_NAME_WAKE% (Sleep/Wake trigger via Kernel-Power Event)
echo.
echo Script path: %SCRIPT_PATH%
echo Pythonw.exe path: %PYTHONW_PATH%
pause
