
import tkinter as tk
import random
import threading
import time
import winsound
from PIL import Image, ImageTk

peli = tk.Tk()
peli.geometry("900x500+800+100")
peli.title("Ernesti ja Kernesti Tomaattisota")

# Pisteet
pisteet = {"ernesti": 0, "kernesti": 0}

# Luodaan Canvas johon elementit lisätään
pelikentta = tk.Canvas(peli, width=900, height=500)
pelikentta.pack()

# Function to resize images
def resize_image(file_path, new_width, new_height):
    img = Image.open(file_path)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# Kuvat (resizing all images)
ernesti_kuva = resize_image("assets/erne.png", 50, 50)
kernesti_kuva = resize_image("assets/kerne.png", 50, 50)
maalitaulu_kuva = resize_image("assets/maalitaulu.png", 100, 100)
tomaatti_kuva = resize_image("assets/tomaatti.png", 20, 20)
osuma_kuva = resize_image("assets/splat.png", 40, 40)

# Hahmojen luonti
ernesti = pelikentta.create_image(800, random.randint(50, 450), anchor=tk.NW, image=ernesti_kuva)
kernesti = pelikentta.create_image(10, random.randint(50, 450), anchor=tk.NW, image=kernesti_kuva)
maalitaulu = pelikentta.create_image(400, 200, anchor=tk.NW, image=maalitaulu_kuva)

# Liikkuvat tomaatit
tomaatti_kernesti = None
tomaatti_ernesti = None

# Heitto- ja osumafunktiot
def heita_tomaatti(heittaja):
    global tomaatti_ernesti
    global tomaatti_kernesti
    if heittaja == "kernesti":
        x, y = pelikentta.coords(kernesti)
        if not tomaatti_kernesti:
            tomaatti_kernesti = pelikentta.create_image(x + 50, y + 25, anchor=tk.NW, image=tomaatti_kuva)
        threading.Thread(target=liikuta_tomaattia, args=(tomaatti_kernesti, 1, heittaja)).start()
    elif heittaja == "ernesti":
        x, y = pelikentta.coords(ernesti)
        if not tomaatti_ernesti:
            tomaatti_ernesti = pelikentta.create_image(x - 30, y + 25, anchor=tk.NW, image=tomaatti_kuva)
        threading.Thread(target=liikuta_tomaattia, args=(tomaatti_ernesti, -1, heittaja)).start()

def liikuta_tomaattia(tomaatti, suunta, heittaja):
    speed = 10
    while True:
        x, y = pelikentta.coords(tomaatti)
        mx, my = pelikentta.coords(maalitaulu)
        
        # Move tomato directly towards the target
        x += speed * suunta
        pelikentta.coords(tomaatti, x, y)
        
        # Check if the tomato reaches the target area
        if (suunta == 1 and x >= 400 - 50) or (suunta == -1 and x <= 400 + 50):
            # Ensure the tomato hits the target
            tarkista_osuma(tomaatti, heittaja)
            break
        
        # Sleep to make the movement visible
        time.sleep(0.05)

def tarkista_osuma(tomaatti, heittaja):
    global tomaatti_kernesti, tomaatti_ernesti
    
    tx, ty = pelikentta.coords(tomaatti)
    mx, my = pelikentta.coords(maalitaulu)
    
    # Increase the size of the target area to ensure a hit
    target_width = 100
    target_height = 100
    
    # Osuma-alue (maalitaulu)
    if mx - target_width // 2 < tx < mx + target_width // 2 and my - target_height // 2 < ty < my + target_height // 2:
        pelikentta.delete(tomaatti)
        pelikentta.create_image(tx, ty, anchor=tk.NW, image=osuma_kuva)
        osuma_aani()
        pisteet[heittaja] += 1
        paivita_taulukko()
    else:
        pelikentta.delete(tomaatti)
    
    # Nollataan tomaatti
    if heittaja == "kernesti":
        tomaatti_kernesti = None
    else:
        tomaatti_ernesti = None

# Ääniefekti
def osuma_aani():
    threading.Thread(target=winsound.Beep, args=(523, 200)).start()

# tulokset
tulostaulu = tk.Label(peli, text=f"Ernesti {pisteet['ernesti']} - {pisteet['kernesti']} Kernesti", font=("Arial", 16))
tulostaulu.pack()

def paivita_taulukko():
    tulostaulu.config(text=f"Ernesti {pisteet['ernesti']} - {pisteet['kernesti']} Kernesti")

# Nollaa pisteet
def nollaa_pisteet():
    pisteet["ernesti"] = 0
    pisteet["kernesti"] = 0
    paivita_taulukko()

# Napit ja toiminnot
ernesti_nappi = tk.Button(peli, text="Ernesti sijainti", command=lambda: pelikentta.coords(ernesti, 800, random.randint(50, 450)))
ernesti_nappi.pack(side=tk.RIGHT)

kernesti_nappi = tk.Button(peli, text="Kernesti sijainti", command=lambda: pelikentta.coords(kernesti, 10, random.randint(50, 450)))
kernesti_nappi.pack(side=tk.LEFT)

ernesti_heita = tk.Button(peli, text="Ernesti heittää", command=lambda: heita_tomaatti("ernesti"))
ernesti_heita.pack(side=tk.RIGHT)

kernesti_heita = tk.Button(peli, text="Kernesti heittää", command=lambda: heita_tomaatti("kernesti"))
kernesti_heita.pack(side=tk.LEFT)

nollaus_nappi = tk.Button(peli, text="Nollaa tulokset", command=nollaa_pisteet)
nollaus_nappi.pack(side=tk.BOTTOM)

# Pääsilmukka
peli.mainloop()
