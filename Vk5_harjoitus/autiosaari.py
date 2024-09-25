
import tkinter as tk
import random
import threading
import time
import winsound
from PIL import Image, ImageTk

# Luodaan window
ikkuna = tk.Tk()
ikkuna.geometry("900x500")
ikkuna.title("Ernesti ja Kernesti autiosaarella")

# Tehdään canvas elementtäjä varten 
ikkuna_canvas = tk.Canvas(ikkuna, width=900, height=500)
ikkuna_canvas.pack()

# Saarien luonti
autiosaari = ikkuna_canvas.create_rectangle(50, 50, 200, 400, fill="#dcca73")
asuttusaari = ikkuna_canvas.create_rectangle(400, 50, 550, 400, fill="#15d712")

# Työkalu kuvien koon muokkaukseen
def resize_image(file_path, new_width, new_height):
    img = Image.open(file_path)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

ernesti_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/erne.png", 50, 50)
kernesti_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/kerne.png", 50, 50)
apina_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/apina.png", 40, 40)
eteteri_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/eteteri.png", 20, 20)
pohteri_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/pohteri.png", 40, 40)

ernesti = ikkuna_canvas.create_image(150, 100, image=ernesti_kuva)
kernesti = ikkuna_canvas.create_image(150, 350, image=kernesti_kuva)

apina_e = ikkuna_canvas.create_image(150, 100, image=apina_kuva)
apina_k = ikkuna_canvas.create_image(150, 350, image=apina_kuva)
    

def laheta_apina(apina_valinta):
    matka=300
    askel=5
    delay=15
    for step in range(0, matka, askel):
        ikkuna_canvas.after(step * delay, lambda: ikkuna_canvas.move(apina_valinta, askel, 0))


ernesti_laheta = tk.Button(ikkuna, text="Kernesti lähettää apinan", command=lambda: laheta_apina(apina_e))
ernesti_laheta.place(x=50, y=10)    

kernesti_laheta = tk.Button(ikkuna, text="Kernesti lähettää apinan", command=lambda: laheta_apina(apina_k))
kernesti_laheta.place(x=50, y=430)



ikkuna.mainloop()