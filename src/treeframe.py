import tkinter as tk
from tkinter import ttk
import familyDB

class TreeFrame(tk.Tk):
    def __init__(self, title, family, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        self.title(title)

        display_frame = tk.Frame(self)

        for i, personList in enumerate(family[1:]):
            lastCol = 0
            if (len(personList) > 0):
                for j, person in enumerate(personList):
                    lf = tk.LabelFrame(display_frame, text=person[1])
                    message = "Born:\t" + person[2] + "\n>" + person[3] + "\nDied:\t" + person[4]
                    if (person[5] != ""):
                        message = message + "\n>" + person[5]
                    message = message + "\nAge:\t" + str(person[6])
                    lfc = tk.Label(lf, text=message, justify='left')
                    lf.grid(row=i, column=j, sticky='nw')
                    lfc.grid(row=i, column=j, sticky='nw')
                    lastCol = j+1
            if (i == 3):
                person = family[:1][0][0]
                lf = tk.LabelFrame(display_frame, text=person[1])
                message = "Born:\t" + person[2] + "\n>" + person[3] + "\nDied:\t" + person[4]
                if (person[5] != ""):
                    message = message + "\n>" + person[5]
                message = message + "\nAge:\t" + str(person[6])
                lfc = tk.Label(lf, text=message, justify='left')
                lf.grid(row=i, column=lastCol, sticky='nw')
                lfc.grid(row=i, column=lastCol, sticky='nw')

        display_frame.grid()
