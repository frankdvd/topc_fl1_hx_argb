# TOPC FL1 HX ARGB Color Setter

This repository contains a small Python script to change the ARGB LED color on a TOPC FL1 HX (vendor id 0x8888, product id 0x7A95) motherboard/controller.

The script uses hidapi to communicate with the device over HID and sends a static color frame to the LED controller.

---

## What this does

- Loads `hidapi.dll` (expects it next to `main.py`).
- Opens the HID device with vendor id `0x8888` and product id `0x7A95`.
- Sends a 256-byte feature report containing RGB values repeated for 60 LEDs and an "apply" command to update the lighting.

This is a simple, single-file utility intended for changing the static color on supported TOPC controllers.

## Requirements

- Python 3.7+ (tested with Python 3.8+)
- Windows (the repository expects `hidapi.dll` to be present alongside `main.py`)
- The Python package `hidapi` (Cython-backed preferred)

Install dependencies with pip:

```powershell
python -m pip install -r requirements.txt
```

If you run into issues with the prebuilt `hidapi` wheel, install the package that matches your Python version and platform. The `requirements.txt` contains:

- hidapi>=0.14.0

## Files

- `main.py` — main script. It contains a small `SimpleColor` helper and `static_effect()` which writes the color to the device.
- `hidapi.dll` — required native DLL (must be placed next to `main.py` on Windows).

## Usage

Run the script from the project directory (PowerShell example):

```powershell
python .\main.py
```

On success the script prints the RGB it applied and "LED strip color set successfully!".

### Command-line interface

The script now supports a simple CLI so you can set RGB from the command-line without editing the file.

Options:

- `--r` Red (0-255). Default: 255
- `--g` Green (0-255). Default: 75
- `--b` Blue (0-255). Default: 75
- `--vid` Vendor ID (hex like 0x8888 or decimal). Default: 0x8888
- `--pid` Product ID (hex like 0x7A95 or decimal). Default: 0x7A95
- `--dll` Optional path to `hidapi.dll` to load before importing `hid` (useful if the DLL is in the repo)

Examples:

```powershell
# Set color to orange-ish
python .\main.py --r 255 --g 100 --b 10

# Use explicit VID/PID
python .\main.py --r 0 --g 255 --b 0 --vid 0x8888 --pid 0x7A95

# Load a local hidapi.dll before importing
python .\main.py --r 10 --g 10 --b 255 --dll .\hidapi.dll
```

## How to change the color

Open `main.py` in a text editor and find the `main()` function. It sets the target color with `SimpleColor`:

```python
target_color = SimpleColor(255, 75, 75)
```

Replace the three numbers with the desired R, G, B values (0–255). Save and re-run the script.

If you prefer to add a CLI later, you can modify `main()` to parse command-line arguments (for example using `argparse`) and pass the parsed values into `static_effect()`.

## Troubleshooting

- "Device not found": The script enumerates HID devices and looks for vendor id `0x8888` and product id `0x7A95`. Ensure the device is connected and the IDs match your hardware. Use a USB tool (Device Manager or USB utilities) to confirm the device's VID/PID.
- `hidapi.dll` missing: Put the appropriate `hidapi.dll` for your platform next to `main.py`. Alternatively, install a platform wheel for `hidapi` that includes a DLL.
- Permission errors: On Windows run the script from an elevated prompt if necessary.
- If `hid.Device` attribute errors occur, the script already falls back to the ctypes-based API (`hid.device()`). Ensure you have the `hidapi` package that provides either interface.

## Implementation notes

- The script constructs a 256-byte feature report. It writes the color for 60 LEDs and pads the report to 256 bytes as required by the target device.
- The script sends the frame for four channels (`0x10`, `0x11`, `0x12`, `0x13`) and then an "apply" feature report to commit the change.