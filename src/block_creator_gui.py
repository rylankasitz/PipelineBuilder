import os
import tkinter as tk
import pygubu
from tkinter import *
from tkinter import messagebox

UI_FILE = "block_editor.ui"

class Application():
    def __init__(self):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file(UI_FILE)

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('main_window')

        self.number_of_inputs = 1
        self.number_of_outputs = 1
    
    def add_input_entry(self):
        print("ADD")
        messagebox.showinfo('Message', 'You clicked Button 1')
    

        #show_lab = Label(builder.get_object('input_lb'), text='Shcoob', column=0, row=1)
        #show_lab.pack()

        #self.number_of_inputs += 1
        
        #setattr("input_ent_" + str(self.number_of_inputs),Entry(self)).pack()

        #all_entries.append( ent )

    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()
        
app = Application()
app.run()