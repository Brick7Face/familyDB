import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys, re
import familyDB, treeframe

# main functionality controlled from here
class Main(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        # set window attributes
        self.title("Family Viewer")
        self.resizable(0,0)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        f = MainMenu(self)
        f.grid(row=0, column=0, sticky='n')
        self.currentFrame = f

    # change the frame in main view
    def switch(self, frame, label="", filter="", id_num=""):
        self.currentFrame.destroy()
        f = frame(self)
        self.currentFrame = f
        f.grid(row=0, column=0, sticky='n')
        if (frame == EntryMenu):
            f.setLabel(label)
            f.setFilter(filter)
            f.updateDisplay("")
        elif (frame == EditPersonMenu):
            f.updateDefaults(id_num, label, filter)

    # populate .db file
    def populate(self):
        string = db.choice("Populate", "", "")
        self.currentFrame.updateMessage("\n".join([string[0], string[1]]), string[2])

    def clearDB(self):
        ans = messagebox.askokcancel("Confirm Delete", "Are you sure you want to purge the database?")
        if ans:
            db.choice("ClearDB", "", "")
            self.currentFrame.updateMessage("All records deleted.", "blue")


# parent class for each type of frame
class MenuFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # create subframes
        top_frame = tk.Frame(self)
        self.mid_frame = tk.Frame(self)
        self.submit_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        self.display_frame = tk.Frame(self)

        self.top_bar = tk.Label(top_frame)
        self.message_bar = tk.Label(self.bottom_frame)
        self.top_bar.grid(sticky='n')
        self.message_bar.grid(sticky='s')

        top_frame.grid(row=0, sticky='n')
        self.mid_frame.grid(row=1, sticky='n')
        self.submit_frame.grid(row=2, sticky='n')
        self.display_frame.grid(row=3, sticky='n')
        self.bottom_frame.grid(row=4, sticky='s')

    # Update the display_box with records
    def updateDisplay(self, results):
        self.display_box.delete(*self.display_box.get_children())
        filtered = []
        for record in results:
            if (record not in filtered):
                filtered.append(record)
        if (len(filtered) > 0):
            self.updateMessage("".join([str(len(filtered)), " record(s) found."]), "green")
        for data in filtered:
            self.display_box.insert('', 'end', values=(data[0], data[1], " ".join([data[2], data[3]]), " ".join([data[4], data[5]]), data[6]))

    # Update bottom message box with status info
    def updateMessage(self, string, color):
        self.message_bar.config(text=string, fg=color)


# first menu frame, inherits from MenuFrame
class MainMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        # create widgets
        search_button = ttk.Button(self.mid_frame, text = 'Search', width = 20, command = lambda: master.switch(FilterMenu))
        populate_button = ttk.Button(self.mid_frame, text = 'Populate Database', width = 20, command = lambda: master.switch(PopulateMenu))
        quit_button = ttk.Button(self.bottom_frame, text = 'Quit', width = 20, command = master.destroy)

        # place the widgets
        search_button.grid()
        populate_button.grid()
        quit_button.grid()

# menu for database manipulation
class PopulateMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        file_button = ttk.Button(self.mid_frame, text = 'Add Included Records', width = 20, command = master.populate)
        edit_button = ttk.Menubutton(self.mid_frame, text = 'Add/Delete Record')
        delete_button = ttk.Button(self.mid_frame, text = 'Delete All Records', width = 20, command = master.clearDB)
        options = tk.Menu(edit_button)
        edit_button.config(menu=options)
        options.add_command(label='Add Person', command = lambda: master.switch(CreatePersonMenu))
        options.add_command(label='Add Marriage', command = lambda: master.switch(CreateMarriageMenu))
        options.add_separator()
        options.add_command(label='Delete Person', command = lambda: master.switch(EntryMenu, "Enter name", "Delete"))
        back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 20, command = lambda: master.switch(MainMenu))

        file_button.grid(sticky='n')
        edit_button.grid(sticky='n')
        delete_button.grid(sticky='n')
        back_button.grid()

# Parent class for creation menus, builds display_box
class DisplayMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        self.submit_button = ttk.Button(self.submit_frame)
        self.option_button = ttk.Button(self.submit_frame, state='disabled')
        self.back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 20)

        self.submit_button.grid(row=0, column=0, sticky='n')
        self.option_button.grid(row=0, column=1, sticky='n')
        self.back_button.grid(sticky='s')

        #self.display_frame.config(height=100)
        scrollbary = ttk.Scrollbar(self.display_frame, orient='vertical')
        self.display_box = ttk.Treeview(self.display_frame, columns=("ID", "Name", "Born", "Died", "Age"), selectmode="browse", yscrollcommand=scrollbary.set)
        scrollbary.config(command=self.display_box.yview)
        scrollbary.grid(column=1, sticky='ns')
        headings = [ 'ID', 'Name', 'Born', 'Died', 'Age' ]
        for i in range(5):
            self.display_box.heading(headings[i], text=headings[i], anchor='w', command=lambda _col=headings[i]: self.sortColumn(self.display_box, _col, False))
        widths = [ 0, 40, 300, 400, 400, 50 ]
        for i in range(6):
            self.display_box.column('#' + str(i), stretch=0, minwidth=0, width=widths[i])
        self.display_box.grid(row=0)

        self.display_box.bind('<<TreeviewSelect>>', self.enableOptions)
        self.display_box.bind('<<TreeviewOpen>>', self.openRecord)

    def search(self, filter, record):
        self.option_button.config(state='disabled')
        result = db.choice("Search", filter, record)
        if (result != None):
            self.updateDisplay(result)
        else:
            self.updateDisplay([])
            self.updateMessage("No results.", "red")

    def searchMultiple(self, names):
        results = []
        for name in names:
            result = None
            try:
                result = db.choice("Search", "ID", int(name))
            except ValueError:
                result = db.choice("Search", "Name", name)
            if (result != None):
                results = results + result
        if (len(results) > 0):
            self.updateDisplay(results)
        else:
            self.updateDisplay([])
            self.updateMessage("No results.", "red")

    def enableOptions(self, *args):
        self.option_button.config(state='enabled')

    def openRecord(self, *args):
        selection = self.display_box.selection()
        vals = self.display_box.item(selection).get("values")
        family = db.relate(vals[0])
        treeframe.TreeFrame(vals[1] + "\'s Family Tree", family)

    # When clicked on, a column will sort itself
    def sortColumn(self, display_box, column, reverse):
        rows = []
        for row in display_box.get_children(''):
            if (column == 'ID' or column == 'Age'):
                # cast to integer for numbered columns
                if (display_box.set(row, column) == 'None'):
                    rows.append([0, row])
                else:
                    rows.append([int(display_box.set(row, column)), row])
            else:
                rows.append([display_box.set(row, column), row])
        # Don't reverse order the first click
        rows.sort(reverse=reverse)
        for index, (val, row) in enumerate(rows):
            display_box.move(row, '', index)
        # Second time, reverse order
        display_box.heading(column, command=lambda _col=column: self.sortColumn(display_box, _col, not reverse))

# menu frame for creating a Person record, with entries
class CreatePersonMenu(DisplayMenu):
    def __init__(self, master=None, **kwargs):
        DisplayMenu.__init__(self, master, **kwargs)

        self.top_bar.config(text = "Create person record", fg = "blue")
        self.option_button.config(text = 'Create', state='enabled', command = self.createPerson)
        self.back_button.config(command = lambda: master.switch(PopulateMenu))

        name_label = tk.Label(self.mid_frame, text = "Enter name")
        parent1_label = tk.Label(self.mid_frame, text = "Enter father name or ID")
        parent2_label = tk.Label(self.mid_frame, text = "Enter mother name or ID")
        dob_label = tk.Label(self.mid_frame, text = "Enter DOB (YYYY-MM-DD)")
        dod_label = tk.Label(self.mid_frame, text = "Enter DOD (YYYY-MM-DD)")
        birthplace_label = tk.Label(self.mid_frame, text = "Enter birthplace")
        deathplace_label = tk.Label(self.mid_frame, text = "Enter deathplace")

        self.name_entry = tk.Entry(self.mid_frame)
        self.parent1_entry = tk.Entry(self.mid_frame)
        self.parent2_entry = tk.Entry(self.mid_frame)
        self.dob_entry = tk.Entry(self.mid_frame, width = 9)
        self.dod_entry = tk.Entry(self.mid_frame, width = 9)
        self.birthplace_entry = tk.Entry(self.mid_frame)
        self.deathplace_entry = tk.Entry(self.mid_frame)

        name_label.grid(row=0, column=0, sticky='w')
        self.name_entry.grid(row=0, column=1, sticky='e')
        parent1_label.grid(row=1, column=0, sticky='w')
        self.parent1_entry.grid(row=1, column=1, sticky='e')
        parent2_label.grid(row=2, column=0, sticky='w')
        self.parent2_entry.grid(row=2, column=1, sticky='e')
        dob_label.grid(row=3, column=0, sticky='w')
        self.dob_entry.grid(row=3, column=1, sticky='e')
        dod_label.grid(row=4, column=0, sticky='w')
        self.dod_entry.grid(row=4, column=1, sticky='e')
        birthplace_label.grid(row=5, column=0, sticky='w')
        self.birthplace_entry.grid(row=5, column=1, sticky='e')
        deathplace_label.grid(row=6, column=0, sticky='w')
        self.deathplace_entry.grid(row=6, column=1, sticky='e')

        self.submit_button.config(text = 'Search', command = lambda: self.searchMultiple([ self.name_entry.get(), self.parent1_entry.get(), self.parent2_entry.get() ]))

    # fetch entries, build record in DB class
    def createPerson(self):
        dob = None
        birthplace = None
        if (self.name_entry.get().strip() == ""):
            self.updateMessage("Name cannot be empty.", "red")
            return
        if (self.dob_entry.get().strip() == ""):
            dob = "0000-00-00"
        elif not (re.match(r"\d\d\d\d-\d\d-\d\d", self.dob_entry.get())):
            self.updateMessage("DOB is not formatted correctly.", "red")
            return
        else:
            dob = self.dob_entry.get()
        if not (self.dod_entry.get().strip() == "") and not (re.match(r"\d\d\d\d-\d\d-\d\d", self.dod_entry.get())):
            self.updateMessage("DOD is not formatted correctly.", "red")
            return
        personEntries = [ self.name_entry.get(), self.parent1_entry.get(), self.parent2_entry.get(), dob, self.dod_entry.get(), self.birthplace_entry.get(), self.deathplace_entry.get() ]
        result = db.createOrUpdate("Person", personEntries, True)
        if (len(result) > 0):
            self.updateDisplay(result)
            self.updateMessage("Person created successfully.", "green")
        else:
            self.updateMessage("Marriage record for parents not found.\nTry creating a marriage record first.", "red")

class EditPersonMenu(CreatePersonMenu):
    def __init__(self, master=None, **kwargs):
        CreatePersonMenu.__init__(self, master, **kwargs)

        self.option_button.config(text = 'Update', state='enabled', command = self.updatePerson)
        self.id_num = None

    def updateDefaults(self, id_num, label, filter):
        self.top_bar.config(text = "Edit record", fg = "blue")
        self.back_button.config(command = lambda: self.master.switch(EntryMenu, label, filter))

        record = db.relate(id_num)

        self.id_num = record[0][0][0]

        self.name_entry.insert(0, record[0][0][1])
        self.parent1_entry.delete(0, 'end')
        if (record[2][0][1] == 'Unknown'):
            record[2][0][1] = ''
        self.parent1_entry.insert(0, record[2][0][1])
        self.parent2_entry.delete(0, 'end')
        if (record[2][1][1] == 'Unknown'):
            record[2][1][1] = ''
        self.parent2_entry.insert(0, record[2][1][1])
        self.dob_entry.delete(0, 'end')
        if (record[0][0][2] == '0000-00-00'):
            record[0][0][2] = ''
        self.dob_entry.insert(0, record[0][0][2])
        self.dod_entry.delete(0, 'end')
        if (record[0][0][4] == 'Alive'):
            record[0][0][4] = ''
        self.dod_entry.insert(0, record[0][0][4])
        self.birthplace_entry.delete(0, 'end')
        self.birthplace_entry.insert(0, record[0][0][3])
        self.deathplace_entry.delete(0, 'end')
        self.deathplace_entry.insert(0, record[0][0][5])

    def updatePerson(self):
        dob = None
        if (self.name_entry.get().strip() == ""):
            self.updateMessage("Name cannot be empty.", "red")
            return
        if (self.dob_entry.get().strip() == ""):
            dob = "0000-00-00"
        elif not (re.match(r"\d\d\d\d-\d\d-\d\d", self.dob_entry.get())):
            self.updateMessage("DOB is not formatted correctly.", "red")
            return
        else:
            dob = self.dob_entry.get()
        if not (self.dod_entry.get().strip() == "") and not (re.match(r"\d\d\d\d-\d\d-\d\d", self.dod_entry.get())):
            self.updateMessage("DOD is not formatted correctly.", "red")
            return
        personEntries = [ self.name_entry.get(), self.parent1_entry.get(), self.parent2_entry.get(), dob, self.dod_entry.get(), self.birthplace_entry.get(), self.deathplace_entry.get(), self.id_num ]
        result = db.createOrUpdate("Person", personEntries, False)
        if (len(result) > 0):
            self.updateDisplay(result)
            self.updateMessage(" ".join([self.name_entry.get(), "updated successfully."]), "green")
        else:
            self.updateMessage("Marriage record for parents not found.\nTry creating a marriage record first.", "red")


# menu frame for creating a Marriage record, with entries
class CreateMarriageMenu(DisplayMenu):
    def __init__(self, master=None, **kwargs):
        DisplayMenu.__init__(self, master, **kwargs)

        self.top_bar.config(text = "Create marriage record", fg = "blue")
        self.option_button.config(text = 'Create', state='enabled', command = self.createMarriage)
        self.back_button.config(command = lambda: master.switch(PopulateMenu))

        parent1_label = tk.Label(self.mid_frame, text = "Enter father name or ID")
        parent2_label = tk.Label(self.mid_frame, text = "Enter mother name or ID")
        date_label = tk.Label(self.mid_frame, text = "Enter marriage date (YYYY-MM-DD)")

        self.parent1_entry = tk.Entry(self.mid_frame)
        self.parent2_entry = tk.Entry(self.mid_frame)
        self.date_entry = tk.Entry(self.mid_frame, width = 9)

        parent1_label.grid(row=0, column=0, sticky='w')
        self.parent1_entry.grid(row=0, column=1, sticky='e')
        parent2_label.grid(row=1, column=0, sticky='w')
        self.parent2_entry.grid(row=1, column=1, sticky='e')
        date_label.grid(row=2, column=0, sticky='w')
        self.date_entry.grid(row=2, column=1, sticky='e')

        self.submit_button.config(text = 'Search', command = lambda: self.searchMultiple([ self.parent1_entry.get(), self.parent2_entry.get() ]))

    # fetch entries, build record in DB class
    def createMarriage(self):
        if (self.parent1_entry.get().strip() == ""):
            self.updateMessage("Father cannot be empty.", "red")
            return
        if (self.parent2_entry.get().strip() == ""):
            self.updateMessage("Mother cannot be empty.", "red")
            return
        if not (self.date_entry.get().strip() == "") and not (re.match(r"\d\d\d\d-\d\d-\d\d", self.date_entry.get())):
            self.updateMessage("Date is not formatted correctly.", "red")
            return
        marriageEntries = [ self.parent1_entry.get(), self.parent2_entry.get(), self.date_entry.get() ]
        result = db.createOrUpdate("Marriage", marriageEntries, True)
        if (len(result) > 0):
            self.updateDisplay(result)
            self.updateMessage("Marriage created successfully.", "green")
        else:
            self.updateMessage("Entries were incorrect.\nMake sure the name or ID is exact.", "red")

# menu frame for picking search filter
class FilterMenu(MenuFrame):
    def __init__(self, master=None, **kwargs):
        MenuFrame.__init__(self, master, **kwargs)

        self.top_bar.config(text = "Filter search by:")

        name_button = ttk.Button(self.mid_frame, text = 'Name', width = 20, command = lambda: master.switch(EntryMenu, "Enter name: ", "Name"))
        dob_button = ttk.Button(self.mid_frame, text = 'Birthdate', width = 20, command = lambda: master.switch(EntryMenu, "Enter birthday (YYYY-MM-DD): ", "Birthday"))
        birthplace_button = ttk.Button(self.mid_frame, text = 'Birthplace', width = 20, command = lambda: master.switch(EntryMenu, "Enter birthplace: ", "Birthplace"))
        deathplace_button = ttk.Button(self.mid_frame, text = 'Deathplace', width = 20, command = lambda: master.switch(EntryMenu, "Enter deathplace: ", "Deathplace"))
        back_button = ttk.Button(self.bottom_frame, text = 'Return', width = 20, command = lambda: master.switch(MainMenu))

        name_button.grid()
        dob_button.grid()
        birthplace_button.grid()
        deathplace_button.grid()
        back_button.grid()

# this is the search frame - allows one text entry (may want to expand for add/delete)
class EntryMenu(DisplayMenu):
    def __init__(self, master=None, **kwargs):
        DisplayMenu.__init__(self, master, **kwargs)

        self.filter = ""
        self.label = ""
        self.master = master

        self.labelW = tk.Label(self.mid_frame)
        self.entryW = tk.Entry(self.mid_frame)

        self.labelW.grid(row=0, column=0, sticky='w')
        self.entryW.grid(row=0, column=1, sticky='e')

    # delete a Person record
    def delete(self):
        selection = self.display_box.selection()
        vals = self.display_box.item(selection).get("values")
        ans = messagebox.askokcancel("Confirm Delete", "Are you sure you want to delete " + vals[1] + "?")
        if ans:
            result = db.delete(vals[0])
            if (len(result) > 0):
                self.display_box.delete(self.display_box.selection())
                self.updateMessage("".join([vals[1], " was deleted successfully."]), "green")
                self.option_button.config(state='disabled')
            else:
                self.updateMessage("".join([vals[1], " was not found."]), "red")

    # update the label for the entry widget based on context
    def setLabel(self, label):
        self.label = label
        self.entryW.delete('0', tk.END)
        self.labelW.config(text = self.label)
        self.labelW.update()

    # set the filter to send to the db search function
    def setFilter(self, filter):
        self.filter = filter
        if (self.filter=="Delete"):
            self.top_bar.config(text = "Delete person", fg ="blue")
            self.submit_button.config(text = 'Search', command = lambda: self.search("Name", self.entryW.get()))
            self.back_button.config(command = lambda: self.master.switch(PopulateMenu))
            self.option_button.config(text = "Delete", command = self.delete)
        else:
            self.top_bar.config(text = "Search for person by " + filter.lower(), fg = "blue")
            self.submit_button.config(text = 'Search', command = lambda: self.search(self.filter, self.entryW.get()))
            self.back_button.config(command = lambda: self.master.switch(FilterMenu))

            self.option_button.destroy()
            self.option_button = ttk.Menubutton(self.submit_frame, text = 'Options', state='disabled')
            options = tk.Menu(self.option_button)
            self.option_button.config(menu=options)
            options.add_command(label='View Family Tree', command = self.openRecord)
            options.add_command(label='Edit Record', command = lambda: self.master.switch(EditPersonMenu, self.label, self.filter, self.display_box.item(self.display_box.selection()).get("values")[0]))
            options.add_separator()
            options.add_command(label='Delete Record', command = self.delete)
            self.option_button.grid(row=0, column=1, sticky='n')

# main script - create a db object, start gui
db = familyDB.FamilyDB()
root = Main()
root.mainloop()
