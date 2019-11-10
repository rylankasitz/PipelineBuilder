import tkinter as tk
import tkinter.filedialog
from tkinter.constants import *

import tkinter.ttk as ttk
import json_loader


class Block(tk.Frame):
    def __init__(self, canvas, coord):
        tk.Frame.__init__(self, canvas, width=50, height=50, bg='red')

        self.canvas = canvas
        self.window_tag = self.canvas.create_window(*coord, window=self)
        
        #self.bind('<B1-Motion>', self.move)    
        self.bind('<ButtonPress-1>', self.press)  
        self.bind('<ButtonRelease-1>', self.release)  
        
        self.bg='green'

    def press(self, event):
        self.offsetX = self.canvas.canvasx(event.x)
        self.offsetY = self.canvas.canvasy(event.y)
    
    #def move(self, event):

        # (x,y) = (self.canvas.canvasx(event.x),self.canvas.canvasy(event.y))
        
        # print("---------------")

        # (cur_x, cur_y) = self.canvas.coords(self.window)
        # print("Cur  pos:  ", cur_x, cur_y)
        # print("Event pos: ", x, y)
    
        # self.canvas.coords(self.window, x, y)

    def release(self, event):
        x = self.canvas.canvasx(event.x) - self.offsetX
        y = self.canvas.canvasy(event.y) - self.offsetY
        self.canvas.move(self.window_tag, x, y)

class PipelineEditorFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='yellow')
        self._draw()

    def _draw(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, bg='gray')
        self.canvas.grid(column=0, row=0, sticky='nswe')
    
        block = Block(self.canvas, (100, 100))

class BlockMenuFrame(tk.Frame):
    _blocks = {}

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self._draw()
        
    def _draw(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # buttons
        self.load_blocks_button = tk.Button(
            self,
            text="Load Blocks File",
            command=self._load_block_config
        )
        self.load_blocks_button.grid(row=0, column=0, sticky='we')

        # lb
        self.blocks_lb = tk.Listbox(self, width=25)
        self.blocks_lb.grid(row=1, column=0, sticky='ns')
        self.grid_rowconfigure(1, weight=1)

    def _load_block_config(self):
        path = tk.filedialog.askopenfilename()

        self.blocks_lb.insert(END, "BLOCK")

class BuildAPipeLine:

    def __init__(self, parent):
        parent.title("Build-A-Pipeline")

        # top level
        parent.grid_rowconfigure(0, weight=1)
        parent.minsize(1000, 500)

        # menu
        block_menu = BlockMenuFrame(parent)
        block_menu.grid(column=0, row=0, sticky="nswe")
        parent.grid_columnconfigure(0, weight=0)

        # seperator
        lr_seperator = ttk.Separator(parent, orient="vertical")
        lr_seperator.grid(column=1, row=0, rowspan=2, sticky="ns", padx=(5,2))
        parent.grid_columnconfigure(1, weight=0)

        # editor
        editor = PipelineEditorFrame(parent)
        editor.grid(column=2, row=0, sticky="nswe")
        parent.grid_columnconfigure(2, weight=1)


        

root = tk.Tk()
my_gui = BuildAPipeLine(root)
root.mainloop()