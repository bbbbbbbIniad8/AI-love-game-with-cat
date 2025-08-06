import tkinter as tk
from function.page1 import Page1
from function.page2 import Page2


class CustomFrame(tk.Frame):
    def __init__(self, X, Y, master=None):
        super().__init__(master)
        self.X_size, self.Y_size = X, Y
        self.frames = {}
        self.master = master

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
    root.title("TALK_game")

    WINDOWX, WINDOWY = 600, 400
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    location = {"x": (screen_width // 2) - (WINDOWX // 2),
                "y": (screen_height // 2) - (WINDOWY // 2)}

    root.geometry(f'{WINDOWX}x{WINDOWY}+{location["x"]}+{int(location["y"] * 0.95)}')
    frame = CustomFrame(X=WINDOWX, Y=WINDOWY, master=root)
    frame.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
