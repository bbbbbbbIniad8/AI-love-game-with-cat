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
    try:
        self.btn_send["state"] = 'normal'
        self.entry["state"] = 'normal'
    except:
        None

    self.confirm_window.destroy()


def alart(self, msg):
    master = self
    self.confirm_window = tk.Toplevel(master)
    self.confirm_window.grab_set()
    WINDOWX, WINDOWY = 250, 76
    location = {"x": (master.winfo_screenwidth()//2)-(WINDOWX)//2, "y": (master.winfo_screenheight()//2)-(WINDOWY)//2}
    self.confirm_window.geometry(f'{WINDOWX}x{WINDOWY}+{location["x"]}+{location["y"]}')
    self.confirm_window.title("メッセージ")
    label5 = tk.Label(self.confirm_window, text=msg)
    btn4 = tk.Button(self.confirm_window, text="OK", command=lambda: alart_end(self))
    label5.pack()
    btn4.pack()

    self.confirm_window.focus_set()
