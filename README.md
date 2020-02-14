# familyDB
### Installation:
- Install Python 3 and pip

### Usage:
- `python3 tkgui.py`

## Packaging
To package this program into a simple executable file, install
PyInstaller from PyPI: `pip install pyinstaller` and refer to below.
#### Windows and Linux
Create the executable file using
`pyinstaller -F -n familyViewer --clean tkgui.py`. This needs to be done manually on the OS it is going to be used on.
#### MacOS
Instead use the command `pyinstaller -F -n familyViewer --clean --add-binary /System/Library/Frameworks/Tcl.framework/Tcl:Tcl --add-binary /System/Library/Frameworks/Tk.framework/Tk:Tk tkgui.py`
on MacOS. This works best on Python 3.7.x. Any version greater than that will crash your computer
and send you to the login screen due to a bug with the tkinter library and MacOS.
