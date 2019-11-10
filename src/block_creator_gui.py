import os
import tkinter as tk
import pygubu
from tkinter import *
from tkinter import messagebox
from src.configs import program_config
from src import json_loader

UI_FILE = "block_editor.ui"


class Application(pygubu.TkApplication):
    def _create_ui(self):
        
         #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file(UI_FILE)
  
        #3: Create the widget using self.master as parent
        self.mainwindow = builder.get_object('main_window', self.master)
        
        # Connect method callbacks
        builder.connect_callbacks(self)


        self.row_of_inputs = 1
        self.input_entry_list = []
        self.inputlb = self.builder.get_object('input_lb')
        self.input_entry_list.append( self.inputlb )

        self.row_of_outputs = 1
        self.output_entry_list = []
        self.outputlb = self.builder.get_object('output_lb')
        self.output_entry_list.append( self.outputlb )


    def add_input_entry(self):
        self.row_of_inputs += 1
        self.inputlb = self.builder.get_object('input_lb')
        this_input_entry = Entry(self.inputlb, width=80, relief="solid").grid(row=self.row_of_inputs)
        self.input_entry_list.append( this_input_entry )

    def add_output_entry(self):
        self.row_of_outputs += 1
        self.outputlb = self.builder.get_object('output_lb')
        this_output_entry = Entry(self.outputlb, width=80, relief="solid").grid(row=self.row_of_outputs)
        self.output_entry_list.append( this_output_entry )


    #def construct_blocks_json(self):



    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()
        
root = tk.Tk()
app = Application(root)
app.run()