import os
import tkinter as tk
import pygubu
from tkinter import *
from tkinter import messagebox
from configs.program_config import ProgramBlock
import json_loader
import utils

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
        #self.inputlb = self.builder.get_object('input_lb')
        #self.input_entry_list.append( self.inputlb )

        self.input_entry1 = self.builder.get_object('input_ent_1')
        self.input_entry_list.append( self.input_entry1 )


        self.row_of_outputs = 1
        self.output_entry_list = []
        #self.outputlb = self.builder.get_object('output_lb')
        #self.output_entry_list.append( self.outputlb )

        self.output_entry1 = self.builder.get_object('output_ent_1')
        self.output_entry_list.append( self.output_entry1 )


    def add_input_entry(self):
        self.row_of_inputs += 1
        self.inputlb = self.builder.get_object('input_lb')
        this_input_entry = Entry(self.inputlb, width=80, relief="solid")
        this_input_entry.grid(row=self.row_of_inputs)
        self.input_entry_list.append( this_input_entry )


    def add_output_entry(self):
        self.row_of_outputs += 1
        self.outputlb = self.builder.get_object('output_lb')
        this_output_entry = Entry(self.outputlb, width=80, relief="solid")
        this_output_entry.grid(row=self.row_of_outputs)
        self.output_entry_list.append( this_output_entry )


    def construct_blocks_json(self):

        #print(self.input_entry_list)
        #print(self.output_entry_list)

        new_block = ProgramBlock()
        #print((self.builder.get_object('name_ent')).get())
        new_block.name = self.builder.get_object('name_ent').get()
        new_block.command = self.builder.get_object('command_ent').get()
        new_block.inputs = [ a.get() for a in self.input_entry_list]
        prelim_outputs =  [ a.get() for a in self.output_entry_list]

        new_block.outputs = []
        prelim_output_types = {}
        for i in prelim_outputs:
            this_output_list = i.split('.')
            new_block.outputs.append(this_output_list[0])
            if len(this_output_list) == 1:
                prelim_output_types.update({this_output_list[0]:""})
            else:
                prelim_output_types.update({this_output_list[0]:this_output_list[1]})
        new_block.output_types = prelim_output_types

        prelim_sbatch_text = self.builder.get_object('sbatch_txtbox').get("1.0",END)

        new_block.sbatch = prelim_sbatch_text.splitlines()

        print("new_block.name:")
        print(new_block.name)
        print("new_block.command:")
        print(new_block.command)
        print("new_block.inputs:")
        print(new_block.inputs)
        print("new_block.outputs:")
        print(new_block.outputs)
        print("new_block.output_types:")
        print(new_block.output_types)
        print("new_block.sbatch:")
        print(new_block.sbatch)

        blocks = utils.get_blocks()
        blocks[new_block.name] = new_block
        json_loader.write_config("./../programs/blocks.json",blocks)



    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()
        
root = tk.Tk()
app = Application(root)
app.run()