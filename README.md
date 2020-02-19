# familyDB
### Installation:
- Install Python 3 and pip

### Usage:
- `python3 tkgui.py`

## Packaging
To package this program into a simple executable file, install
PyInstaller from PyPI: `pip install pyinstaller` and refer to below. Using the
command appropriate for your Operating System will produce an executable file in the
`dist` folder called `familyViewer`. Click on this to run the compiled program.
#### Windows
Create the executable file by running `install.bat`. This needs to be done manually on the OS it is going to be used on.
#### MacOS
Instead run the `install.sh` script on MacOS. This works best on Python 3.7.x. Any version greater than that will crash your computer
and send you to the login screen due to a bug with the tkinter library and MacOS.
#### Linux
Use the command from `install.sh` without the `--add binary` flags.
