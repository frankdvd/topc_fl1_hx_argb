# rgb_startup.bat

This small batch file launches `main.py` using `pythonw.exe` so the script runs without opening a console window.

File: `rgb_startup.bat` (example contents)

```
@echo off
REM Change the path below to the folder that contains your script (main.py).
REM Example: cd /d "C:\Codes\topc_fl1_hx_argb"
cd /d "C:\your\script\path"

REM Run without opening a console window using pythonw.exe
REM Ensure pythonw.exe is in PATH or use the full path to pythonw.exe
pythonw.exe main.py

REM Exit the batch file
exit /b 0
```

How to configure

1. Open `rgb_startup.bat` in a text editor.
2. Replace `C:\your\script\path` with the absolute path to the folder that contains `main.py` (for example `C:\Codes\topc_fl1_hx_argb`).
3. Optionally replace `pythonw.exe` with the full path to your Python interpreter's `pythonw.exe` (for example `C:\Python39\pythonw.exe`) if it is not on your PATH.

How to add to Windows Startup

Option A — Current user Startup folder (GUI):

1. Press Win+R, type `shell:startup` and press Enter.
2. Copy `rgb_startup.bat` into the folder that opens. The script will run at user login.

Option B — Task Scheduler (recommended for more control):

1. Open Task Scheduler.
2. Create a new task and set the trigger to "At log on" for the desired user.
3. In Actions, add a new action: Program/script = `C:\Windows\System32\cmd.exe` and add arguments `/c "C:\path\to\rgb_startup.bat"`.

Notes

- `pythonw.exe` runs Python without a console window. If your script prints errors, they will not be visible. For debugging, use `python.exe` instead.
- Make sure the working directory (the `cd /d` path) is the directory containing `main.py` so relative imports and file loads work correctly.
- If your script needs elevated privileges, configure the scheduled task to run with highest privileges.
