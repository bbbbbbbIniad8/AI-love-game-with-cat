import tkinter as tk 
from tkinter import font as tkfont
from PIL import Image, ImageTk
from GPT import GPT

log = ""

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
        global log
        super().__init__(parent)
        self.controller = controller

        # --- 画像(Canvas)の配置 ---
        canvas_width = 200
        canvas_height = 200
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.place(x=10, y=10) # 左上の(10, 10)座標に配置

        try:
            image = Image.open("pic/every_cat_0.jpg")
            image = image.resize((canvas_width, canvas_height), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
        except FileNotFoundError:
            self.canvas.create_text(canvas_width/2, canvas_height/2, text="画像なし", anchor=tk.CENTER)
        
        text_area_x = 220  # テキストエリアの開始X座標
        text_area_y = 10   # テキストエリアの開始Y座標
        text_area_width = 360 # テキストエリアの幅（ピクセル）
        text_area_height = 240 # テキストエリアの高さ（ピクセル）
        scrollbar_width = 20 # スクロールバーの幅（ピクセル）

        self.text_box = tk.Text(self, wrap=tk.CHAR, font = ("",15)) 
        self.text_box.place(x=text_area_x, 
                       y=text_area_y, 
                       width=text_area_width - scrollbar_width,
                       height=text_area_height)

        
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text_box.yview)
        scrollbar.place(x=text_area_x + text_area_width - scrollbar_width, 
                        y=text_area_y, 
                        height=text_area_height)
        
        self.text_box.config(yscrollcommand=scrollbar.set)
        long_text = log
        self.text_box.insert(tk.END, long_text)
        self.text_box.config(state=tk.DISABLED)

        self.entry = tk.Text(self, width= 40,height = 3, font = ("",15),)
        self.entry.place(x=self.controller.X_size // 2, 
                     y=300,anchor="center")
        
        btn_send = tk.Button(self, text="send",command=self.get_entry)
        btn_send.place(x=self.controller.X_size // 2, 
                        y=int(self.controller.Y_size * 0.88), 
                        anchor="center")
        
    def get_entry(self):
        global log
        content = self.entry.get("1.0", tk.END).strip()
        answer = GPT.ResSimple(content)
        self.update_text_box(answer)
        self.entry.delete("1.0", tk.END)


    def update_text_box(self, message):
        # 一時的に編集可能にする
        self.text_box.config(state=tk.NORMAL)
        # メッセージを挿入
        self.text_box.insert(tk.END, message)
        # 再び編集不可に戻す
        self.text_box.config(state=tk.DISABLED)
        # 自動で一番下までスクロールする
        self.text_box.see(tk.END)



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