import tkinter
import familyDB

class Screen:
    def __init__(self):
        self.db = familyDB.FamilyDB()
        #create root window
        self.root = tkinter.Tk()
        self.mainMenu()

    def clear(self):
        self.mid_frame.destroy()
        self.bottom_frame.destroy()
        self.root.quit()

    def initFrames(self):
        self.mid_frame = tkinter.Frame(self.root)
        self.bottom_frame = tkinter.Frame(self.root)

    def mainMenu(self):
        try:
            self.clear()
            self.top_frame.destroy()
        except: (AttributeError)
        self.top_frame = tkinter.Frame(self.root, height = 40)
        self.initFrames()
        #Create two labels
        self.search_button = tkinter.Button(self.mid_frame, text = 'Search', width = 20, command = self.filterMenu)
        self.family_button = tkinter.Button(self.mid_frame, text = 'Family', width = 20, command = lambda: self.entryMenu("Enter full name", ""))
        self.populate_button = tkinter.Button(self.mid_frame, text = 'Populate Database', width = 20, command = self.populate)
        #Pack top frame widgets
        self.search_button.pack(side = 'top')
        self.family_button.pack(side = 'top')
        self.populate_button.pack(side = 'bottom')
        #root.destroy exits/destroys the main window
        self.quit_button = tkinter.Button(self.bottom_frame, text = 'Quit', width = 15, command = self.root.destroy)
        #Pack the buttons
        self.quit_button.pack(side = 'left')

        #Now pack the frames also
        self.top_frame.pack()
        self.mid_frame.pack()
        self.bottom_frame.pack()
        self.root.mainloop()

    def filterMenu(self):
        self.clear()
        self.initFrames()

        self.name_button = tkinter.Button(self.mid_frame, text = 'Name', width = 20, command = lambda: self.entryMenu("Enter name", "Name"))
        self.dob_button = tkinter.Button(self.mid_frame, text = 'Birthdate', width = 20, command = lambda: self.entryMenu("Enter birthday YYYY-MM-DD", "Birthday"))
        self.birthplace_button = tkinter.Button(self.mid_frame, text = 'Birthplace', width = 20, command = lambda: self.entryMenu("Enter birthplace", "Birthplace"))
        self.deathplace_button = tkinter.Button(self.mid_frame, text = 'Deathplace', width = 20, command = lambda: self.entryMenu("Enter deathplace", "Deathplace"))
        self.back_button = tkinter.Button(self.bottom_frame, text = 'Return', width = 15, command = self.mainMenu)

        self.name_button.pack(side = 'top')
        self.dob_button.pack(side = 'top')
        self.birthplace_button.pack(side = 'top')
        self.deathplace_button.pack(side = 'top')
        self.back_button.pack(side = 'bottom')

        self.mid_frame.pack()
        self.bottom_frame.pack()
        self.root.mainloop()

    def entryMenu(self, label, filter):
        self.clear()
        self.initFrames()

        self.label = tkinter.Label(self.mid_frame, text = label)
        self.nameEntry = tkinter.Entry(self.mid_frame)
        if (filter==""):
            self.submit_button = tkinter.Button(self.mid_frame, text = 'Submit', command = self.family)
            self.back_button = tkinter.Button(self.bottom_frame, text = 'Return', width = 15, command = self.mainMenu)
        else:
            self.submit_button = tkinter.Button(self.mid_frame, text = 'Search', command = lambda: self.search(filter))
            self.back_button = tkinter.Button(self.bottom_frame, text = 'Return', width = 15, command = self.filterMenu)

        self.label.pack(side = 'left')
        self.nameEntry.pack(side = 'right')
        self.submit_button.pack(side = 'right')
        self.back_button.pack(side = 'bottom')

        self.mid_frame.pack()
        self.bottom_frame.pack()
        self.root.mainloop()

    def search(self, filter):
        self.db.choice("Search", filter, self.nameEntry.get())

    def family(self):
        self.db.choice("Family", "", self.nameEntry.get())

    def populate(self):
        self.db.choice("Populate", "", "")

gui = Screen()
