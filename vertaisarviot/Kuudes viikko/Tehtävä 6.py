import tkinter as tk
from PIL import ImageTk, Image
import random
import time
import threading
import winsound
# Koodin runko on saatu copilotilta

#**************ALUSTUKSET***********
#Globaalit muuttujat
maaritetty = False
altaanLeveys = 60
altaanKorkeus = 20
ojaLeveys = 1 
ojaKorkeus = 100
suuruusKerroin = 4 #Suurentaa saarta ja ojia
apinat = []

# Piirretään uima-allas saaren keskelle (20x60 metriä) 
allas_x0 = 300
allas_y0 = 500 
allas_x1 = allas_x0 + (60*suuruusKerroin)
allas_y1 = allas_y0 + (20*suuruusKerroin) 

# Piirretään Ernestin oja (100x1 metriä) 
ernestiOja_x0 = allas_x0
ernestiOja_y0 = allas_y0 - (100*suuruusKerroin)
ernestiOja_x1 = ernestiOja_x0 + (1*suuruusKerroin)
ernestiOja_y1 = ernestiOja_y0 + (100*suuruusKerroin) 

# Piirretään Kernestin oja (100x1 metriä)
kernestiOja_x0 = allas_x1 - (1*suuruusKerroin)
kernestiOja_y0 = allas_y0 - (100*suuruusKerroin)
kernestiOja_x1 = kernestiOja_x0 + (1*suuruusKerroin)
kernestiOja_y1 = kernestiOja_y0 + (100*suuruusKerroin)

# Menu ikkuna
menuIkkuna = tk.Tk()
menuIkkuna.geometry('400x400')
menuIkkuna.configure(bg='white')

# Kuvat kansiosta
apina = Image.open('Kuvat/apina.png')
apina = apina.resize((20, 20))
metsä = Image.open('Kuvat/mehtä.webp')
metsä = metsä.resize((500, 800))

# Apina
apina_image = ImageTk.PhotoImage(apina)

# Metsä
metsä_image = ImageTk.PhotoImage(metsä)

# Määritellään matriisit
ojaVasemmalla = [[1] for _ in range(100)]
ojaOikealla = [[1] for _ in range(100)]
allasMatriisi = [[0 for _ in range(altaanLeveys)] for _ in range(altaanKorkeus)]

def alustaTehtavaIkkuna():
    global tehtavaIkkuna, canvas, maaritetty
    tehtavaIkkuna = tk.Toplevel(menuIkkuna)
    tehtavaIkkuna.geometry('800x600')
    tehtavaIkkuna.configure(bg='white')
    
    # Piirretään saari 
    canvas = tk.Canvas(tehtavaIkkuna, width=800, height=600, bg='lightblue')
    canvas.pack(expand=True)
    saaren_x0, saaren_y0 = 0, -800
    saaren_x1, saaren_y1 = 1400, 1000
    canvas.create_arc(saaren_x0, saaren_y0, saaren_x1, saaren_y1, start=180, extent=180, outline="black", fill="gold3", width=2)

    #Sijoitetaan metsä saarelle
    canvas.create_image(850, 325, image=metsä_image)  
    maaritetty = True

def maaritaAllas():
    global maaritetty, altaanLeveys, altaanKorkeus
    if not maaritetty:
        alustaTehtavaIkkuna()
    paivitaRuutu()
    
#**************Funktiot*************
# 1 pisteen funkkarit.
def paivitaRuutu():
    # Allas
    for i in range(altaanKorkeus):
        for j in range(altaanLeveys):
            canvas.create_rectangle(
                allas_x0 + j * suuruusKerroin, allas_y0 + i * suuruusKerroin, 
                allas_x0 + (j + 1) * suuruusKerroin, allas_y0 + (i + 1) * suuruusKerroin, 
                outline="black", fill="grey"
            )
    
    # Oja
    for i in range(ojaKorkeus):
        if ojaVasemmalla[i][0] == 1:
            canvas.create_rectangle(
                ernestiOja_x0, ernestiOja_y0 + i * suuruusKerroin, 
                ernestiOja_x0 + ojaLeveys * suuruusKerroin, ernestiOja_y0 + (i + 1) * suuruusKerroin, 
                outline="black", fill="gold3"
            )
        if ojaOikealla[i][0] == 1:
            canvas.create_rectangle(
                kernestiOja_x0, kernestiOja_y0 + i * suuruusKerroin, 
                kernestiOja_x0 + ojaLeveys * suuruusKerroin, kernestiOja_y0 + (i + 1) * suuruusKerroin, 
                outline="black", fill="gold3"
            )
def eka_piste():
    maaritaAllas()

# 2 pisteen funkkarit.
def sijoitaApinat():
    for _ in range(20):
        x = random.randint(600, 800)
        y = random.randint(200, 500) 
        apina = canvas.create_image(x, y, image=apina_image)
        apinat.append(apina)

def haeApina():
    print("Ernesti lähtee hakemaan apinaa")
    apina_thread = threading.Thread(target=siirraApinaErnestinOjalle)
    apina_thread.start()

def siirraApinaErnestinOjalle():
    if apinat:
        print("Annetaan apinalle lapio ja nakitetaan se Ernestin ojalle")
        apina = apinat.pop(0)
        x, y = canvas.coords(apina)
        # Siirrä apina Ernestin ojalle (pisteiden A_e ja B_e välille)
        random_y = random.randint(ernestiOja_y0, ernestiOja_y1 - suuruusKerroin)
        for i in range(20):
            new_x = x - i * (x - ernestiOja_x0) / 20
            new_y = y - i * (y - random_y) / 20
            canvas.coords(apina, new_x, new_y)
            canvas.update()
            time.sleep(0.1)
        aloitaKaivaminen(apina)
    else:
        print("Apinat loppuivat:(")

def aloitaKaivaminen(apina):
    kaivuu_aika = 1
    x, y = canvas.coords(apina)
    start_index = int((y - ernestiOja_y0) // suuruusKerroin)
    for i in range(start_index, -1, -1):
        if ojaVasemmalla[i][0] == 1:
            ojaVasemmalla[i][0] = 0
            canvas.create_rectangle(
                ernestiOja_x0, ernestiOja_y0 + i * suuruusKerroin, 
                ernestiOja_x0 + ojaLeveys * suuruusKerroin, ernestiOja_y0 + (i + 1) * suuruusKerroin, 
                outline="black", fill="saddle brown"
            )
            winsound.Beep(1000, 100)
            canvas.update()
            time.sleep(kaivuu_aika)
            kaivuu_aika *= 2
            y -= 4
            canvas.coords(apina, x, y)
            canvas.update()

def toka_piste():
    maaritaAllas()
    sijoitaApinat()
    laheta=tk.Button(canvas,text="Lähetä ernestin ojalle", command=haeApina)
    laheta.place(x=0, y=10)

#***************Painikkeet************
eka=tk.Button(menuIkkuna,text="         1p         ", command=eka_piste)
eka.place(x=150, y=10)
toka=tk.Button(menuIkkuna,text="         2p         ", command=toka_piste)
toka.place(x=150, y=50)

menuIkkuna.mainloop()