from PIL import Image, ImageTk
import tkinter as tk


def image_paste(self, path):
    try:
        self.image = Image.open(path)
        self.image = self.image.resize((self.canvas_width, self.canvas_height), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
    except FileNotFoundError:
        self.canvas.create_text(self.canvas_width/2, self.canvas_height/2, text="画像なし", anchor=tk.CENTER)


def alart_end(self):
    self.confirm_window.destroy()


def alart(self, msg):
    master = self
    self.confirm_window = tk.Toplevel(master)
    self.confirm_window.grab_set()
    window_X, window_Y = 250, 76
    location = {"x": (master.winfo_screenwidth()//2)-(window_X)//2, "y": (master.winfo_screenheight()//2)-(window_Y)//2}
    self.confirm_window.geometry(f'{window_X}x{window_Y}+{location["x"]}+{location["y"]}')
    self.confirm_window.title("メッセージ")
    label = tk.Label(self.confirm_window, text=msg)
    btn = tk.Button(self.confirm_window, text="OK", command=lambda: alart_end(self))
    label.pack()
    btn.pack()
    self.confirm_window.focus_set()


def ending(self, end_code):
    master = self
    self.confirm_window = tk.Toplevel(master)
    self.confirm_window.grab_set()
    window_X, window_Y = 400, 300
    location = {"x": (master.winfo_screenwidth()//2)-(window_X)//2, "y": (master.winfo_screenheight()//2)-(window_Y)//2}
    self.confirm_window.geometry(f'{window_X}x{window_Y}+{location["x"]}+{location["y"]}')
    self.confirm_window.title("ending")

    window_X, window_Y = 400, 300
    canvas_X, canvas_Y = 300, 150
    canvas = tk.Canvas(self.confirm_window, width=canvas_X, height=canvas_Y)
    canvas.place(x=window_X // 2, y=window_Y // 3 + 10, anchor="center")

    if end_code == 1:
        endmsg1 = "GAMEOVER"
        endmsg2 = "あなたの臓器は奴の'コレクション'に加えられた"
        back_color = "black"
        canvasmsg_color = "red"
        canvasmsg = "You died"
    else:
        endmsg1 = "GAMECLEAR"
        endmsg2 = "あなたは生き延びた?"
        canvasmsg_color = "blue"
        r, g, b = 255, 255, 220
        back_color = f'#{r:02x}{g:02x}{b:02x}'
        canvasmsg = "You survived"

    canvas.create_rectangle(0, 0, canvas_X, canvas_Y, fill=back_color)
    canvas.create_text(canvas_X // 2, canvas_Y // 2, text=canvasmsg, fill=canvasmsg_color, font=("", 32))

    label = tk.Label(self.confirm_window, text=endmsg1, font=("", 20))
    label.place(x=window_X // 2,
                y=window_Y // 4 * 3 - 15, anchor="center")

    label2 = tk.Label(self.confirm_window, text=endmsg2, font=("", 12))
    label2.place(x=window_X // 2,
                y=window_Y // 4 * 3 + 15, anchor="center")

    btn = tk.Button(self.confirm_window, text="OK", command=lambda: alart_end(self))
    btn.place(x=window_X // 2,
              y=window_Y // 10 * 9, anchor="center")

    self.confirm_window.focus_set()
