"""
RGB LED Strip Control (Single File Version)
Set color to RGB(255, 75, 75)
"""
from pathlib import Path
import ctypes
import argparse
import sys

# Defer importing `hid` until runtime so `--help` works even if hidapi.dll is missing.
hid = None

class SimpleColor:
    """Simple color class"""
    def __init__(self, r, g, b):
        self._r = r
        self._g = g
        self._b = b
    
    def red(self):
        return self._r
    
    def green(self):
        return self._g
    
    def blue(self):
        return self._b

def static_effect(color=None, vid=0x8888, pid=0x7A95):
    """
    Static lighting effect implementation
    Compatible with both hidapi versions (Cython and ctypes)
    """
    _dev = None
    
    # Find the device
    device_found = False
    for dev in hid.enumerate():
        if dev['vendor_id'] == vid and dev['product_id'] == pid:
            device_found = True
            break
    
    if not device_found:
        print("Device not found")
        return
    
    # Try Cython version first (hid.Device)
    try:
        _dev = hid.Device(vid, pid)
    except (AttributeError, TypeError):
        # Fall back to ctypes version (hid.device)
        try:
            _dev = hid.device()
            _dev.open(vid, pid)
        except Exception as e:
            print(f"Failed to open device: {e}")
            return
    
    current_color = color if color else SimpleColor(255, 75, 75)  # Default Pink
    r, g, b = [int(current_color.red()),
                int(current_color.green()),
                int(current_color.blue())]
    
    # Construct LED strip data
    data = [0x10, 0, 0x00] + [r, g, b] * 60  # Fixed params + 60 LED colors
    data += [0] * (256 - len(data))  # Pad to 256 bytes
    
    apply_cmd = [0x01, 0, 0x88, 0xFF] + [0]*252  # Apply command
    
    # Send data for 4 channels
    for channel in [0x10, 0x11, 0x12, 0x13]:
        data[0] = channel
        _dev.send_feature_report(bytes(data))
        _dev.send_feature_report(bytes(apply_cmd))

def _ensure_hid(loaded_dll_path=None):
    """Load hidapi DLL and import hid at runtime.

    Returns the imported `hid` module or raises an ImportError.
    """
    global hid
    if hid is not None:
        return hid

    # Optionally load a local hidapi.dll first for the ctypes back-end
    if loaded_dll_path:
        ctypes.CDLL(str(loaded_dll_path))

    try:
        import hid as _hid
    except Exception as e:
        raise ImportError(f"Failed to import hid module: {e}")

    hid = _hid
    return hid


def main(argv=None):
    parser = argparse.ArgumentParser(description="Set static ARGB color for TOPC FL1 HX devices")
    parser.add_argument("--r", type=int, default=255, help="Red value 0-255")
    parser.add_argument("--g", type=int, default=75, help="Green value 0-255")
    parser.add_argument("--b", type=int, default=75, help="Blue value 0-255")
    parser.add_argument("--vid", type=lambda x: int(x, 0), default=0x8888, help="Vendor ID (hex or decimal). Default 0x8888")
    parser.add_argument("--pid", type=lambda x: int(x, 0), default=0x7A95, help="Product ID (hex or decimal). Default 0x7A95")
    parser.add_argument("--dll", type=str, default=None, help="Optional path to hidapi.dll to load before importing hid")

    args = parser.parse_args(argv)

    # Validate RGB
    for channel_name in ("r", "g", "b"):
        val = getattr(args, channel_name)
        if val < 0 or val > 255:
            print(f"{channel_name.upper()} must be in range 0-255")
            return 2

    # If user provided a DLL path, attempt to load it
    dll_path = None
    if args.dll:
        dll_path = Path(args.dll)
        if not dll_path.exists():
            print(f"Specified DLL not found: {dll_path}")
            return 3

    try:
        _ensure_hid(dll_path)
    except ImportError as e:
        print(e)
        return 4

    # Build color
    target_color = SimpleColor(args.r, args.g, args.b)

    print(f"Setting LED strip color to RGB({target_color.red()}, {target_color.green()}, {target_color.blue()}) on VID=0x{args.vid:04X} PID=0x{args.pid:04X}...")

    try:
        static_effect(target_color, vid=args.vid, pid=args.pid)
        print("LED strip color set successfully!")
    except Exception as e:
        print(f"Failed to set color: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())