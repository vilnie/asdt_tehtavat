
import tkinter as tk
import random
import threading
import time
from PIL import Image, ImageTk
import numpy as np
import winsound
from playsound import playsound
from threading import Lock



# Luodaan windowi
ikkuna = tk.Tk()
ikkuna.geometry("1000x600")
ikkuna.title("Apina saari")

# Tehdään canvas elementtejä varten 
ikkuna_canvas = tk.Canvas(ikkuna, width=1000, height=600, bg="#2374AB")
ikkuna_canvas.pack()

def muokkaa_kuvan_kokoa(polku, uusi_leveys, uusi_korkeus):
    kuva = Image.open(polku)
    kuva = kuva.resize((uusi_leveys, uusi_korkeus), Image.Resampling.LANCZOS)
    valmis_kuva = ImageTk.PhotoImage(kuva)
    return valmis_kuva

apina_kuva = muokkaa_kuvan_kokoa("assets/apina.png", 30, 30)
kuolema_kuva = muokkaa_kuvan_kokoa("assets/hitsplat.png", 30, 30)
laituri = muokkaa_kuvan_kokoa("assets/laituri.png", 60, 30)
laituri2 = muokkaa_kuvan_kokoa("assets/laituri2.png", 30, 60)

saaret = []
saarien_nimet = []
laiturit = []
apinat = []
saari_laskuri = 1
maalla_kuolleet = 0
merellä_kuolleet = 0

maalla_kuolleet_teksti = ikkuna_canvas.create_text(920, 550, text=f"Maalla kuolleet: {maalla_kuolleet}", 
                                                    font=("Arial", 12), fill="black")
merellä_kuolleet_teksti = ikkuna_canvas.create_text(920, 580, text=f"Merellä kuolleet: {merellä_kuolleet}", 
                                                    font=("Arial", 12), fill="black")                                                            

    
# Apina ääntelee niin kauan kun on elossa
def apinoiden_ääntely(apina_id):
    for apina in apinat:
        if apina["id"] == apina_id:
            ääntelijä = apina
    while ääntelijä["elossa"]:
        taajuus = random.randint(400, 2000)
        winsound.Beep(taajuus, 500)
        time.sleep(random.randint(7, 15))

def tarkista_kuolema(apina_id):
    global maalla_kuolleet, merellä_kuolleet, apinat, saaret, saarien_nimet

    # Haetaan oikean apinan tiedot listasta
    apinoita = None
    apina_laskuri = None
    apina_valinta = None
    kuoleman_riski = 0.01

    for apina in apinat:
        if apina["id"] == apina_id:
            apina_valinta = apina   
    for saari in saaret: 
        if apina_valinta["saari"] == saari["saari_numero"]:
            apina_laskuri = saari["apina_laskuri"]
            apinoita = saari["apinat"]

    while apina_valinta["elossa"]:
        if apina_valinta["maalla"]:
            time.sleep(10)
            if random.random() < kuoleman_riski:
                apina_valinta["elossa"] = False
                saari["apinat"] -= 1
                ikkuna_canvas.itemconfig(apina_laskuri, text="Apinoita: " + str(saari["apinat"]))
                ikkuna_canvas.itemconfig(apina_valinta["id"], image=kuolema_kuva)
                playsound('assets/kids-laugh.wav')
                time.sleep(0.3)
                ikkuna_canvas.delete(apina_valinta["id"])
                print(apina_valinta["id"], "kuoli :(")
                maalla_kuolleet += 1 
                ikkuna_canvas.itemconfig(maalla_kuolleet_teksti, text=f"Maalla kuolleet: {maalla_kuolleet}")
                return
        else:
            time.sleep(1)
            if random.random() < kuoleman_riski:
                apina_valinta["elossa"] = False
                ikkuna_canvas.itemconfig(apina_laskuri, text="Apinoita: " + str(saari["apinat"]))
                ikkuna_canvas.itemconfig(apina_valinta["id"], image=kuolema_kuva)
                playsound('assets/kids-laugh.wav')
                time.sleep(0.3)
                ikkuna_canvas.delete(apina_valinta["id"])
                print(apina_valinta["id"], "kuoli :(") 
                merellä_kuolleet += 1 
                ikkuna_canvas.itemconfig(merellä_kuolleet_teksti, text=f"Merellä kuolleet: {merellä_kuolleet}")
                return



def lähetä_apinat_uimaan():
    apina = apinat[1]["id"]
    apinat[1]["maalla"] = False
    while True:
        ikkuna_canvas.move(apina, 3, 1)
        time.sleep(0.3)


def liikuta_apinaa(apina, apina_num):
    global apinat, saaret, saarien_nimet

    valittu_apina = None
    saari_valinta = None

    # Tarkistetaan onko apinaa apinalistalla
    for apsu in apinat:
        if apsu["id"] == apina_num:
            valittu_apina = apsu
            break   

    # Tarkistetaan saari jolla apina on
    for saari in saaret: 
        if valittu_apina['saari'] == saari["saari_numero"]:
            saari_valinta = saari
            break

    if saari_valinta and valittu_apina:
        apina_laskuri = saari_valinta["apina_laskuri"]
        saari_valinta["apinat"] -= 1

        valittu_apina["maalla"] = False
        ikkuna_canvas.itemconfig(apina_laskuri, text="Apinoita: " + str(saari_valinta["apinat"]))

        # Random suunta neljästä ilmansuunnasta
        suunta = {1: (0, -5), 
                2: (5, 0),
                3: (0, 5),
                4: (-5, 0)
        } 
        rng = random.randint(1, 4)
        askel_x , askel_y = suunta[rng]

        ääni_laskuri = 0
        while True:
            if not valittu_apina["elossa"]:
                break
            ääni_laskuri += 1
            ikkuna_canvas.move(apina, askel_x, askel_y)
            # Soitetaan uimisääni vain joka viides askel
            if ääni_laskuri % 7 == 0:
                threading.Thread(target = lambda: playsound('assets/swimming.wav')).start()
            x_koord, y_koord = ikkuna_canvas.coords(apina)
            x = int(x_koord)
            y = int(y_koord)
  
            # Tarkistetaan osuuko apina saareen
            for saari in saaret:
                saari_x1 = int(saari['x_koordinaatti'])
                saari_y1 = int(saari['y_koordinaatti'])
                saari_x2 = int(saari['x_koordinaatti2'])
                saari_y2 = int(saari['y_koordinaatti2'])  

                saari_num = saari["saari_numero"]
                # Tarkistetaan apinan törmäys saareen
                if (x > saari_x1 and x < saari_x2) and (y > saari_y1 and y < saari_y2) and saari_valinta["id"] != saari["id"]:
                    valittu_apina["saari"] = saari_num
                    saari["apinat"] += 1
                    uusi_apina_laskuri = saari["apina_laskuri"]
                    ikkuna_canvas.itemconfig(uusi_apina_laskuri, text="Apinoita: " + str(saari["apinat"]))
                    ikkuna_canvas.tag_raise(apina)
                    print("Apina löysi saaren S",saari_num)

                    luo_laiturit(saari["saari_numero"])
                    threading.Thread(target=lähetä_apina, args=(saari_num,)).start()
                    return

            time.sleep(0.3)



def lähetä_apina(saari_num):
    time.sleep(1)
    saaren_apinat = []
    for apina in apinat:
        if apina["saari"] == saari_num:
            saaren_apinat.append(apina["id"])
    print(saari_num,"saarella nämä apsut: ", saaren_apinat)
    while len(saaren_apinat) > 0:
        seuraava_apina = random.choice(saaren_apinat)
        saaren_apinat.remove(seuraava_apina)
        threading.Thread(target=liikuta_apinaa, args=(seuraava_apina, int(seuraava_apina))).start()
        time.sleep(10)
 

def tarkista_päällekkäisyys(x1, y1, x2, y2):
    for saari in saaret:
        saari_x1 = saari['x_koordinaatti']
        saari_y1 = saari['y_koordinaatti']
        saari_x2 = saari['x_koordinaatti2']
        saari_y2 = saari['y_koordinaatti2']  

        # Tarkistetaan päällekkäisyys
        if not (x1 > saari_x2 or y1 > saari_y2 or x2 < saari_x1 or y2 < saari_y1):
            return True
    return False
        

def luo_saari() :
    global saari_laskuri
    looppeja = 0

    # Loopatan sijainnin määritystä kunnes löydetään vapaa paikka
    while looppeja < 100:
        looppeja += 1
        x_koordinaatti = random.randint(0, 900)
        y_koordinaatti = random.randint(0, 500)
        x_koordinaatti2 = x_koordinaatti + 150
        y_koordinaatti2 = y_koordinaatti + 150

        päällä = tarkista_päällekkäisyys(x_koordinaatti, y_koordinaatti, x_koordinaatti2, y_koordinaatti2)
        if not päällä and x_koordinaatti2 < 1000 and y_koordinaatti2 < 600:
            break
        elif looppeja >= 98:
            print("Saaria ei mahdu enempää!")
            return
    
    # Luodaan saari ja lisätään listaan
    saari = ikkuna_canvas.create_rectangle(x_koordinaatti, y_koordinaatti, x_koordinaatti2,
                                            y_koordinaatti2, fill="#dcca73")
    saaren_nimi = ikkuna_canvas.create_text(x_koordinaatti + 70, y_koordinaatti + 70, text=f"S{saari_laskuri}", font=("Arial", 40), fill="black")
    ikkuna_canvas.tag_raise(saaren_nimi)
    
    saaret.append({'id': saari, 'saari_numero': saari_laskuri, 'nimi': f"S{saari_laskuri}",
                    'x_koordinaatti': x_koordinaatti, 'y_koordinaatti': y_koordinaatti,
                    'x_koordinaatti2': x_koordinaatti2, 'y_koordinaatti2': y_koordinaatti2, 
                    'apinat': 0, 'apina_laskuri': None, 'tietoisuus': False})
    saarien_nimet.append({'id': saaren_nimi, 'nimi': f"S{saari_laskuri}"})

    apinoita_saarella = ikkuna_canvas.create_text(x_koordinaatti + 70, y_koordinaatti + 100, text=f"Apinoita: {saaret[saari_laskuri-1]["apinat"]}", 
                                                    font=("Arial", 14), fill="black")
    saaret[saari_laskuri-1]["apina_laskuri"] = apinoita_saarella
    luo_laiturit(1)

    threading.Thread(target = lambda: playsound('assets/explosion.wav')).start()

    # Luodaan 10 apinaa joka saarelle ja aloitetaan ääntely 
    for i in range(10):
        rng_x = random.randint(x_koordinaatti, x_koordinaatti2)
        rng_y = random.randint(y_koordinaatti, y_koordinaatti2)
        apina = ikkuna_canvas.create_image(rng_x, rng_y, image=apina_kuva)
        apinat.append({'id': apina, 'elossa': True, 'maalla': True, 'saari': saari_laskuri})
        saaret[saari_laskuri-1]["apinat"] += 1
        threading.Thread(target=apinoiden_ääntely, args=(apina,)).start()
        threading.Thread(target=tarkista_kuolema, args=(apina,)).start()
    
    #threading.Thread(target=lähetä_apina, args=(saaret[saari_laskuri-1],)).start()

    ikkuna_canvas.itemconfig(apinoita_saarella, text="Apinoita: " + str(saaret[saari_laskuri-1]["apinat"]))
    saari_laskuri += 1
    #print(saaret[saari_laskuri]["apinat"])


# Luodaan laiturit
def luo_laiturit(saari_num):
    for saari in saaret:
        if saari["saari_numero"] == saari_num:
            saari_numero = saari["saari_numero"]
            x, y, x2, y2= ikkuna_canvas.coords(saari["id"])
            laituri_p = ikkuna_canvas.create_image(x + 70, y - 30, image=laituri2)
            laituri_e = ikkuna_canvas.create_image(x + 70, y + 180, image=laituri2)
            laituri_l = ikkuna_canvas.create_image(x - 30, y + 70, image=laituri)
            laituri_i = ikkuna_canvas.create_image(x + 180, y + 70, image=laituri)
            laiturit.append({'saari': saari_numero, 'laituri_p': laituri_p, 'laituri_e': laituri_e,
                            'laituri_l': laituri_l, 'laituri_i': laituri_i, })


# Tuhotaan saaret ja kaikki niihin liittyvä
def tuhoa_saaret():
    global saari_laskuri
    for saari in saaret:
        ikkuna_canvas.delete(saari["id"])
        ikkuna_canvas.delete(saari["apina_laskuri"])
    saaret.clear()

    for apina in apinat:
        apina["elossa"] = False
        ikkuna_canvas.delete(apina["id"])
    apinat.clear()

    for nimi in saarien_nimet:
        ikkuna_canvas.delete(nimi["id"])
    saarien_nimet.clear() 

    for laituri in laiturit:
        ikkuna_canvas.delete(laituri["laituri_p"], laituri["laituri_e"], 
                             laituri["laituri_l"], laituri["laituri_i"], )
    laiturit.clear() 

    saari_laskuri = 1   




tulivuorenpurkaus_nappi = tk.Button(ikkuna, text="Tulivuorenpurkaus", command=lambda: luo_saari())
tulivuorenpurkaus_nappi.place(x=10, y=10)

tuhoa_saaret_nappi = tk.Button(ikkuna, text="Tuhoa saaret", command=lambda: tuhoa_saaret())
tuhoa_saaret_nappi.place(x=10, y=50)

#luo_laiturit_nappi = tk.Button(ikkuna, text="Luo laiturit", command=lambda: luo_laiturit())
#luo_laiturit_nappi.place(x=500, y=10)

lähetä_apinat_uimaan_nappi = tk.Button(
    ikkuna, text="testi uinti",
    command=lambda: threading.Thread(target=lähetä_apinat_uimaan).start())
lähetä_apinat_uimaan_nappi.place(x=850, y=10)

lähetä_apina_satunnaisesti_nappi = tk.Button(
    ikkuna, text="aloita simulaatio", 
    command=lambda: threading.Thread(target=lähetä_apina, args=(1,)).start()
)
lähetä_apina_satunnaisesti_nappi.place(x=180, y=10)

ikkuna.mainloop()