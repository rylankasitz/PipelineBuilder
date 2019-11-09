from tkinter import *
from tkinter.filedialog import askopenfilename

class MyFirstGUI:
    _configs = []
    
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 400

    def __init__(self, master):
        self.master = master
        master.title("Build-A-Pipeline")

        self.greet_button = Button(
            master, text="Load block config", command=self.load_block_config
        )

        self.greet_button.grid(row=0, column=0)

        self.blocks_lb = Listbox(master)
        self.blocks_lb.grid(row=1, column=0)


        self.pipe_line_c = Canvas(
            master, 
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bd=3,
            relief=ridge
        )
        self.pipe_line_c.grid(row=1, column=1)

    def load_block_config(self):
        path = askopenfilename()
        self.blocks_lb.insert(END, "BLOCK"+path.split('/')[-1])



        

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()