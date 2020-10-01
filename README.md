# familyDB
This is a relatively simple CRUD database application to help me learn SQL and learn about
my family history. I have records stored in a private location that I can import into this
application and manipulate. For example purposes, there are included records.

### Installation:
- Install Python 3 and pip

### Usage:
- `python3 tkgui.py`

#### Populating the Database
The first thing you'll want to do is add included records, which are example records for
English royalty that I found from a college project. Select `Populate Database` and then
`Add Included Records`. Now the app's database has records to manipulate. If you want to
edit the database manually, you can select an option from the `Add/Delete Record` dropdown
menu. If you want to purge the database and start over, select `Delete All Records`.
#### Querying the Database
Select `Search` on the main menu and select a search filter. The search uses an SQL `LIKE`
search, so the `Name`, `Birthplace`, and `Deathplace` filters should work with substrings.
The `Birthdate` filter also will search with the included numbers, but works best if it is formatted like `YYYY-MM-DD`. If wanting to search all years, leave out the `YYYY`. For example, if you wanted to search for birthdates of October 1st in any year, you could enter `-10-01`. Same goes for searching for people born in May: `-05-`. Entering `-05` will search for people born in May or on the 5th of any month, as both have the `-05` substring. To assist with this formatting and make it easier to search for a birthday on the current day, the birthdate field is auto-populated with today's date in the latest commit on the master branch. This feature will be in the next release.

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
