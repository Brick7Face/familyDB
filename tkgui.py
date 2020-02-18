import tkinter as tk
from tkinter import ttk
import sys
import familyDB

# allows redirecting stdout, stderr to a text widget
class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    # overwrite write method
    def write(self, string):
        self.text_space.config(state=tk.NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        self.text_space.config(state=tk.DISABLED)

    # clear the output content
    def clear(self):
        self.text_space.config(state=tk.NORMAL)
        self.text_space.delete('1.0', tk.END)

# main functionality controlled from here
class Main(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        # set window attributes
        self.geometry("500x800")
        self.title("Family Viewer")

        # create dict of frame elements, representing frame stack
        self.frames = {}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # add frame types to stack, creating 1 instance of each
        for frame in (MainMenu, PopulateMenu, EntryMenu, FilterMenu):
            f = frame(self)
            f.grid(row=0, column=0, sticky='nsew')
            self.frames[frame] = f
        self.switch(MainMenu)

    # change the frame in main view
    def switch(self, frame, label="", filter=""):
        f = self.frames[frame]
        if (frame==EntryMenu):
            f.setLabel(label)
            f.setFilter(filter)
        f.tkraise()
        f.redirect()

    # quit
    def callback(self):
        self.destroy()

    # populate .db file
    def populate(self):
        db.choice("Populate", "", "")

# parent class for each type of frame
class MenuFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # create subframes
        top_frame = tk.Frame(self, height = 40)
        self.mid_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        display_frame = tk.Frame(self)

        displayBox = tk.Text(display_frame, state=tk.DISABLED)
        self.redirector = StdRedirector(displayBox)

        displayBox.pack(side = 'bottom')

        top_frame.pack()
        self.mid_frame.pack()
        self.bottom_frame.pack()
        display_frame.pack()

    # redirect stdout and stderr
    def redirect(self):
        self.redirector.clear()
        sys.stdout = self.redirector
        sys.stderr = self.redirector


# first menu frame, inherits from MenuFrame
class MainMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        # create widgets
        search_button = ttk.Button(self.mid_frame, text = 'Search', width = 20, command = lambda: master.switch(FilterMenu))
        family_button = ttk.Button(self.mid_frame, text = 'Family', width = 20, command = lambda: master.switch(EntryMenu, "Enter full name", ""))
        populate_button = ttk.Button(self.mid_frame, text = 'Populate Database', width = 20, command = lambda: master.switch(PopulateMenu))
        quit_button = ttk.Button(self.bottom_frame, text = 'Quit', width = 15, command = master.callback)

        # place the widgets
        search_button.pack(side = 'top')
        family_button.pack(side = 'top')
        populate_button.pack(side = 'bottom')
        quit_button.pack(side = 'left')

# similar to above frame, with different buttons
class FilterMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        name_button = ttk.Button(self.mid_frame, text = 'Name', width = 20, command = lambda: master.switch(EntryMenu, "Enter name", "Name"))
        dob_button = ttk.Button(self.mid_frame, text = 'Birthdate', width = 20, command = lambda: master.switch(EntryMenu, "Enter birthday YYYY-MM-DD", "Birthday"))
        birthplace_button = ttk.Button(self.mid_frame, text = 'Birthplace', width = 20, command = lambda: master.switch(EntryMenu, "Enter birthplace", "Birthplace"))
        deathplace_button = ttk.Button(self.mid_frame, text = 'Deathplace', width = 20, command = lambda: master.switch(EntryMenu, "Enter deathplace", "Deathplace"))
        back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 15, command = lambda: master.switch(MainMenu))

        name_button.pack(side = 'top')
        dob_button.pack(side = 'top')
        birthplace_button.pack(side = 'top')
        deathplace_button.pack(side = 'top')
        back_button.pack(side = 'bottom')

# similar to above; directs populate functionality
class PopulateMenu(MenuFrame):
    # will add records to db from user input - need to delete this function and create another frame menu
    def addRecord(self):
        pass

    def delRecord(self):
        pass

    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        file_button = ttk.Button(self.mid_frame, text = 'Read from records.py', width = 20, command = master.populate)
        add_button = ttk.Button(self.mid_frame, text = 'Add record', width = 20, command = self.addRecord)
        delete_button = ttk.Button(self.mid_frame, text = 'Delete record', width = 20, command = self.delRecord)
        back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 15, command = lambda: master.switch(MainMenu))

        file_button.pack(side = 'top')
        add_button.pack(side = 'top')
        delete_button.pack(side = 'top')
        back_button.pack(side = 'bottom')

# this is the search frame - allows one text entry (may want to expand for add/delete)
class EntryMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        self.filter = ""
        self.master = master

        self.labelW = tk.Label(self.mid_frame)
        self.entryW = tk.Entry(self.mid_frame)

        self.submit_button = ttk.Button(self.mid_frame)
        self.back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 15)

        self.labelW.pack(side = 'left')
        self.entryW.pack(side = 'right')
        self.submit_button.pack(side = 'right')
        self.back_button.pack(side = 'bottom')

    # search db based on filters
    def search(self, filter):
        self.redirector.clear()
        db.choice("Search", self.filter, self.entryW.get())

    # display famlily of a person
    def family(self):
        self.redirector.clear()
        db.choice("Family", "", self.entryW.get())

    # update the label for the entry widget based on context
    def setLabel(self, label):
        self.entryW.delete('0', tk.END)
        self.labelW.config(text = label)
        self.labelW.update()

    # set the filter to send to the db search function
    def setFilter(self, filter):
        self.filter = filter
        if (self.filter==""):
            self.submit_button.config(text = 'Submit', command = self.family)
            self.back_button.config(command = lambda: self.master.switch(MainMenu))
        else:
            self.submit_button.config(text = 'Search', command = lambda: self.search(self.filter))
            self.back_button.config(command = lambda: self.master.switch(FilterMenu))

# main script - create a db object, start gui
db = familyDB.FamilyDB()
root = Main()
root.mainloop()
