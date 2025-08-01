import tkinter as tk 
from tkinter import font as tkfont
from PIL import Image, ImageTk

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label_font = ("Yu Gothic", 30, "bold")
        self.label = tk.Label(self, text="Love Game with Cat", font=label_font)
        self.label.place(x=self.controller.X_size // 2, 
                         y=int(self.controller.Y_size // 2 * 0.6), 
                         anchor="center")

        btn_start = tk.Button(self, text="Start", command=lambda: controller.show_frame("Page2"))
        btn_start.place(x=self.controller.X_size // 2, 
                        y=int(self.controller.Y_size // 2 * 1.4), 
                        anchor="center")

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.canvas = tk.Canvas(self, width=200, height=200)
        self.canvas.place(x=10, y=50)

        image = Image.open("pic/every_cat_0.jpg")
        image = image.resize((200, 200), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
        self.canvas.image = image


class CustomFrame(tk.Frame):
    def __init__(self, X, Y, master=None):
        super().__init__(master) 
        self.X_size = X
        self.Y_size = Y
        

        self.frames = {}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (Page1, Page2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Page1")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.title("love_game")
    
    WINDOWX, WINDOWY = 600, 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    location = {"x": (screen_width // 2) - (WINDOWX // 2), 
                "y": (screen_height // 2) - (WINDOWY // 2)}
    
    root.geometry(f'{WINDOWX}x{WINDOWY}+{location["x"]}+{int(location["y"] * 0.95)}')
    
    frame = CustomFrame(X=WINDOWX, Y=WINDOWY, master=root)
    frame.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()