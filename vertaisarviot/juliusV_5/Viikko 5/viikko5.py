import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import winsound
import random

root = tk.Tk()
root.title("Apinasaarelta pekeneminen")
root.geometry("700x600")

canvas = tk.Canvas(root, width=700, height=500)
canvas.pack()

canvas.create_line(100, 0, 100, 500, fill="black", width=2)
canvas.create_line(600, 0, 600, 500, fill="black", width=2)
canvas.create_line(600, 250, 700, 250, fill="black", width=2)
canvas.create_line(0, 250, 100, 250, fill="black", width=2)
canvas.create_text(50, 125, text="Ernesti", font=("Arial", 16), fill="black")
canvas.create_text(50, 375, text="Kernesti", font=("Arial", 16), fill="black")
canvas.create_text(650, 125, text="Pohteri", font=("Arial", 16), fill="black")
canvas.create_text(650, 375, text="Eteteri", font=("Arial", 16), fill="black")

monkeyimage= Image.open("apina.png")
monkeyimage = monkeyimage.resize((25, 25))
monkeyimage_tk = ImageTk.PhotoImage(monkeyimage)

shipimage= Image.open("ship.png")
shipimage = shipimage.resize((40, 40))
shipimage_tk = ImageTk.PhotoImage(shipimage)

jeeimage= Image.open("jee.png")
jeeimage = jeeimage.resize((60, 60))
jeeimage_tk = ImageTk.PhotoImage(jeeimage)

stop_threads = False
ship_sent = False
threads = []
message_words = {
    "Ernesti",
    "ja",
    "Kernesti",
    "tässä",
    "terve!",
    "Olemme",
    "autiolla",
    "saarella",
    "voisiko",
    "joku",
    "tulla",
    "sieltä",
    "sivistyneestä",
    "maailmasta",
    "hakemaan",
    "meidät",
    "pois!",
    "Kiitos!"
}

pohteri_words = []
eteteri_words = []

lock = threading.Lock()

def pohteri(word):
    global ship_sent
    with lock:
        if word not in pohteri_words:
            pohteri_words.append(word)
            if len(pohteri_words) > 10 and not ship_sent:
                send_ship("pohteri")
                print(pohteri_words)
                ship_sent = True

def eteteri(word):
    global ship_sent
    with lock:
        if word not in eteteri_words:
            eteteri_words.append(word)
            if len(eteteri_words) > 10 and not ship_sent:
                send_ship("eteteri")
                print(eteteri_words)
                ship_sent = True

def send_ship(name):
    if name == "pohteri":
        y_pos = 125
    elif name == "eteteri":
        y_pos = 375
    shipimage = canvas.create_image(600, y_pos, image=shipimage_tk, anchor=tk.CENTER)
    for step in range(100):
        x_pos = 600 - (5 + step *5)
        canvas.coords(shipimage, x_pos, y_pos)
        if x_pos==100:
            winsound.PlaySound("jee.wav",winsound.SND_ASYNC)
            canvas.create_image(50, y_pos, image=jeeimage_tk, anchor=tk.CENTER)
        time.sleep(0.05)

def move_monkey(monkeyimage, y_pos, word):
    global stop_threads                   
    if not stop_threads:
        for step in range(100):
            if random.random() < 0.0069:   #99.31% ^100 = ~50% mahdollisuus selvitä 100 askelta
                winsound.PlaySound("death.wav", winsound.SND_ASYNC)
                break
            winsound.Beep(1000, 3)
            x_pos = 100 + (5+step *5)
            if x_pos == 600:
                winsound.PlaySound("success.wav",winsound.SND_ASYNC)
                if y_pos < 250:
                    pohteri(word)
                elif y_pos > 250:
                    eteteri(word)
            canvas.coords(monkeyimage, x_pos, y_pos)
            time.sleep(0.1)

def start_swimming():
    start_swimming_ernesti()
    start_swimming_kernesti()

def start_swimming_ernesti():
    global threads
    def send_monkey(i):
        y_pos = 25 + (i * 20)
        monkeyimage = canvas.create_image(100,y_pos, image=monkeyimage_tk, anchor=tk.CENTER)
        word = random.choice(list(message_words))
        t = threading.Thread(target=move_monkey,args=(monkeyimage, y_pos, word))
        threads.append(t)
        t.start()
    for i in range(10):
        root.after(i*1000, send_monkey, i)


def start_swimming_kernesti():
    global threads
    def send_monkey(i):
        y_pos = 275 + (i * 20)
        monkeyimage = canvas.create_image(100,y_pos, image=monkeyimage_tk, anchor=tk.CENTER)
        word = random.choice(list(message_words))
        t = threading.Thread(target=move_monkey,args=(monkeyimage, y_pos, word))
        threads.append(t)
        t.start()
    for i in range(10):
        root.after(i*1000, send_monkey, i)

start_button = tk.Button(root, text="Send Monkeys", command=start_swimming)
start_button.pack(pady=20)

def on_closing():                       #pysäyttää threadit kun sulkee ikkunan nii ei tule erroreita. chatgpt:ltä
    global stop_threads
    stop_threads = True

    for t in threads:
        t.join(timeout=0.1)

    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()