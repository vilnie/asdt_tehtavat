

import tkinter as tk
import random
import threading
import time
from PIL import Image, ImageTk
import numpy as np
import winsound
from threading import Lock


# Luodaan windowi
ikkuna = tk.Tk()
ikkuna.geometry("900x500")
ikkuna.title("Ernesti ja Kernesti autiosaarella")

# Tehdään canvas elementtejä varten 
ikkuna_canvas = tk.Canvas(ikkuna, width=900, height=500, bg="#2374AB")
ikkuna_canvas.pack()

# Saaren luonti
autiosaari = ikkuna_canvas.create_rectangle(100, 100, 800, 450, fill="#dcca73")
uima_allas = ikkuna_canvas.create_rectangle(390, 200, 510, 240, fill="#2380ab", outline="#2380ab")
oja_ernesti = ikkuna_canvas.create_rectangle(398, 100, 400, 200, fill="#2380ab", outline="#2380ab")
oja_kernesti = ikkuna_canvas.create_rectangle(500, 100, 502, 200, fill="#2380ab", outline="#2380ab")
for i in range(100):
        #Ernestin indikaattori
        aloitus_x_ernesti = 50  
        ikkuna_canvas.create_rectangle(
            aloitus_x_ernesti, 450 - (i * 4),
            aloitus_x_ernesti + 10, 450 - (i * 4) - 4,
            fill="yellow", outline="black", tags="ernestin_indikaattori"
        )
        #Kernestin indikaattori
        aloitus_x_kernesti = 850
        ikkuna_canvas.create_rectangle(
            aloitus_x_kernesti, 450 - (i * 4),
            aloitus_x_kernesti + 10, 450 - (i * 4) - 4,
            fill="yellow", outline="black", tags="kernestin_indikaattori"
        )       

# matriisit
matriisi_uima_allas = np.zeros((20, 60), dtype=int)
matriisi_ernestin_oja = np.ones((100, 1), dtype=int)
matriisi_kernestin_oja = np.ones((100, 1), dtype=int)

# kuvien koon muokkaus
def muokkaa_kuvan_kokoa(polku, uusi_leveys, uusi_korkeus):
    kuva = Image.open(polku)
    kuva = kuva.resize((uusi_leveys, uusi_korkeus), Image.Resampling.LANCZOS)
    valmis_kuva = ImageTk.PhotoImage(kuva)
    return valmis_kuva

ernesti_kuva = muokkaa_kuvan_kokoa("uima-allas_assets/erne.png", 40, 40)
kernesti_kuva = muokkaa_kuvan_kokoa("uima-allas_assets/kerne.png", 40, 40)
metsä_kuva = muokkaa_kuvan_kokoa("uima-allas_assets/metsä.jpg", 200, 100)
apina_kuva = muokkaa_kuvan_kokoa("uima-allas_assets/apina.png", 30, 20)
apina_töissä_kuva = muokkaa_kuvan_kokoa("uima-allas_assets/apina_töissä.png", 30, 20)
lapio_kuva = muokkaa_kuvan_kokoa("uima-allas_assets/lapio.png", 20, 40)

metsä = ikkuna_canvas.create_image(680, 180, image=metsä_kuva)
ernesti = ikkuna_canvas.create_image(360, 210, image=ernesti_kuva)
kernesti = ikkuna_canvas.create_image(540, 210, image=kernesti_kuva)
#lapio = ikkuna_canvas.create_image(260, 410, image=lapio_kuva)

apinat = []
seuraava_työllistettävä_apina = 0
apina_lähetetty = False
ernesti_lähetetty = False
kernesti_lähetetty = False
ernesti_after_id = None
ernesti_300 = False
kernesti_300 = False
työt_käynnissä = False
ernesti_10_inkrementti = 0
kernesti_10_inkrementti = 0

#luodaan apinat metsään
for i in range(20):
    rng_x = random.randint(580, 770)
    rng_y = random.randint(120, 250)
    apina = ikkuna_canvas.create_image(rng_x, rng_y, image=apina_kuva)
    apinat.append({'id': apina, 'töissä': False, 'työnantaja': None})

# tulostetaan matriisit terminaaliin vaakatasossa
def tulosta_matriisi(matriisi):
    if matriisi == "ernesti":
        print("ernestin oja:")
        matriisi_vaakatasossa = matriisi_ernestin_oja.flatten()
        print(' '.join(map(str, matriisi_vaakatasossa)))
    elif matriisi == "kernesti":
        print("kernestin oja:")
        matriisi_vaakatasossa = matriisi_kernestin_oja.flatten()
        print(' '.join(map(str, matriisi_vaakatasossa)))   
    else:
        return     

def soita_ääni():
    winsound.Beep(500, 1000)

def nouda_apina(henkilo):
    if henkilo == "ernesti":
        threading.Thread(target=nouda_apina_ernesti).start()
    else:
        threading.Thread(target=nouda_apina_kernesti).start()  

# hae henkilön alkuperäinen sijainti
def alkup_sijainti(henkilo):
    if henkilo == "ernesti":
        return [360, 310]
    elif henkilo == "kernesti":
        return [540, 310]
    
# Ernesti noutaa apinan töihin    
def nouda_apina_ernesti():
    global ernesti_lähetetty, ernesti_after_id
    ernesti_sijainti = ikkuna_canvas.coords(ernesti) 

    if ernesti_sijainti[0] <= 580 and ernesti_lähetetty == False:
        threading.Thread(target=lambda: winsound.Beep(100, 70)).start()
        ikkuna_canvas.move(ernesti, 4, -2)
        ikkuna.after(50, lambda: nouda_apina_ernesti())
        if ernesti_sijainti[0] >= 570:
            #time.sleep(1)
            #soita_ääni()
            lähetä_apina("ernesti", False) 
            ernesti_lähetetty = True

    elif ernesti_sijainti[0] >= alkup_sijainti("ernesti")[0] and ernesti_lähetetty == True:
        threading.Thread(target=lambda: winsound.Beep(100, 70)).start()
        ikkuna_canvas.move(ernesti, -4, 2)
        ernesti_after_id = ikkuna.after(50, lambda: nouda_apina_ernesti()) 
        if ernesti_sijainti[0] <= alkup_sijainti("ernesti")[0]:
            #time.sleep(1)
            #soita_ääni()
            ikkuna.after_cancel(ernesti_after_id)
            ernesti_lähetetty = False   
            return  
    else:
        return    

# Kernesti noutaa apinan töihin        
def nouda_apina_kernesti():
    global kernesti_lähetetty
    kernesti_sijainti = ikkuna_canvas.coords(kernesti) 

    if kernesti_sijainti[0] <= 700 and kernesti_lähetetty == False:
        threading.Thread(target=lambda: winsound.Beep(100, 70)).start()
        ikkuna_canvas.move(kernesti, 4, -5)
        ikkuna.after(50, lambda: nouda_apina_kernesti())
        if kernesti_sijainti[0] >= 600:
            #time.sleep(1)
            #winsound.Beep(500, 1000)
            #soita_ääni()
            lähetä_apina("kernesti", False) 
            kernesti_lähetetty = True

    elif kernesti_sijainti[0] >= alkup_sijainti("kernesti")[0] and kernesti_lähetetty == True:
        threading.Thread(target=lambda: winsound.Beep(100, 70)).start()
        ikkuna_canvas.move(kernesti, -4, 5)
        kernesti_after_id = ikkuna.after(50, lambda: nouda_apina_kernesti()) 
        if kernesti_sijainti[0] <= alkup_sijainti("kernesti")[0]:
            #time.sleep(1)
            #winsound.Beep(500, 1000)
            #soita_ääni()
            ikkuna.after_cancel(kernesti_after_id)
            kernesti_lähetetty = False   
            return      
    else:
        return

def lähetä_apina(henkilo, monta_apinaa):
    global seuraava_työllistettävä_apina
    while seuraava_työllistettävä_apina < len(apinat):
        apina = apinat[seuraava_työllistettävä_apina]
        if not apina['töissä']:
            apina['töissä'] = True
            apina['työnantaja'] = henkilo
            print(apina)
            threading.Thread(target=lähetä_apina_ojalle, args=(apina['id'], henkilo, monta_apinaa)).start()
            seuraava_työllistettävä_apina += 1
            break
        seuraava_työllistettävä_apina += 1

#viedään apinat ojalle odottamaan kaivamiskäskyä
def lähetä_apina_ojalle(apina_id, henkilo, monta_apinaa):
    global ernesti_300, kernesti_300, työt_käynnissä, ernesti_10_inkrementti, kernesti_10_inkrementti

    ikkuna_canvas.itemconfig(apina_id, image=apina_töissä_kuva)
    meri_y = 100
    apina_sijainti = ikkuna_canvas.coords(apina_id)
    x_tavoite = 0
    y_tavoite = 0

    #Jos lähetetään 10 apinaa, käytetään tätä logiikkaa
    if monta_apinaa:
        if henkilo == "ernesti":
            if ernesti_10_inkrementti == 0:
                x_tavoite = 420
                y_tavoite = random.randint(110, 200) - apina_sijainti[1]
                ernesti_10_inkrementti += 1
            else:
                x_tavoite = 420
                y_tavoite = 201 - apina_sijainti[1] - ernesti_10_inkrementti
                ernesti_10_inkrementti += 13
        else:
            if kernesti_10_inkrementti == 0:
                x_tavoite = 525
                y_tavoite = random.randint(110, 200) - apina_sijainti[1]
                kernesti_10_inkrementti += 1
            else:
                x_tavoite = 525
                y_tavoite = 201 - apina_sijainti[1] - kernesti_10_inkrementti
                kernesti_10_inkrementti += 13           
    #Jos lähetetään 1 apina, käytetään tätä logiikkaa
    else:    
        if henkilo == "ernesti":
            x_tavoite = 420 
            if not ernesti_300:
                y_tavoite = 201 - apina_sijainti[1]
                ernesti_300 = True
            else:    
                y_tavoite = random.randint(110, 200) - apina_sijainti[1]
        else:
            x_tavoite = 525
            if not kernesti_300:
                y_tavoite = 201 - apina_sijainti[1]
                kernesti_300 = True
            else:    
                y_tavoite = random.randint(110, 200) - apina_sijainti[1]

    while apina_sijainti[0] > x_tavoite:
        ikkuna_canvas.move(apina_id, -5, 0)
        apina_sijainti = ikkuna_canvas.coords(apina_id)
        time.sleep(0.1)     
    ikkuna_canvas.move(apina_id, 0, y_tavoite)

    if työt_käynnissä:
        apina_sijainti = ikkuna_canvas.coords(apina_id)
        threading.Thread(target=liikuta_työläisiä, args=(apina_id, henkilo, apina_sijainti, meri_y)).start()

#lähetetään 10 apinaa kerrallaan threadingin avulla
def lähetä_10_apinaa_ojalle(henkilo):
    global työt_käynnissä
    työt_käynnissä = True
    for i in range(1, 10):
        threading.Timer(i, lähetä_apina, args=(henkilo, True)).start()

def kaiva_oja():
    global apinat, työt_käynnissä
    print("kaivetaaaaaaaaaaaaaaaaaan")
    työt_käynnissä = True
    meri_y = 100
    allas_y = 300
    
    for apina in apinat:
        if apina['töissä']:
            apina_sijainti = ikkuna_canvas.coords(apina['id'])
            threading.Thread(target=liikuta_työläisiä, args=(apina['id'], apina['työnantaja'], apina_sijainti, meri_y)).start()

#liikutetaan apinoita yksi askel kerrallaan ja kaivetaan ojaa
def liikuta_työläisiä(apina_id, työnantaja, apina_sijainti, meri_y):
    levähdys_aika = 1
    while apina_sijainti[1] > meri_y:
        for apina in apinat:
            if apina['id'] == apina_id:
                if not apina['töissä']: 
                    return
        apina_sijainti = ikkuna_canvas.coords(apina_id)
        kaivettava_kohta = int(apina_sijainti[1] - 100)
        time.sleep(levähdys_aika)
        winsound.Beep(50, 50)
        #levähdys_aika *= 2
        if työnantaja == "ernesti" and 0 <= kaivettava_kohta < len(matriisi_ernestin_oja):
            matriisi_ernestin_oja[kaivettava_kohta] -= 1

        elif työnantaja == "kernesti" and 0 <= kaivettava_kohta < len(matriisi_ernestin_oja):
            matriisi_kernestin_oja[kaivettava_kohta] -= 1  
        ikkuna_canvas.move(apina_id, 0, -1)
        päivitä_indikaattori()    

#Päivitetään ojan kaivamis indikaattoreita
def päivitä_indikaattori():
    for i in range(100):
        index = ikkuna_canvas.find_withtag("ernestin_indikaattori")[i]
        e_o = matriisi_ernestin_oja[i]
        uusi_väri = "green" if e_o == 0 else "yellow" if e_o == 1 else "blue"
        ikkuna_canvas.itemconfig(index, fill=uusi_väri)
    for i in range(100):
        index = ikkuna_canvas.find_withtag("kernestin_indikaattori")[i]
        k_o = matriisi_kernestin_oja[i]
        uusi_väri = "green" if k_o < 1 else "yellow"
        ikkuna_canvas.itemconfig(index, fill=uusi_väri)      
 
#lähetetään apinat takaisin metsään ja täytetään ojat
def täytä_ojat():
    global matriisi_ernestin_oja, matriisi_kernestin_oja, matriisi_uima_allas, työt_käynnissä
    työt_käynnissä = False
    for apina in apinat:
        apina["töissä"] = False
        sijainti = ikkuna_canvas.coords(apina['id'])
        rng_x = random.randint(580, 770) - sijainti[0]
        rng_y = random.randint(120, 250) - sijainti[1]
        ikkuna_canvas.move(apina['id'], rng_x, rng_y)
        
    matriisi_uima_allas = np.zeros((20, 60), dtype=int)
    matriisi_ernestin_oja = np.ones((100, 1), dtype=int)
    matriisi_kernestin_oja = np.ones((100, 1), dtype=int)
    päivitä_indikaattori()    


#nappulat
ernesti_laheta = tk.Button(ikkuna, text="Ernesti lähettää apinan", command=lambda: nouda_apina("ernesti"))
ernesti_laheta.place(x=100, y=10)
kernesti_laheta = tk.Button(ikkuna, text="Kernesti lähettää apinan", command=lambda: nouda_apina("kernesti"))
kernesti_laheta.place(x=250, y=10)

ernesti_laheta_10 = tk.Button(ikkuna, text="Ernesti lähettää 10 apinaa", command=lambda: lähetä_10_apinaa_ojalle("ernesti"))
ernesti_laheta_10.place(x=100, y=50)
kernesti_laheta_10 = tk.Button(ikkuna, text="Kernesti lähettää 10 apinaa", command=lambda: lähetä_10_apinaa_ojalle("kernesti"))
kernesti_laheta_10.place(x=250, y=50)

kaiva_oja_nappi = tk.Button(ikkuna, text="Aloita kaivaminen", command=lambda: kaiva_oja())
kaiva_oja_nappi.place(x=450, y=10)
täytä_oja_nappi = tk.Button(ikkuna, text="Täytä ojat", command=lambda: täytä_ojat())
täytä_oja_nappi.place(x=450, y=50)

näytä_ernestin_oja = tk.Button(ikkuna, text="näytä ernestin oja", command=lambda: tulosta_matriisi("ernesti"))
näytä_ernestin_oja.place(x=600, y=10)
näytä_kernestin_oja = tk.Button(ikkuna, text="näytä kernestin oja", command=lambda: tulosta_matriisi("kernesti"))
näytä_kernestin_oja.place(x=600, y=50)

ikkuna.mainloop()
