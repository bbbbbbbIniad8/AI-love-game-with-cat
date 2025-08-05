import tkinter as tk
from function.other import image_paste

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.canvas_width, self.canvas_height  = 400,606
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.place(x=0, y=0) 
        image_paste(self,"pic/Anchor3.png")
        width_center, height_center = self.controller.X_size // 2, self.controller.Y_size // 2

        ## ラベル
        label_font = ("Yu Gothic", 30, "bold")
        self.label = tk.Label(self, text="AI猫を口説く\nゲーム", font=label_font)
        self.label.place(x=width_center + 120, 
                         y=int(height_center * 0.6), 
                         anchor="center")
        
        ## API入力ラベル
        label_font = ("Yu Gothic", 10, "bold")
        self.APIlabel = tk.Label(self, text="APIキーを入力してください。", font=label_font)
        self.APIlabel.place(x=width_center + 120, 
                         y=int(height_center * 1.0), 
                         anchor="center")
        
        ## API入力ボックス
        self.entry = tk.Entry(self, width=30)
        self.entry.place(x=width_center + 120, 
                         y=int(height_center * 1.1), 
                         anchor="center")
        ## API保存ボタン
        self.btn_save = tk.Button(self, text="save", command=lambda: controller.show_frame("Page2"))
        self.btn_save.place(x=width_center + 235, 
                        y=int(height_center * 1.1), 
                        anchor="center")

        ## 開始ボタン
        btn_start = tk.Button(self, text="Start", command=lambda: controller.show_frame("Page2"), width=10, height=3)
        btn_start.place(x=width_center + 120, 
                        y=int(height_center * 1.4), 
                        anchor="center")