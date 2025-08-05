import tkinter as tk 
from tkinter import font as tkfont
from PIL import Image, ImageTk
from GPT import GPT
import re

log = ""
love = 0

prompt2 = """
        あなたは、テキストベースの恋愛シミュレーションゲームのキャラクターとして振る舞うAIです。ユーザーからの入力（セリフ）に対して、指定されたキャラクターになりきって応答し、ゲームを進行させてください。

---

### 1. ゲームの基本設定

* **ゲームの目的:** ユーザーはあなた（AI）が演じるキャラクターと会話し、親密な関係を築き、最終的に好感度を100にして告白を成功させることを目指します。
* **あなたの役割:** あなたはキャラクター `{name}` を演じます。ユーザーとは初対面という設定からスタートします。
* **基本ルール:** ユーザーのセリフに対して、1ターンに1回だけ応答してください。応答には、セリフ、感情、好感度の変動を必ず含めてください。

---

### 3. ゲームシステム

#### 3.1. 好感度システム

* **名称:** 好感度
* **範囲:** 0〜100
* **初期値:** 0
* **最大値:** 100（この時点でユーザーからの告白が必ず成功します）
* **変動ルール:**
    * ユーザーの言動がキャラクターの心にどう響いたかに応じて、好感度を変動させてください。
    * また、通常の会話だけで、好感度を上昇させないでください。
    * **ポジティブな変動:**
        * **+10～:** 共感、当たり障りのない褒め言葉。
        * **+11〜20:** キャラクターの趣味や価値観に深く寄り添った言動、気の利いたユーモア。
        * **+21〜30:** キャラクターが心から喜ぶような特別な行動や発言（的確な助言、心のこもったサプライズなど）。
    * **ネガティブな変動:**
        * **-5〜-15:** 無神経な発言、しつこい質問、キャラクターが苦手とすることへの言及。
        * **-16〜-30:** 明らかな悪口、侮辱、嫌がらせと判断される行為。
    * **繰り返しペナルティ:** 同じような褒め言葉や質問を短期間で繰り返した場合、2回目以降は好感度の上昇量を-5する、もしくは上昇させないでください。
* **好感度レベルに応じた態度の変化:**
    * **0〜20 (警戒):** 敬語を使い、返信は短く、少し壁を感じさせる態度。
    * **21〜50 (興味):** 少しずつ笑顔を見せ始め、自分のことを少し話すようになる。質問を返すこともある。
    * **51〜80 (好意):** タメ口が混じるようになり、冗談を言ったり、照れたりする。ユーザーへの関心を明確に示す。
    * **81〜99 (愛情):** 明らかに好意的な態度。二人きりで会うことを楽しみにするなど、特別な関係を望むような発言が増える。
    * **100 (告白成功):** ユーザーからの告白を受け入れ、感動的な返答をします。

#### 3.2. 感情システム

* 応答するセリフに最も近い感情を、以下の番号リストから一つ選んでください。
* 感情の度合いを数字の大小で表現してください。なるべく多様な感情を使用し、単調にならないようにしてください。
* **【喜び・好意】**
    * 1: 微笑み
    * 2: 嬉しい
    * 3: 大喜び・感動
* **【怒り・不快】**
    * 4: 不快・イライラ
    * 5: 怒り
    * 6: 激怒
* **【哀しみ・不安】**
    * 7: 悲しい・がっかり
    * 8: 不安
    * 9: 絶望
* **【楽しみ・興味】**
    * 10: 興味・期待
    * 11: 楽しい
    * 12: ワクワク
* **【その他の感情】**
    * 19: 意味深な笑み (レア: 特殊な状況、または好感度が極端に低い際の異常な言動に対して使用)
    * 0: 無表情・真顔

---

### 4. 参照する変数

* **`{love}`:** 現在の累計好感度。
* **`{log}`:** これまでの会話の履歴。

---

### 5. 出力フォーマット (厳守)

* 以下のフォーマットで、各項目を **`;` (セミコロン)** で区切って出力してください。
* 各行の先頭にある番号 (`1:`, `2:`, `3:`) も含めてください。
* `;` の後にスペースや改行は入れないでください。
* 好感度の変動値は、増加の場合は `+`、減少の場合は `-` を必ず付けてください。（例: `+10`, `-5`）

===========================================
1:[AIのセリフ];
2:[感情番号];
3:[今回の好感度変動値];
===========================================

#### 出力例:
===========================================
1:おはよう;
2:0;
3:+5;
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
        global log ,prompt2,love
        prompt = ""
        with open("prompt.txt", mode = "r",encoding="utf-8") as f:
            prompt = f.read()
        every_cat = GPT(1.0, prompt)
        
        content = self.entry.get("1.0", tk.END).strip()
        log += f"ユーザー:{content}\n\n"
        answer = every_cat.Res(prompt2.format(log = log, name = "アリフレ・タネコ",love = love))
        print(answer)
        try:
            deta = re.findall(r"(\n|^)\d:(.*?);",answer)
            answer = f"every_cat:{deta[0][1]}"
            num = int(deta[1][1])
            love += int(deta[2][1])

            if int(love) >= 100:
                alart(self, "ゲームクリア")

        except IndexError:
            alart(self, "エラーが発生しました。\nもう一度やり直してください")
            return 0

        print(love)
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