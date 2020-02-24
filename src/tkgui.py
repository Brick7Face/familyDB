import tkinter as tk
from tkinter import ttk
import sys
import familyDB

# main functionality controlled from here
class Main(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        # set window attributes
        self.title("Family Viewer")
        self.geometry("300x200")

        # create dict of frame elements, representing frame stack
        self.frames = {}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # add frame types to stack, creating 1 instance of each
        for frame in (MainMenu, PopulateMenu, CreatePersonMenu, CreateMarriageMenu, EntryMenu, FilterMenu):
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
            f.updateDisplay("")
            self.geometry("1300x350")
        elif (frame==CreatePersonMenu):
            self.geometry("1300x525")
        elif (frame==CreateMarriageMenu):
            self.geometry("1300x400")
        else:
            self.geometry("300x200")
        f.tkraise()
        f.updateMessage("", "black")

    # quit
    def callback(self):
        self.destroy()

    # populate .db file
    def populate(self):
        string = db.choice("Populate", "", "")
        self.frames[PopulateMenu].updateMessage("\n".join([string[0], string[1]]), "green")

# parent class for each type of frame
class MenuFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # create subframes
        top_frame = tk.Frame(self, height = 20)     # @TODO - add header
        self.mid_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        self.display_frame = tk.Frame(self)

        self.top_bar = tk.Label(top_frame, text = '')
        self.message_bar = tk.Label(self.bottom_frame)
        self.top_bar.pack(side = 'top')
        self.message_bar.pack(side = 'bottom')

        self.bottom_frame.pack(side = 'bottom')
        self.display_frame.pack(side = 'bottom')
        top_frame.pack(side = 'top')
        self.mid_frame.pack(side = 'top')

    # Update the display_box with records
    def updateDisplay(self, results, grandparents=None, parents=None, spouse=None, children=None):
        self.display_box.delete(*self.display_box.get_children())
        if (grandparents != None and len(grandparents) > 0):
            self.display_box.insert('', 'end', values=('--', '----------', '----GRANDPARENTS----', '-----------', '--'))
            for parent in grandparents:
                self.display_box.insert('', 'end', values=(parent[0], parent[1], parent[2], parent[3], parent[4]))
        if (parents != None and len(parents) > 0):
            self.display_box.insert('', 'end', values=('--', '----------', '----PARENTS----', '-----------', '--'))
            for parent in parents:
                self.display_box.insert('', 'end', values=(parent[0], parent[1], parent[2], parent[3], parent[4]))
            if (len(results) > 0):
                self.display_box.insert('', 'end', values=('--', '----------', '----SIBLINGS----', '-----------', '--'))
        for data in results:
            self.display_box.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4]))
        if (spouse != None and len(spouse) > 0):
            self.display_box.insert('', 'end', values=('--', '----------', '----SPOUSE(S)----', '----------', '--'))
            for person in spouse:
                self.display_box.insert('', 'end', values=(person[0], person[1], person[2], person[3], person[4]))
        if (children != None and len(children) > 0):
            self.display_box.insert('', 'end', values=('--', '----------', '----CHILDREN----', '----------', '--'))
            for child in children:
                self.display_box.insert('', 'end', values=(child[0], child[1], child[2], child[3], child[4]))

    # Update bottom message box with status info
    def updateMessage(self, string, color):
        self.message_bar.config(text=string, fg=color)


# first menu frame, inherits from MenuFrame
class MainMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        # create widgets
        search_button = ttk.Button(self.mid_frame, text = 'Search', width = 15, command = lambda: master.switch(FilterMenu))
        family_button = ttk.Button(self.mid_frame, text = 'Find Family', width = 15, command = lambda: master.switch(EntryMenu, "Enter full name", ""))
        populate_button = ttk.Button(self.mid_frame, text = 'Populate Database', width = 15, command = lambda: master.switch(PopulateMenu))
        quit_button = ttk.Button(self.bottom_frame, text = 'Quit', width = 15, command = master.callback)

        # place the widgets
        search_button.pack(side = 'top')
        family_button.pack(side = 'top')
        populate_button.pack(side = 'top')
        quit_button.pack(side = 'bottom')

# menu for database manipulation
class PopulateMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        file_button = ttk.Button(self.mid_frame, text = 'Add Included Records', command = master.populate)
        edit_button = ttk.Menubutton(self.mid_frame, text = 'Add/Delete Record')
        options = tk.Menu(edit_button)
        edit_button.config(menu=options)
        options.add_command(label='Add Person', command = lambda: master.switch(CreatePersonMenu))
        options.add_command(label='Add Marriage', command = lambda: master.switch(CreateMarriageMenu))
        options.add_separator()
        options.add_command(label='Delete Person', command = lambda: master.switch(EntryMenu, "Enter full name", "Delete"))
        back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 15, command = lambda: master.switch(MainMenu))

        file_button.pack(side = 'top')
        edit_button.pack(side = 'top')
        back_button.pack(side = 'bottom')

# Parent class for creation menus, builds display_box
class CreateMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        self.submit_button = ttk.Button(self.mid_frame, text = 'Submit')
        self.back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 15, command = lambda: master.switch(PopulateMenu))

        self.back_button.pack(side = 'bottom')
        self.submit_button.pack(side = 'bottom')

        self.display_frame.config(height=100)
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
        self.display_box.column('#0', stretch=0, minwidth=0, width=0)
        self.display_box.column('#1', stretch=0, minwidth=0, width=40)
        self.display_box.column('#2', stretch=0, minwidth=0, width=300)
        self.display_box.column('#3', stretch=0, minwidth=0, width=400)
        self.display_box.column('#4', stretch=0, minwidth=0, width=400)
        self.display_box.column('#5', stretch=0, minwidth=0, width=50)
        self.display_box.pack(side = 'bottom')

# menu frame for creating a Person record, with entries
class CreatePersonMenu(CreateMenu):
    def __init__(self, master=None, **kwargs):
        CreateMenu.__init__(self, master, **kwargs)

        self.top_bar.config(text = "Create person record", fg = "blue")

        name_frame = tk.Frame(self.mid_frame)
        parent1_frame = tk.Frame(self.mid_frame)
        parent2_frame = tk.Frame(self.mid_frame)
        dob_frame = tk.Frame(self.mid_frame)
        dod_frame = tk.Frame(self.mid_frame)
        birthplace_frame = tk.Frame(self.mid_frame)
        deathplace_frame = tk.Frame(self.mid_frame)

        name_label = tk.Label(name_frame, text = "Enter name")
        parent1_label = tk.Label(parent1_frame, text = "Enter father")
        parent2_label = tk.Label(parent2_frame, text = "Enter mother")
        dob_label = tk.Label(dob_frame, text = "Enter DOB (YYYY-MM-DD)")
        dod_label = tk.Label(dod_frame, text = "Enter DOD (YYYY-MM-DD)")
        birthplace_label = tk.Label(birthplace_frame, text = "Enter birthplace")
        deathplace_label = tk.Label(deathplace_frame, text = "Enter deathplace")

        self.name_entry = tk.Entry(name_frame)
        self.parent1_entry = tk.Entry(parent1_frame)
        self.parent2_entry = tk.Entry(parent2_frame)
        self.dob_entry = tk.Entry(dob_frame, width = 9)
        self.dod_entry = tk.Entry(dod_frame, width = 9)
        self.birthplace_entry = tk.Entry(birthplace_frame)
        self.deathplace_entry = tk.Entry(deathplace_frame)

        name_label.pack(side = 'left')
        self.name_entry.pack(side = 'right')
        parent1_label.pack(side = 'left')
        self.parent1_entry.pack(side = 'right')
        parent2_label.pack(side = 'left')
        self.parent2_entry.pack(side = 'right')
        dob_label.pack(side = 'left')
        self.dob_entry.pack(side = 'right')
        dod_label.pack(side = 'left')
        self.dod_entry.pack(side = 'right')
        birthplace_label.pack(side = 'left')
        self.birthplace_entry.pack(side = 'right')
        deathplace_label.pack(side = 'left')
        self.deathplace_entry.pack(side = 'right')

        name_frame.pack(side = 'top')
        parent1_frame.pack(side = 'top')
        parent2_frame.pack(side = 'top')
        dob_frame.pack(side = 'top')
        dod_frame.pack(side = 'top')
        birthplace_frame.pack(side = 'top')
        deathplace_frame.pack(side = 'top')

        self.submit_button.config(command = self.createPerson)

    # fetch entries, build record in DB class
    def createPerson(self):
        personEntries = [ self.name_entry.get(), self.parent1_entry.get(), self.parent2_entry.get(), self.dob_entry.get(), self.dod_entry.get(), self.birthplace_entry.get(), self.deathplace_entry.get() ]
        result = db.create("Person", personEntries)
        if (len(result) > 0):
            self.updateDisplay(result)
            self.updateMessage("Person created successfully.", "green")

# menu frame for creating a Marriage record, with entries
class CreateMarriageMenu(CreateMenu):
    def __init__(self, master=None, **kwargs):
        CreateMenu.__init__(self, master, **kwargs)

        self.top_bar.config(text = "Create marriage record", fg = "blue")

        parent1_frame = tk.Frame(self.mid_frame)
        parent2_frame = tk.Frame(self.mid_frame)
        date_frame = tk.Frame(self.mid_frame)

        parent1_label = tk.Label(parent1_frame, text = "Enter father")
        parent2_label = tk.Label(parent2_frame, text = "Enter mother")
        date_label = tk.Label(date_frame, text = "Enter marriage date (YYYY-MM-DD)")

        self.parent1_entry = tk.Entry(parent1_frame)
        self.parent2_entry = tk.Entry(parent2_frame)
        self.date_entry = tk.Entry(date_frame, width = 9)

        parent1_label.pack(side = 'left')
        self.parent1_entry.pack(side = 'right')
        parent2_label.pack(side = 'left')
        self.parent2_entry.pack(side = 'right')
        date_label.pack(side = 'left')
        self.date_entry.pack(side = 'right')

        parent1_frame.pack(side = 'top')
        parent2_frame.pack(side = 'top')
        date_frame.pack(side = 'top')

        self.submit_button.config(command = self.createMarriage)

    # fetch entries, build record in DB class
    def createMarriage(self):
        marriageEntries = [ self.parent1_entry.get(), self.parent2_entry.get(), self.date_entry.get() ]
        result = db.create("Marriage", marriageEntries)
        if (len(result) > 0):
            self.updateDisplay(result)
            self.updateMessage("Marriage created successfully.", "green")

# menu frame for picking search filter
class FilterMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        self.top_bar.config(text = "Filter search by:")

        name_button = ttk.Button(self.mid_frame, text = 'Name', width = 15, command = lambda: master.switch(EntryMenu, "Enter name: ", "Name"))
        dob_button = ttk.Button(self.mid_frame, text = 'Birthdate', width = 15, command = lambda: master.switch(EntryMenu, "Enter birthday (YYYY-MM-DD): ", "Birthday"))
        birthplace_button = ttk.Button(self.mid_frame, text = 'Birthplace', width = 15, command = lambda: master.switch(EntryMenu, "Enter birthplace: ", "Birthplace"))
        deathplace_button = ttk.Button(self.mid_frame, text = 'Deathplace', width = 15, command = lambda: master.switch(EntryMenu, "Enter deathplace: ", "Deathplace"))
        back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 15, command = lambda: master.switch(MainMenu))

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
        self.back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 15)

        self.labelW.pack(side = 'left')
        self.entryW.pack(side = 'left')
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
        self.display_box.column('#0', stretch=0, minwidth=0, width=0)
        self.display_box.column('#1', stretch=0, minwidth=0, width=40)
        self.display_box.column('#2', stretch=0, minwidth=0, width=300)
        self.display_box.column('#3', stretch=0, minwidth=0, width=400)
        self.display_box.column('#4', stretch=0, minwidth=0, width=400)
        self.display_box.column('#5', stretch=0, minwidth=0, width=50)
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
            self.updateDisplay(family[2], family[0], family[1], family[3], family[4])
            self.updateMessage("".join([str(len(family[0]) + len(family[1]) + len(family[2]) + len(family[3])), " record(s) found."]), "green")
        else:
            self.updateMessage("That person was not found.", "red")

    # delete a Person record
    def delete(self):
        success = db.delete(self.entryW.get())
        if (success):
            self.updateMessage("".join([self.entryW.get(), " was deleted successfully."]), "green")
        else:
            self.updateMessage("".join([self.entryW.get(), " was not found."]), "red")

    # update the label for the entry widget based on context
    def setLabel(self, label):
        self.entryW.delete('0', tk.END)
        self.labelW.config(text = label)
        self.labelW.update()

    # set the filter to send to the db search function
    def setFilter(self, filter):
        self.filter = filter
        if (self.filter==""):
            self.top_bar.config(text = "Search for family", fg ="blue")
            self.submit_button.config(text = 'Submit', command = self.family)
            self.back_button.config(command = lambda: self.master.switch(MainMenu))
        elif (self.filter=="Delete"):
            self.top_bar.config(text = "Delete person", fg ="blue")
            self.submit_button.config(text = 'Submit', command = self.delete)
            self.back_button.config(command = lambda: self.master.switch(PopulateMenu))
        else:
            self.top_bar.config(text = "Search for person by " + filter.lower(), fg = "blue")
            self.submit_button.config(text = 'Search', command = lambda: self.search(self.filter))
            self.back_button.config(command = lambda: self.master.switch(FilterMenu))

# main script - create a db object, start gui
db = familyDB.FamilyDB()
root = Main()
root.mainloop()
