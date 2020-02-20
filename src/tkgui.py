import tkinter as tk
from tkinter import ttk
import sys
import familyDB

# main functionality controlled from here
class Main(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        # set window attributes
        #self.geometry("1400x400")
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
        f.updateMessage("", "black")
        if (frame==EntryMenu):
            f.updateDisplay("")

    # quit
    def callback(self):
        self.destroy()

    # populate .db file
    def populate(self):
        string = db.choice("Populate", "", "")
        self.frames[MainMenu].updateMessage("\n".join([string[0], string[1]]), "green")

# parent class for each type of frame
class MenuFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # create subframes
        top_frame = tk.Frame(self, height = 20)     # @TODO - add header
        self.mid_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        self.display_frame = tk.Frame(self, height = 0)

        self.message_bar = tk.Label(self.bottom_frame)
        self.message_bar.pack(side = 'bottom')

        self.bottom_frame.pack(side = 'bottom')
        self.display_frame.pack(side = 'bottom')
        top_frame.pack(side = 'top')
        self.mid_frame.pack(side = 'top')

    def updateDisplay(self, results, grandparents=None, parents=None, children=None):
        self.display_box.delete(*self.display_box.get_children())
        if (grandparents != None):
            self.display_box.insert('', 'end', values=('-', '-----', '--GRANDPARENTS--', '------', '-'))
            for parent in grandparents:
                self.display_box.insert('', 'end', values=(parent[0], parent[1], parent[2], parent[3], parent[4]))
        if (parents != None):
            self.display_box.insert('', 'end', values=('-', '-----', '--PARENTS--', '------', '-'))
            for parent in parents:
                self.display_box.insert('', 'end', values=(parent[0], parent[1], parent[2], parent[3], parent[4]))
            self.display_box.insert('', 'end', values=('-', '-----', '--SIBLINGS--', '------', '-'))
        for data in results:
            self.display_box.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4]))
        if (children != None):
            self.display_box.insert('', 'end', values=('-', '-----', '--CHILDREN--', '-----', '-'))
            for child in children:            
                self.display_box.insert('', 'end', values=(child[0], child[1], child[2], child[3], child[4]))

    def updateMessage(self, string, color):
        self.message_bar.config(text=string, fg=color)


# first menu frame, inherits from MenuFrame
class MainMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        # create widgets
        search_button = ttk.Button(self.mid_frame, text = 'Search', width = 20, command = lambda: master.switch(FilterMenu))
        family_button = ttk.Button(self.mid_frame, text = 'Family', width = 20, command = lambda: master.switch(EntryMenu, "Enter full name", ""))
        populate_button = ttk.Button(self.mid_frame, text = 'Populate Database', width = 20, command = master.populate)
        quit_button = ttk.Button(self.bottom_frame, text = 'Quit', width = 20, command = master.callback)

        # place the widgets
        search_button.pack(side = 'top')
        family_button.pack(side = 'top')
        populate_button.pack(side = 'top')
        quit_button.pack(side = 'bottom')

# similar to above frame, with different buttons
class FilterMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        name_button = ttk.Button(self.mid_frame, text = 'Name', width = 20, command = lambda: master.switch(EntryMenu, "Enter name", "Name"))
        dob_button = ttk.Button(self.mid_frame, text = 'Birthdate', width = 20, command = lambda: master.switch(EntryMenu, "Enter birthday YYYY-MM-DD", "Birthday"))
        birthplace_button = ttk.Button(self.mid_frame, text = 'Birthplace', width = 20, command = lambda: master.switch(EntryMenu, "Enter birthplace", "Birthplace"))
        deathplace_button = ttk.Button(self.mid_frame, text = 'Deathplace', width = 20, command = lambda: master.switch(EntryMenu, "Enter deathplace", "Deathplace"))
        back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 20, command = lambda: master.switch(MainMenu))

        name_button.pack(side = 'top')
        dob_button.pack(side = 'top')
        birthplace_button.pack(side = 'top')
        deathplace_button.pack(side = 'top')
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
        self.back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 20)

        self.labelW.pack(side = 'left')
        self.entryW.pack(side = 'right')
        self.submit_button.pack(side = 'right')
        self.back_button.pack(side = 'bottom')

        self.display_frame.config(height=200)
        scrollbary = ttk.Scrollbar(self.display_frame, orient='vertical')
        scrollbarx = ttk.Scrollbar(self.display_frame, orient='horizontal')
        self.display_box = ttk.Treeview(self.display_frame, columns=("ID", "Name", "Born", "Died", "Age"), selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.display_box.yview)
        scrollbary.pack(side='right', fill='y')
        scrollbarx.config(command=self.display_box.xview)
        scrollbarx.pack(side='bottom', fill='x')
        self.display_box.heading('ID', text="ID", anchor='w')
        self.display_box.heading('Name', text="Name", anchor='w')
        self.display_box.heading('Born', text="Born", anchor='w')
        self.display_box.heading('Died', text="Died", anchor='w')
        self.display_box.heading('Age', text="Age", anchor='w')
        self.display_box.column('#0', minwidth=0, width=20)
        self.display_box.column('#1', minwidth=0, width=40)
        self.display_box.column('#2', minwidth=0, width=300)
        self.display_box.column('#3', minwidth=0, width=400)
        self.display_box.column('#4', minwidth=0, width=400)
        self.display_box.column('#5', minwidth=0, width=50)
        self.display_box.pack(side = 'bottom')

    # search db based on filters
    def search(self, filter):
        result = db.choice("Search", self.filter, self.entryW.get())
        if (result != None):
            self.updateDisplay(result)
            self.updateMessage("".join([str(len(result)), " record(s) found."]), "green")
        else:
            self.updateMessage("No results.", "red")

    # display famlily of a person
    def family(self):
        family = db.choice("Family", "", self.entryW.get())
        if (family != None):
            self.updateDisplay(family[2], family[0], family[1], family[3])
            self.updateMessage("".join([str(len(family[0]) + len(family[1]) + len(family[2]) + len(family[3])), " record(s) found."]), "green")
        else:
            self.updateMessage("That person was not found.", "red")

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
