
import tkinter as tk
import random
import threading
import time
from PIL import Image, ImageTk
from äänet import Torvi
import winsound

torvi = Torvi()

# Luodaan window
ikkuna = tk.Tk()
ikkuna.geometry("900x500")
ikkuna.title("Ernesti ja Kernesti autiosaarella")

# Tehdään canvas elementtejä varten 
ikkuna_canvas = tk.Canvas(ikkuna, width=900, height=500)
ikkuna_canvas.pack()

# Saarien luonti
autiosaari = ikkuna_canvas.create_rectangle(50, 50, 200, 400, fill="#dcca73")
asuttusaari = ikkuna_canvas.create_rectangle(400, 50, 850, 400, fill="#15d712")

# Työkalu kuvien koon muokkaukseen (kysytty ChatGPT)
def resize_image(file_path, new_width, new_height):
    img = Image.open(file_path)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

ernesti_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/erne.png", 50, 50)
kernesti_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/kerne.png", 50, 50)
apina_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/apina.png", 30, 30)
eteteri_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/eteteri.png", 50, 100)
pohteri_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/pohteri.png", 50, 100)
laiva_kuva = resize_image("Vk5_harjoitus/autiosaari_assets/laiva.png", 70, 70)

ernesti = ikkuna_canvas.create_image(150, 100, image=ernesti_kuva)
kernesti = ikkuna_canvas.create_image(150, 350, image=kernesti_kuva)
pohteri = ikkuna_canvas.create_image(450, 100, image=pohteri_kuva)
eteteri = ikkuna_canvas.create_image(450, 350, image=eteteri_kuva)

sanat = ["sos", "ernesti", "ja", "kernesti", "haaksirikkoutuivat", "autiosaarelle", "he", "tarvitsevat",
        "pikaisesti", "apua", "lähettäkää", "laiva", "pelastamaan", "heidät", "muuten", "he", "kuolevat",
        "luvassa", "suuret", "juhlat", "heidän", "pelastajille"]
ernestin_sanat = set()
kernestin_sanat = set()
ernestin_apinat = 0
kernestin_apinat = 0

laiva_lahetetty = False

# Määritetään apina jommallekummalle ja valitaan sana
def maarita_sana_apina(apina_valinta):
    henkilo = apina_valinta
    if apina_valinta == "ernesti":
        sana = random.choice(sanat)
        sana_apina = ikkuna_canvas.create_image(180, 110, image=apina_kuva)
        valittu_sana = ikkuna_canvas.create_text(180, 110 - 30, text=sana, font=10, fill="black")
        return sana_apina, valittu_sana, sana, henkilo
    else:
        sana = random.choice(sanat)
        sana_apina = ikkuna_canvas.create_image(180, 360, image=apina_kuva)
        valittu_sana = ikkuna_canvas.create_text(180, 360 - 30, text=sana, font=10, fill="black")
        return sana_apina, valittu_sana, sana, henkilo

# Liikutetaan apinaa ja sanaa
def liikuta_apina(apina_valinta, sana_valinta, sana, henkilo):
    global ernestin_sanat, kernestin_sanat, kernestin_apinat, ernestin_apinat
    matka = 300
    askel = 3
    delay = 0
    kuoleman_riski = 0.01
    for _ in range(0, matka, askel):
        time.sleep(delay)
        winsound.Beep(300, 50)
        ikkuna_canvas.move(apina_valinta, askel, 0)
        ikkuna_canvas.move(sana_valinta, askel, 0)

        # Tarkistetaan jokohan ernesti tai kernesti on hain mahassa
        if random.random() < kuoleman_riski:
            winsound.Beep(100, 500) 
            ikkuna_canvas.delete(apina_valinta)
            ikkuna_canvas.delete(sana_valinta)
            return 
    x, y = ikkuna_canvas.coords(apina_valinta)
    target_x = 480

    # Siirretään sanoja sivummalle ja soitetaan ääni jos perillä
    if x >= target_x:
        ikkuna_canvas.move(sana_valinta, random.randint(40, 400), random.randint(-50, 50))
        winsound.Beep(500, 400)
        if henkilo == "ernesti":
            ernestin_apinat += 1
        else:
            kernestin_apinat += 1

    tarkista_sanat(henkilo, sana)


# Laivan liikuttamis funktio
def liikuta_laiva(henkilo):
    global laiva_lahetetty
    if not laiva_lahetetty:
        matka = 200
        askel = -3
        delay = 0.1
        if henkilo == "ernesti":
            laiva = ikkuna_canvas.create_image(400, 100, image=laiva_kuva)
            laiva_lahetetty = True
            for i in range(0, matka, abs(askel)):
                time.sleep(delay)
                winsound.Beep(100, 50)
                ikkuna_canvas.move(laiva, askel, 0)
            print("Jipii ernesti voitti")
            ikkuna_canvas.create_text(100, 100, text="Jihuu!", font=14, fill="black")
        else:
            laiva = ikkuna_canvas.create_image(400, 350, image=laiva_kuva)
            laiva_lahetetty = True
            for i in range(0, matka, abs(askel)):
                time.sleep(delay)
                winsound.Beep(100, 50)
                ikkuna_canvas.move(laiva, askel, 0)
            print("Jipii kernesti voitti")
            ikkuna_canvas.create_text(100, 350, text="Jipii!", font=14, fill="black")
        juhla_laskelma()    
    else:
        print("Laiva on jo lähtenyt matkaan. Ei tarvetta toiselle!")            

# Tarkastellaan josko 10 sanaa olisi löytänyt perille    
def tarkista_sanat(henkilo, sana):   
    if henkilo == "ernesti":
        ernestin_sanat.add(sana)
        print(f"Ernestin sanat: {ernestin_sanat}")  
        if len(ernestin_sanat) >= 10:
            print("Ernesti sai 10 uniikkia sanaa perille, Jihuu!")
            liikuta_laiva(henkilo)
    elif henkilo == "kernesti":
        kernestin_sanat.add(sana)
        print(f"Kernestin sanat: {kernestin_sanat}")  
        if len(kernestin_sanat) >= 10:
            print("Kernesti sai 10 uniikkia sanaa perille, Jipii!") 
            liikuta_laiva(henkilo)

def juhla_laskelma():
    ernestin_juhlat = ernestin_apinat * 4
    kernestin_juhlat = kernestin_apinat * 4
    pippuria_yhteensa = (ernestin_apinat + kernestin_apinat) * 2
    viesti = (f"Ernestin päädyssä juhlitaan {ernestin_juhlat} ihmisen voimin ja "
                    f"Kernestin päässä {kernestin_juhlat} ihmisen voimin. "
                    f"Pippuria juhlissa kului yhteensä {pippuria_yhteensa} tl.")
    print(viesti)
    ikkuna_canvas.create_text(450, 480, text=viesti, font=14, fill="black")

# Lähetetään apina 
def laheta_apina(apina_valinta):
    apina, sana_valinta, sana, henkilo = maarita_sana_apina(apina_valinta)
    threading.Thread(target=liikuta_apina, args=(apina, sana_valinta, sana, henkilo)).start()

# Lähetetään 10 apinaa
def laheta_10_apinaa(apina_valinta): 
    for i in range(10):
        apina, sana_valinta, sana, henkilo = maarita_sana_apina(apina_valinta)
        threading.Thread(target=liikuta_apina, args=(apina, sana_valinta, sana, henkilo)).start()
        time.sleep(1)

# Napit
ernesti_laheta = tk.Button(ikkuna, text="Ernesti lähettää apinan", command=lambda: laheta_apina("ernesti"))
ernesti_laheta.place(x=50, y=10)
ernesti_laheta_10 = tk.Button(ikkuna, text="Ernesti lähettää 10 apinaa", command=lambda: threading.Thread(target=laheta_10_apinaa, args=("ernesti",)).start())
ernesti_laheta_10.place(x=200, y=10)

kernesti_laheta = tk.Button(ikkuna, text="Kernesti lähettää apinan", command=lambda: laheta_apina("kernesti"))
kernesti_laheta.place(x=50, y=430)
kernesti_laheta_10 = tk.Button(ikkuna, text="Kernesti lähettää 10 apinaa", command=lambda: threading.Thread(target=laheta_10_apinaa, args=("kernesti",)).start())
kernesti_laheta_10.place(x=200, y=430)

ikkuna.mainloop()