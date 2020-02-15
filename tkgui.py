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
        self.geometry("500x500")
        self.title("Family Viewer")

        # create dict of frame elements, representing frame stack
        self.frames = {}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # add frame types to stack, creating 1 instance of each
        for frame in (MainMenu, EntryMenu, FilterMenu):
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

# first menu frame, inherits from tk.Frame
class MainMenu(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # create subframes
        top_frame = tk.Frame(self, height = 40)
        mid_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)
        display_frame = tk.Frame(self)

        # create widgets
        search_button = ttk.Button(mid_frame, text = 'Search', width = 20, command = lambda: master.switch(FilterMenu))
        family_button = ttk.Button(mid_frame, text = 'Family', width = 20, command = lambda: master.switch(EntryMenu, "Enter full name", ""))
        populate_button = ttk.Button(mid_frame, text = 'Populate Database', width = 20, command = master.populate)
        quit_button = ttk.Button(bottom_frame, text = 'Quit', width = 15, command = master.callback)
        displayBox = tk.Text(display_frame, state=tk.DISABLED)

        # create output
        self.redirector = StdRedirector(displayBox)

        # place the widgets
        search_button.pack(side = 'top')
        family_button.pack(side = 'top')
        populate_button.pack(side = 'bottom')
        quit_button.pack(side = 'left')
        displayBox.pack(side = 'bottom')

        # place the subframes
        top_frame.pack()
        mid_frame.pack()
        bottom_frame.pack()
        display_frame.pack()

    # redirect stdout and stderr
    def redirect(self):
        self.redirector.clear()
        sys.stdout = self.redirector
        sys.stderr = self.redirector

# similar to above frame, with different buttons
class FilterMenu(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        top_frame = tk.Frame(self, height = 40)
        mid_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)
        display_frame = tk.Frame(self)

        name_button = ttk.Button(mid_frame, text = 'Name', width = 20, command = lambda: master.switch(EntryMenu, "Enter name", "Name"))
        dob_button = ttk.Button(mid_frame, text = 'Birthdate', width = 20, command = lambda: master.switch(EntryMenu, "Enter birthday YYYY-MM-DD", "Birthday"))
        birthplace_button = ttk.Button(mid_frame, text = 'Birthplace', width = 20, command = lambda: master.switch(EntryMenu, "Enter birthplace", "Birthplace"))
        deathplace_button = ttk.Button(mid_frame, text = 'Deathplace', width = 20, command = lambda: master.switch(EntryMenu, "Enter deathplace", "Deathplace"))
        back_button = ttk.Button(bottom_frame, text = 'Return', width = 15, command = lambda: master.switch(MainMenu))
        displayBox = tk.Text(display_frame, state=tk.DISABLED)

        self.redirector = StdRedirector(displayBox)

        name_button.pack(side = 'top')
        dob_button.pack(side = 'top')
        birthplace_button.pack(side = 'top')
        deathplace_button.pack(side = 'top')
        back_button.pack(side = 'bottom')
        displayBox.pack(side = 'bottom')

        top_frame.pack()
        mid_frame.pack()
        bottom_frame.pack()
        display_frame.pack()

    def redirect(self):
        self.redirector.clear()
        sys.stdout = self.redirector
        sys.stderr = self.redirector

# similar to above, but this is the search frame
class EntryMenu(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.filter = ""
        self.master = master

        top_frame = tk.Frame(self, height = 40)
        mid_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)
        display_frame = tk.Frame(self)

        self.labelW = tk.Label(mid_frame)
        self.entryW = tk.Entry(mid_frame)

        self.submit_button = ttk.Button(mid_frame)
        self.back_button = ttk.Button(bottom_frame, text = 'Return', width = 15)
        displayBox = tk.Text(display_frame, state=tk.DISABLED)

        self.redirector = StdRedirector(displayBox)

        self.labelW.pack(side = 'left')
        self.entryW.pack(side = 'right')
        self.submit_button.pack(side = 'right')
        self.back_button.pack(side = 'bottom')
        displayBox.pack(side = 'bottom')

        top_frame.pack()
        mid_frame.pack()
        bottom_frame.pack()
        display_frame.pack()

    # search db based on filters
    def search(self, filter):
        db.choice("Search", self.filter, self.entryW.get())

    # display famlily of a person
    def family(self):
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

    def redirect(self):
        self.redirector.clear()
        sys.stdout = self.redirector
        sys.stderr = self.redirector

# main script - create a db object, start gui
db = familyDB.FamilyDB()
root = Main()
root.mainloop()
