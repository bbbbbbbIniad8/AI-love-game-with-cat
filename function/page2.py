import tkinter as tk 
from function.GPT import GPT
from function.game_prompt import game_prompt
from function.other import image_paste, alart
import re

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