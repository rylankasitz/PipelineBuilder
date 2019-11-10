import tkinter as tk
import tkinter.filedialog
from tkinter.constants import *

import tkinter.ttk as ttk
import json_loader

import configs.program_config as programBlockConfig
import functools
import enum

class BlockElementConnect(tk.Frame):
    def __init__(self, parent, color):
        tk.Frame.__init__(self, parent, bg=color, width=5)
        self.parent = parent

        self.bind('<ButtonPress-1>', self.press)
        self.bind('<ButtonRelease-1>', self.release)

    def press(self, event):
        print("asdf")

    def release(self, event):
        print("asdf")

class BlockElement(tk.Frame):
    class Types(enum.Enum):
        Input = 1
        Output = 2
        Title = 3

    def __init__(self, parent, text_in, element_type):
        tk.Frame.__init__(self, parent, bg='blue')

        if element_type == BlockElement.Types.Title:
            left_color = 'white'
            right_color = 'white'
        elif element_type == BlockElement.Types.Input:
            left_color = 'green'
            right_color = 'white'
        elif element_type == BlockElement.Types.Output:
            left_color = 'white'
            right_color = 'red'

        connector_left = BlockElementConnect(self, left_color)
        connector_left.grid(column=0, row=0, sticky='wns') 

        label = tk.Label(self, text=text_in, height=1, width=10)
        label.grid(column=1, row=0, sticky='we') 

        connector_right = BlockElementConnect(self, right_color)
        connector_right.grid(column=2, row=0, sticky='ens') 

        label.bind('<ButtonPress-1>', parent.press)
        label.bind('<ButtonRelease-1>', parent.release)
        
class Block(tk.Frame):
    def __init__(self, canvas, coord, block_data):
        tk.Frame.__init__(self, canvas, bg='white')

        self._load_block_data(block_data)

        self.canvas = canvas
        self.window_tag = self.canvas.create_window(*coord, window=self)
        
    def _load_block_data(self, block_data):
        row_counter = 0
        BlockElement(
            self, 
            block_data.name, 
            BlockElement.Types.Title
        ).grid(column=0, row=row_counter, sticky='nswe')
        row_counter += 1

        for input_name in block_data.inputs:
            BlockElement(
                self, 
                input_name, 
                BlockElement.Types.Input
            ).grid(column=0, row=row_counter, sticky='nswe')
            row_counter += 1
        
        for output_name in block_data.outputs:
            BlockElement(
                self,
                output_name,
                BlockElement.Types.Output
            ).grid(column=0, row=row_counter, sticky='nswe')
            row_counter += 1

    def press(self, event):
        self.offsetX = self.canvas.canvasx(event.x)
        self.offsetY = self.canvas.canvasy(event.y)

    def release(self, event):
        x = self.canvas.canvasx(event.x) - self.offsetX
        y = self.canvas.canvasy(event.y) - self.offsetY
        self.canvas.move(self.window_tag, x, y)

class PipelineEditorFrame(tk.Frame):

    (BLOCK_INIT_X, BLOCK_INIT_Y) = (100,100)

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='yellow')
        self._draw()

    def _draw(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, bg='gray')
        self.canvas.grid(column=0, row=0, sticky='nswe')

    def add_block(self, attribs):
        block = Block(
            self.canvas, 
            (self.BLOCK_INIT_X, self.BLOCK_INIT_Y),
            attribs
        )

class BlockMenuFrame(tk.Frame):

    def __init__(self, parent, block_callback):
        tk.Frame.__init__(self, parent, padx=3, pady=3)
        self.blocks = {}
        self.block_callback = block_callback
        
        self._draw()

    def _draw(self):
        self.grid_columnconfigure(0, weight=0)

        # load config
        self.load_blocks_button = tk.Button(
            self,
            text="Load Block Config",
            command=self._load_block_config
        )
        self.load_blocks_button.grid(row=0, column=0, sticky='we')

        # add block
        self.load_blocks_button = tk.Button(
            self,
            text="Add Block",
            command=self._give_block_to_editor
        )
        self.load_blocks_button.grid(row=1, column=0, sticky='we')

        # lb
        self.blocks_lb = tk.Listbox(self, width=25)
        self.blocks_lb.grid(row=2, column=0, sticky='ns')
        self.grid_rowconfigure(2, weight=1)

    def _give_block_to_editor(self):
        
        cur = self.blocks_lb.get(self.blocks_lb.curselection())

        if cur in self.blocks:
            self.block_callback(self.blocks[cur])

    def _load_block_config(self):
        path = tk.filedialog.askopenfilename()
        new_block_dict = json_loader.load_config(path)
        self.blocks.update(new_block_dict)

        for key in new_block_dict.keys():
            self.blocks_lb.insert(END, key)

        
class BuildAPipeLine:

    def __init__(self, parent):
        parent.title("Build-A-Pipeline")

        # top level
        parent.grid_rowconfigure(0, weight=1)
        parent.minsize(1000, 500)

        # menu
        self.block_menu = BlockMenuFrame(parent, self.add_block)
        self.block_menu.grid(column=0, row=0, sticky="nswe")
        parent.grid_columnconfigure(0, weight=0)

        # seperator
        self.lr_seperator = ttk.Separator(parent, orient="vertical")
        self.lr_seperator.grid(column=1, row=0, rowspan=2, sticky="ns", padx=(2,2))
        parent.grid_columnconfigure(1, weight=0)

        # editor
        self.editor = PipelineEditorFrame(parent)
        self.editor.grid(column=2, row=0, sticky="nswe")
        parent.grid_columnconfigure(2, weight=1)

    def add_block(self, attribs):
        self.editor.add_block(attribs)

        

root = tk.Tk()
my_gui = BuildAPipeLine(root)
root.mainloop()