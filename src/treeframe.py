import tkinter as tk
from tkinter import ttk
import familyDB

class TreeFrame(tk.Tk):
    def __init__(self, title, family, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, width=1000)
        scrollbary = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        scrollbarx = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

        self.display_frame = tk.Frame(self.canvas)
        self.createTree(family)

        self.canvas.create_window((0,0), window=self.display_frame, anchor='nw', state='disabled')

        scrollbary.grid(row=0, column=1, sticky='nes')
        scrollbarx.grid(row=1, column=0, sticky='sew')
        self.canvas.grid(row=0, column=0, sticky='nswe')

        self.display_frame.bind("<Configure>", self.onFrameConfigure)


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def createTree(self, family):
        selfRecord = family[:1][0][0]
        grandparents = family[1]
        parents = family[2]
        siblings = family[3]
        spouses = family[4]
        children = family[5]

        if (len(grandparents) > 0):
            for i, person in enumerate(grandparents):
                col = [ 12, 14, 16, 18 ]
                frame = tk.LabelFrame(self.display_frame, text=person[1], font=("Helvetica", 10))
                message = "Born: " + person[2] + "\nDied: " + person[4] + "\nAge: " + str(person[6])
                text_box = tk.Text(frame, width=25, height=3, font=("Helvetica", 10))
                text_box.insert('end', message)
                text_box.configure(state='disabled')
                frame.grid(row=0, column=col[i])
                text_box.grid(sticky='news')

        if (len(parents) > 0):
            for i, person in enumerate(parents):
                col = [ 13, 17 ]
                frame = tk.LabelFrame(self.display_frame, text=person[1], font=("Helvetica", 10))
                message = "Born: " + person[2] + "\nDied: " + person[4] + "\nAge: " + str(person[6])
                text_box = tk.Text(frame, width=25, height=3, font=("Helvetica", 10))
                text_box.insert('end', message)
                text_box.configure(state='disabled')
                frame.grid(row=1, column=col[i])
                text_box.grid(sticky='news')

        start = 15 - int((len(siblings) / 2))
        offset = 0
        parent_start = 0
        if (len(siblings) == 0):
            siblings.append(selfRecord)
        for i, person in enumerate(siblings):
            frame = tk.LabelFrame(self.display_frame, text=person[1], font=("Helvetica", 10))
            message = "Born: " + person[2] + "\nDied: " + person[4] + "\nAge: " + str(person[6])
            text_box = tk.Text(frame, width=25, height=3, font=("Helvetica", 10))
            text_box.insert('end', message)
            text_box.configure(state='disabled')
            frame.grid(row=2, column=start+offset+i)
            text_box.grid(sticky='news')
            if (person[1] == selfRecord[1]):
                frame.configure(relief="solid")
                parent_start = start+offset+i
                for j, spouse in enumerate(spouses):
                    offset = j+1
                    frame2 = tk.LabelFrame(self.display_frame, text=spouse[1], font=("Helvetica", 10))
                    frame2.configure(relief="solid")
                    message2 = "Born: " + spouse[2] + "\nDied: " + spouse[4] + "\nAge: " + str(spouse[6])
                    text_box2 = tk.Text(frame2, width=25, height=3, font=("Helvetica", 10))
                    text_box2.insert('end', message2)
                    text_box2.configure(state='disabled')
                    frame2.grid(row=2, column=start+offset+i)
                    text_box2.grid(sticky='news')

        if (len(children) > 0):
            start = parent_start - int((len(children) / 2))
            for i, person in enumerate(children):
                frame = tk.LabelFrame(self.display_frame, text=person[1], font=("Helvetica", 10))
                message = "Born: " + person[2] + "\nDied: " + person[4] + "\nAge: " + str(person[6])
                text_box = tk.Text(frame, width=25, height=3, font=("Helvetica", 10))
                text_box.insert('end', message)
                text_box.configure(state='disabled')
                frame.grid(row=3, column=start+i)
                text_box.grid(sticky='news')
