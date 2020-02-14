# familyDB
### Installation:
- Install Python 3 and pip
- `pip3 install -r requirements.txt`

### Usage:
- `python3 screen.py`

## Packaging
To package this program into a simple executable file, install
PyInstaller from PyPI: `pip install pyinstaller` and refer to below.
#### Windows and Linux
Create the executable file using
`pyinstaller -F -n familyViewer --clean screen.py`. This needs to be done manually on the OS it is going to be used on.
#### MacOS
Instead use the command `pyinstaller -F -n familyViewer --clean --add-binary /System/Library/Frameworks/Tcl.framework/Tcl:Tcl --add-binary /System/Library/Frameworks/Tk.framework/Tk:Tk screen.py`
on MacOS. This works best on Python 3.7.0, but 3.7.5 will handle it. Any version greater
than that will crash your computer and send you to the login screen due to a bug with the
Python Tkinter library and MacOS.
