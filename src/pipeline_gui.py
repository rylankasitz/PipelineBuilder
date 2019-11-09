import os
import tkinter as tk
from tkinter import *
import pygubu

UI_FILE = "main.ui"

class Application(pygubu.TkApplication):
    
    def _create_ui(self):

        self.builder = builder = pygubu.Builder()
        
        builder.add_from_file(UI_FILE)
        
        self.mainwindow = builder.get_object('mainwindow', self.master)
        
        self.mainmenu = menu = builder.get_object('menu', self.master)
        self.set_menu(menu)
        
        self.canvas = builder.get_object('canvas')
        
        self.node = Node(builder, self.canvas)
        self.node = Node(builder, self.canvas, x=200, y=200)
        
        builder.connect_callbacks(self)
            
    def run(self):
        self.mainwindow.mainloop()

class Node():
    
    def __init__(self, builder, canvas, x=100, y=100):   
        
        self.canvas = canvas
        self.offsetX = 0
        self.offsetY = 0
        
        frame = Frame(canvas, width=200, height=200, background="red")
        frame.bind('<B1-Motion>', self.move)
        frame.bind('<Button-1>', self.press)

        self.node = self.canvas.create_window(x, y, window=frame)      

    def press(self, event):
        self.offsetX = self.canvas.canvasx(event.x)
        self.offsetY = self.canvas.canvasy(event.y)
    
    def move(self, event): 
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.move(self.node, x - self.offsetX, y - self.offsetY)


root = tk.Tk()
app = Application(root)
app.run()