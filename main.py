import tkinter as tk 
from tkinter import Tk, Spinbox
from tkinter import ttk
import tkinter.filedialog as fd
import random
from PIL import Image, ImageTk

class CustomFrame:
    def __init__(self, master=None):
        self.master = master
        self.baseX = 50
        self.running = False
        self.clicker_proc = None

    def setting(self, master, time):
        self.master = master
        self.frames = []
        self.canvas = []
        self.img = None
        self.time = time
        self.counter = 0

    def main(self):
        frame = {}
        frame[-100] = tk.Tk()
        self.root = frame[-100]
        self.master = self.root

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.title(f"love_game")
    WINDOWX,WINDOWY = 600, 400
    location = {"x":(root.winfo_screenwidth()//2)-(WINDOWX)//2,"y":(root.winfo_screenheight()//2)-(WINDOWY)//2}
    
    root.geometry(f'{WINDOWX}x{WINDOWY}+{location["x"]}+{int(location["y"] * 0.95)}')
    frame = CustomFrame(master=root)
    frame.run()
