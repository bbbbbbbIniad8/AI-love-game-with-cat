import tkinter as tk 
from tkinter import font as tkfont
from PIL import Image, ImageTk
from GPT import GPT
import re

log = ""

prompt2 = """
        これはテキストベースの恋愛シュミレーションゲームです。
        あなたはユーザーからのセリフに対して一つずつ返信し、好感度を更新してください。
        好感度の最大値は100です。
        {log}
        ===========================================
        発言内容ともに、感情番号の出力も行え。番号のルールは以下に従う。
        また、同じ種類の感情でも数字が大きくなると感情の度合いも大きくなる。
        好感度は、ユーザーへの好感度が向上するたびに上昇(一度に10~30上昇)
        変動率は平均値が10です。every_catがユーザーに対して行動や言葉に対して感じる愛情の度合いに応じて、スコアを徐々に増加させてください。
        (いやがらせ等を行えば好感度の値は減少する。(一度に10~　現象))。100になると必ず告白が成功する。
        初期好感度は0です。

        なるべく、いろんな番号を使え。
        0:真顔
        1~3:喜び
        4~6:怒り
        7~9:哀しみ
        10~12:楽しみ
        19:不気味な笑い(レア)
        ===========================================
        出力フォーマット(必ず;をつけろ。)
        ===========================================
        1:AIの発言内容;
        2:感情番号;
        3:AIへの好感度;
        ===========================================
        出力例:
        ===========================================
        1:おはよう;
        2:1;
        3:10;
        ===========================================
        """

def image_paste(self,path):
    try:
        self.image = Image.open(path)
        self.image = self.image.resize((self.canvas_width, self.canvas_height), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
    except FileNotFoundError:
        self.canvas.create_text(self.canvas_width/2, self.canvas_height/2, text="画像なし", anchor=tk.CENTER)

def alart(self, msg):         
        master = self
        self.confirm_window = tk.Toplevel(master) 
        
        WINDOWX,WINDOWY = 250,76
        location = {"x":(master.winfo_screenwidth()//2)-(WINDOWX)//2,"y":(master.winfo_screenheight()//2)-(WINDOWY)//2}
        self.confirm_window.geometry(f'{WINDOWX}x{WINDOWY}+{location["x"]}+{location["y"]}')
        self.confirm_window.title(f"メッセージ")
        label5 =  tk.Label(self.confirm_window, text=f"{msg}")
        btn4 = tk.Button(self.confirm_window, text="OK", command= lambda:self.confirm_window.destroy())
        label5.pack()
        btn4.pack()
        

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
        
        btn_send = tk.Button(self, text="send",command=self.get_entry)
        btn_send.place(x=self.controller.X_size//2, 
                        y=int(self.controller.Y_size*0.88), 
                        anchor="center")
        
    def get_entry(self):
        global log ,prompt2
        prompt = ""
        with open("prompt.txt", mode = "r",encoding="utf-8") as f:
            prompt = f.read()
        every_cat = GPT(1.0, prompt)
        
        content = self.entry.get("1.0", tk.END).strip()
        log += f"ユーザー:{content}\n\n"
        answer = every_cat.Res(prompt2.format(log = log))
        print(answer)
        try:
            deta = re.findall(r"(\n|^)\d:(.*?);",answer)
            answer = f"every_cat:{deta[0][1]}"
            num = int(deta[1][1])

            if int(deta[2][1]) >= 100:
                alart(self, "ゲームクリア")

        except IndexError:
            alart(self, "エラーが発生しました。\nもう一度やり直してください")
            return 0

        log += answer + f"\n感情番号{num}\n\n"
        self.update_text_box(answer, num)
        self.entry.delete("1.0", tk.END)
        return 1

    def update_text_box(self, message, number):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete("1.0", tk.END)
        image_paste(self,f"pic/every_cat_{number}.jpg")
        self.text_box.insert(tk.END, message)
        self.text_box.config(state=tk.DISABLED)
        self.text_box.see(tk.END)


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