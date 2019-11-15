import os
import functools
import enum
import uuid
import copy 
import bezier
import np

import tkinter as tk
import tkinter.ttk as ttk

from tkinter.constants import *
from tkinter import StringVar

import json_loader
import utils
import pipeline_compiler
import configs.program_config as programBlockConfig

from configs.program_config import ProgramBlock
from configs.pipeline_config import Pipeline, Program, Outputs, Constant, Loop

BLOCKS_PATH = os.path.abspath('./programs/blocks.json')

connections = {}

class ConnectionMap():
    def __init__(self, uuid, name):
        self.name = name
        self.uuid = uuid

class BlockElementConnect(tk.Frame):
    def __init__(self, parent, color, type_):
        tk.Frame.__init__(self, parent, bg=color, width=5)
        
        self.canvas = parent.parent.canvas
        self.parent = parent
        self.color = color
        self.type = type_
        self.connects = []
        self.current_line = -1
        self.cors = []

        if self.type == 'output':
            self.bind('<ButtonPress-1>', self.press)
            self.bind('<B1-Motion>', self.move)
            self.bind('<ButtonRelease-1>', self.release)
        
    def parent_press(self):
        self.cors = []
        for line_tag in self.parent.line_tags:
            self.cors.append(self.canvas.coords(line_tag))

    def press(self, event):
        self.parent.parent.parent.connectors.add(self)
        self.parent.parent.parent.parent.bind('<Configure>', lambda event, connectors=self.parent.parent.parent.connectors : self.motion(event, connectors))
        
        self.parent.line_tags.append(self.canvas.create_line(0,0,0,0))
        self.current_line += 1
        
        self.init_x = self.canvas.canvasx(self.parent.parent.winfo_x()) + self.canvas.canvasx(self.winfo_x())
        self.init_y = self.canvas.canvasy(self.parent.parent.winfo_y()) + self.canvas.canvasy(self.parent.winfo_y())
        
    def parent_move(self):
        px = self.canvas.canvasx(self.parent.parent.winfo_x()) + self.canvas.canvasx(self.winfo_x())
        py = self.canvas.canvasy(self.parent.parent.winfo_y()) + self.canvas.canvasy(self.parent.winfo_y())
        self.canvas.coords(self.parent.connector_obj, px, py, px, py)
        for i, cor in enumerate(self.cors):     
            if cor[0] != 0 or cor[1] != 0:
                if len(self.connects) > 0:
                    self.move_line(self.parent.line_tags[i], px, py, cor[2], cor[3])
                else:
                    self.move_line(self.parent.line_tags[i], px, py, px, py)
        
    def move(self, event):
        self.canvas.coords(self.parent.connector_obj, self.init_x, self.init_y, self.init_x, self.init_y)
        self.move_line(self.parent.line_tags[self.current_line], self.init_x, self.init_y, 
                    self.canvas.canvasx(event.x) + self.init_x, 
                    self.canvas.canvasy(event.y) + self.init_y)
            
    def move_line(self, tag, x1, y1, x2, y2):
        nodes1 = np.asfortranarray([
            [0.0, 0.5, 1.0],
            [0.0, 1.0, 0.0],
        ])
        bezier.curve.Curve(nodes1)
        self.canvas.coords(tag, x1, y1, x2, y2)
        
    def motion(self, event, conncs):
        for connector in conncs:
            for i, connect in enumerate(connector.connects):
                pos = connector.canvas.coords(connector.parent.line_tags[i])
                pos_con = connector.canvas.coords(connect)
                connector.canvas.coords(connector.parent.line_tags[i], pos[0], pos[1], pos_con[0], pos_con[1])
        
    def release(self, event):
        if self.type != 'output': return
        
        error = 20
        org_pos = self.canvas.coords(self.parent.line_tags[self.current_line])
        nodes = self.canvas.find_withtag('input')
        
        x = self.canvas.canvasx(event.x) + self.init_x 
        y = self.canvas.canvasy(event.y) + self.init_y

        for node in nodes:
            pos = self.canvas.coords(node)
            if abs(pos[0] - x) < error and abs(pos[1] - y) < error:              
                self.canvas.coords(self.parent.line_tags[self.current_line], org_pos[0], org_pos[1], pos[2], pos[3])
                self.connects.append(node)
                self._add_output(node)
                return
        
        self.parent.line_tags = self.parent.line_tags[::-1]
        self.current_line -= 1
        self.canvas.coords(self.parent.line_tags[self.current_line], org_pos[0], org_pos[1], org_pos[0], org_pos[1])
        
    def _add_output(self, node):
        out = Outputs()
        out.input_uuid = connections[node].uuid
        out.output_name = self.parent.output_name
        out.input_name = connections[node].name
        if isinstance(self.parent.output_name, StringVar):
            out.output_name = self.parent.output_name.get()
        self.parent.parent.block.outputs.append(out)
        

class BlockElement(tk.Frame):
    class Types(enum.Enum):
        Input = 1
        Output = 2
        Title = 3
        AddInput = 4
        InputName = 5
        Loop = 6

    def __init__(self, parent, text_in, element_type):
        tk.Frame.__init__(self, parent, bg='blue')
        
        self.parent = parent             
        self.line_tags = []
        self.output_name = text_in

        self.type = 'none'
        
        self.grid_columnconfigure(1, minsize=100)
        self.label = tk.Label(self, text=text_in, height=1, width=10)
        
        if element_type == BlockElement.Types.Title:
            left_color = 'white'
            right_color = 'white'
        elif element_type == BlockElement.Types.Input:
            left_color = 'green'
            right_color = 'white'
            self.type = 'input'
        elif element_type == BlockElement.Types.Output:
            left_color = 'white'
            right_color = 'red'
            self.type = 'output'
        elif element_type == BlockElement.Types.AddInput:
            left_color = 'white'
            right_color = 'white'
            self.label = tk.Button(self, text=text_in, command=self.parent.add_input)   
        elif element_type == BlockElement.Types.InputName:
            left_color = 'white'
            right_color = 'red'
            self.type = 'output'   
            self.output_name = StringVar()
            self.label = tk.Entry(self, text='Input Name', textvariable=self.output_name, width=15)  
        elif element_type == BlockElement.Types.Loop:
            left_color = 'white'
            right_color = 'white'
            self.label = tk.Button(self, text=text_in, command=self.parent.edit_loop)   
        
        self.connector_obj = self.parent.canvas.create_oval(0,0,0,0)  
        self.parent.canvas.addtag_withtag(self.type, self.connector_obj)
        
        connections[self.connector_obj] = ConnectionMap(self.parent.block.uuid, self.output_name)
        
        self.connector_left = BlockElementConnect(self, left_color, self.type)
        self.connector_left.grid(column=0, row=0, sticky='wns') 

        self.connector_right = BlockElementConnect(self, right_color, self.type)
        self.connector_right.grid(column=2, row=0, sticky='ens') 
        
        self.label.grid(column=1, row=0, sticky='we') 

        self.label.bind('<B1-Motion>', parent.move)
        self.label.bind('<ButtonPress-1>', parent.press)
        
            
class Block(tk.Frame):
    def __init__(self, canvas, coord, block_data, parent, type_='program'):
        tk.Frame.__init__(self, canvas, bg='white')

        self.canvas = canvas
        self.coord = coord
        self.parent = parent
        
        self.connectors = []
        self.row_counter = 0
        self.loop_block = None
        self.loop_root = None
          
        if type_ == 'program':
            self._add_program(block_data)
            self._load_block_data(block_data)
        elif type_ == 'inputs':
            self._add_program(block_data)
            self._create_input_block()
        elif type_ == 'loop':
            self._add_loop(block_data)
            self._create_loop_block()
        elif type_ == 'loop_entry':
            self._add_program(block_data)
            self._create_loop_entry_block()
  
        self.window_tag = self.canvas.create_window(*coord, window=self)                      
        
    def _add_program(self, block_data):
        self.block = Program()
        self.block.uuid = self.id_ = str(uuid.uuid1())
        self.block.name = block_data.name
        self.block.outputs = []
    
    def _add_loop(self, block_data):
        self.block = Loop()
        self.block.uuid = self.id_ = str(uuid.uuid1())
        self.block.mapping = "*.txt"
        self.block.outputs = []
        
    def _create_input_block(self):  
        BlockElement(
            self, 
            'Add Input',
            BlockElement.Types.AddInput
        ).grid(column=0, row=0, sticky='nswe')
        
    def _create_loop_block(self):  
        BlockElement(
            self, 
            'Edit Loop',
            BlockElement.Types.Loop
        ).grid(column=0, row=self.row_counter, sticky='nswe')
        self.row_counter += 1
        block = BlockElement(
            self, 
            '__Entry__',
            BlockElement.Types.Input
        )
        block.grid(column=0, row=self.row_counter, sticky='nswe')
        self.connectors.append(block)
        self.row_counter += 1
        
    def _create_loop_entry_block(self):
        BlockElement(
            self, 
            'Loop Input',
            BlockElement.Types.Title
        ).grid(column=0, row=self.row_counter, sticky='nswe')
        self.row_counter += 1
        block = BlockElement(
            self, 
            '__Entry__',
            BlockElement.Types.Output
        )
        block.grid(column=0, row=self.row_counter, sticky='nswe')
        self.connectors.append(block)
        self.row_counter += 1
        
    def _load_block_data(self, block_data):
        BlockElement(
            self, 
            block_data.name, 
            BlockElement.Types.Title
        ).grid(column=0, row=self.row_counter, sticky='nswe')
        self.row_counter += 1

        for input_name in block_data.inputs:
            block = BlockElement(
                self,
                input_name, 
                BlockElement.Types.Input
            )
            block.grid(column=0, row=self.row_counter, sticky='nswe')
            self.connectors.append(block)
            self.row_counter += 1
        
        for output_name in block_data.outputs:
            block = BlockElement(
                self,
                output_name,
                BlockElement.Types.Output
            )
            block.grid(column=0, row=self.row_counter, sticky='nswe')
            self.connectors.append(block)
            self.row_counter += 1
    
    def add_input(self):
        self.row_counter += 1
        block = BlockElement(
            self,
            'Input Name',
            BlockElement.Types.InputName
        )
        block.grid(column=0, row=self.row_counter, sticky='nswe')
        self.connectors.append(block)

    def edit_loop(self):   
        if self.loop_block == None:
            self.loop_root = tk.Tk()
            self.loop_block = BuildAPipeLine(self.loop_root, "inner_pipeline", "False")
        else :
            self.loop_root.update()
            self.loop_root.deiconify()
            
        def on_closing():
            current_root = self.parent.parent
            
            self.block.body = self.loop_block.config
            
            out = Outputs()
            out.input_uuid = self.loop_block.config.uuid
            out.output_name = "__Entry__"
            out.input_name = "__Entry__"
            
            self.block.outputs.append(out)
            self.loop_root.withdraw()
        
        self.loop_root.protocol("WM_DELETE_WINDOW", on_closing)
        self.loop_root.mainloop()

    def press(self, event):
        self.offsetX = self.canvas.canvasx(event.x)
        self.offsetY = self.canvas.canvasy(event.y)
        
        for connector in self.connectors:
            if connector.type == 'output':
                connector.connector_right.parent_press()
            else:
                connector.connector_left.parent_press()

    def move(self, event):
        x = self.canvas.canvasx(event.x) - self.offsetX
        y = self.canvas.canvasy(event.y) - self.offsetY
        self.canvas.move(self.window_tag, x, y)
        
        for connector in self.connectors:
            if connector.type == 'output':
                connector.connector_right.parent_move()
            else:
                connector.connector_left.parent_move()
        
class PipelineEditorFrame(tk.Frame):

    (BLOCK_INIT_X, BLOCK_INIT_Y) = (100,100)

    def __init__(self, parent , is_root):
        tk.Frame.__init__(self, parent, bg='yellow')
        self.parent = parent
        self.loop_blocks = []
        
        self.connectors = set()
        
        self._add_pipeline()
        self._draw()
        self._add_inputs_block(is_root)

    def _draw(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, bg='gray')
        self.canvas.grid(column=0, row=0, sticky='nswe')

    def add_block(self, attribs):
        block = Block(
            self.canvas, 
            (self.BLOCK_INIT_X, self.BLOCK_INIT_Y),
            attribs,
            self
        )
        
        self.pipeline.blocks[block.id_] = block.block
    
    def add_loop(self):
        block = Block(
            self.canvas, 
            (self.BLOCK_INIT_X, self.BLOCK_INIT_Y),
            ProgramBlock(),
            self,
            type_="loop"
        )
        
        self.pipeline.blocks[block.id_] = block.block
        self.loop_blocks.append(block)
    
    def _add_inputs_block(self, is_root):
        if is_root == "True":
            type_ = "inputs"
        else:
            type_ = "loop_entry"
            
        block = Block(
            self.canvas, 
            (self.BLOCK_INIT_X, self.BLOCK_INIT_Y),
            ProgramBlock(),
            self,
            type_=type_
        )
        
        self.pipeline.outputs = block.block.outputs     
    
    def _add_pipeline(self):
        self.pipeline = Pipeline()
        self.pipeline.uuid = self.id_ = str(uuid.uuid1())
        self.pipeline.outputs = []
        self.pipeline.blocks = {}

class BlockMenuFrame(tk.Frame):

    def __init__(self, parent, block_callback, loop_callback):
        tk.Frame.__init__(self, parent, padx=3, pady=3)
        self.blocks = {}
        self.block_callback = block_callback
        self.loop_callback = loop_callback
        
        self._draw()
        self._load_block_config()

    def _draw(self):
        self.grid_columnconfigure(0, weight=0)

        # load config
        self.load_blocks_button = tk.Button(
            self,
            text="Create New Block",
            command=self._open_block_gui
        )
        self.load_blocks_button.grid(row=0, column=0, sticky='we')

        # add block
        self.load_blocks_button = tk.Button(
            self,
            text="Create Loop",
            command=self._add_loop_block
        )
        self.load_blocks_button.grid(row=1, column=0, sticky='we')
        
        # add block
        self.load_blocks_button = tk.Button(
            self,
            text="Add Block",
            command=self._give_block_to_editor
        )
        self.load_blocks_button.grid(row=2, column=0, sticky='we')
        
        # lb
        self.blocks_lb = tk.Listbox(self, width=25)
        self.blocks_lb.grid(row=3, column=0, sticky='ns')
        self.grid_rowconfigure(3, weight=1)

    def _give_block_to_editor(self):     
        cur = self.blocks_lb.get(self.blocks_lb.curselection())

        if cur in self.blocks:
            self.block_callback(self.blocks[cur])

    def _load_block_config(self):
        new_block_dict = json_loader.load_config(BLOCKS_PATH)
        self.blocks.update(new_block_dict)

        for key in new_block_dict.keys():
            self.blocks_lb.insert(END, key)
    
    def _add_loop_block(self):
        self.loop_callback()
        
    def _open_block_gui(self):
        import block_creator_gui

        
class BuildAPipeLine:

    def __init__(self, parent, name, is_root):
        self.parent = parent
        
        parent.title("Build-A-Pipeline")

        # top level
        parent.grid_rowconfigure(0, weight=1)
        parent.minsize(1000, 500)

        # menu
        self.block_menu = BlockMenuFrame(parent, self.add_block, self.add_loop)
        self.block_menu.grid(column=0, row=0, sticky="nswe")
        parent.grid_columnconfigure(0, weight=0)

        # seperator
        self.lr_seperator = ttk.Separator(parent, orient="vertical")
        self.lr_seperator.grid(column=1, row=0, rowspan=2, sticky="ns", padx=(2,2))
        parent.grid_columnconfigure(1, weight=0)

        # editor
        self.editor = PipelineEditorFrame(parent, is_root)
        self.editor.grid(column=2, row=0, sticky="nswe")
        parent.grid_columnconfigure(2, weight=1)
        
        # config
        self.editor.pipeline.name = name
        self.editor.pipeline.root = is_root
        self.config = self.editor.pipeline

    def add_block(self, attribs):
        self.editor.add_block(attribs)
    
    def add_loop(self):
        self.editor.add_loop()
 

pipeline_name = 'test'

root = tk.Tk()
my_gui = BuildAPipeLine(root, pipeline_name, "True")

def on_closing():
    json_loader.write_config('./pipelines/' + pipeline_name + '/config.json', my_gui.config)
    pipeline_compiler.run(pipeline_name)
    for r in my_gui.editor.loop_blocks:
        r.loop_root.destroy()
    root.destroy()
        
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()