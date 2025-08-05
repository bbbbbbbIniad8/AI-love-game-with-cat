import tkinter as tk 
from funciton.GPT import GPT
from funciton.game_prompt import game_prompt
from funciton.other import image_paste, alart
import re


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.canvas_width, self.canvas_height  = 400,606
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.place(x=0, y=0) 
        image_paste(self,"pic/Anchor3.png")
        width_center, height_center = self.controller.X_size // 2, self.controller.Y_size // 2

        label_font = ("Yu Gothic", 30, "bold")
        self.label = tk.Label(self, text="Love\nGame\nwith\nCat", font=label_font)
        self.label.place(x=width_center + 120, 
                         y=int(height_center * 0.6), 
                         anchor="center")

        btn_start = tk.Button(self, text="Start", command=lambda: controller.show_frame("Page2"))
        btn_start.place(x=width_center + 160, 
                        y=int(height_center * 1.4), 
                        anchor="center")

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.canvas_width, self.canvas_height  = 250, 250
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.place(x=10, y=10)
        image_paste(self,"pic/every_cat_0.jpg")
        
        text_area_x, text_area_y = 270, 10
        text_area_width = 330
        text_area_height = 240
        scrollbar_width = 20

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
        self.text_box.insert(tk.END, "every_catが表れた。")
        self.text_box.config(state=tk.DISABLED)

        self.entry = tk.Text(self, width=40,height=3, font = ("",15),)
        self.entry.place(x=self.controller.X_size//2, 
                     y=300, anchor="center")
        
        self.btn_send = tk.Button(self, text="send",command=self.get_entry)
        self.btn_send.place(x=self.controller.X_size//2, 
                        y=int(self.controller.Y_size*0.88), 
                        anchor="center")
        self.log = ""
        self.love = 0
        with open("prompt.txt", mode = "r",encoding="utf-8") as f:
           self.game_prompt = f.read()
        self.every_cat = GPT(1.0, self.game_prompt)
        self.AIname = "アリフレ・タネコ"
        
    def get_entry(self):
        self.entry.config(state=tk.DISABLED) 
        endnum, content = self.get_content(self.entry.get("1.0", tk.END))
        if endnum == 0:
            self.entry.config(state=tk.NORMAL)
            return 0
        self.log += f"ユーザー:{content}\n\n"
        answer = self.every_cat.Res(game_prompt(self.AIname, self.love, self.log))
        print(answer)
        try:
            answer, face_num, love_num =  self.answer_processing(answer)
            if int(love_num) >= 100:
                alart(self, "ゲームクリア")
        except IndexError:
            alart(self, "エラーが発生しました。\nもう一度やり直してください")
            return 0

        print(love_num)
        self.log += f"self.AIname :{answer}\n感情番号{face_num}\n\n"
        self.update_text_box(answer, face_num)
        self.entry.delete("1.0", tk.END)
        self.entry.config(state=tk.NORMAL)
        return 1

    def update_text_box(self, message, number):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete("1.0", tk.END)
        image_paste(self,f"pic/every_cat_{number}.jpg")
        self.text_box.insert(tk.END, message)
        self.text_box.config(state=tk.DISABLED)
        self.text_box.see(tk.END)

    def answer_processing(self, answer):
        deta = re.findall(r"(\n|^)\d:(.*?);",answer)
        answer = f"every_cat:{deta[0][1]}"
        num = int(deta[1][1])
        self.love += int(deta[2][1])
        return answer, num, self.love

    def get_content(self,target):
        content = target.strip()
        return (1 if content != "" else 0), content


class CustomFrame(tk.Frame):
    def __init__(self, X, Y, master=None):
        super().__init__(master) 
        self.X_size, self.Y_size = X, Y
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
    root.title("love_game")
    
    WINDOWX, WINDOWY = 600, 400
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    location = {"x": (screen_width // 2) - (WINDOWX // 2), 
                "y": (screen_height // 2) - (WINDOWY // 2)}
    
    root.geometry(f'{WINDOWX}x{WINDOWY}+{location["x"]}+{int(location["y"] * 0.95)}')
    
    frame = CustomFrame(X=WINDOWX, Y=WINDOWY, master=root)
    frame.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()