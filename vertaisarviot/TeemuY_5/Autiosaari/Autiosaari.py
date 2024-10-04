import tkinter as tk
import winsound
import time
import threading
import numpy as np
import random

ikkuna = tk.Tk()
ikkuna.geometry("800x500+200+50")

canvas = tk.Canvas(ikkuna, width=800, height=500)
canvas.pack()

autiosaari = canvas.create_rectangle(100, 120, 200, 350, outline="black", width=2)
mantere = canvas.create_rectangle(550, 120, 650, 350, outline="green", width=2)

canvas.create_text(150, 100, text="Autio saari", font=20)
canvas.create_text(600, 100, text="Mantere", font=20)

hataviesti = [ "Ernesti", "Ja", "Kernesti", "Tässä", "Terve", "Olemme", "Autiolla", "Saarella", "Voisiko", "Joku", "Sieltä", "Sivistyneestä", "Maailmasta", "Tulla", "Hakemaan", "Meidät", "Pois" , "Kiitos"]

#Globaali dictionary
tiedot = {}
tiedot['apinamaara'] = 0
tiedot['apina'] = {}

def ernestin_apina():
    ernestin_apina_xkoordinaatti = 180
    ernestin_apina_ykoordinaatti = 200 
    ernestin_apina = canvas.create_text(ernestin_apina_xkoordinaatti, ernestin_apina_ykoordinaatti, text="Ernestin apina")
    
    for i in range(100):
        ernestin_apina_xkoordinaatti += 4
        ernestin_apina_ykoordinaatti = ernestin_apina_ykoordinaatti

        canvas.coords(ernestin_apina, ernestin_apina_xkoordinaatti, ernestin_apina_ykoordinaatti)
        time.sleep(0.5)

def kernestin_apina():
    kernestin_apina_xkoordinaatti = 180
    kernestin_apina_ykoordinaatti = 300
    kernestin_apina = canvas.create_text(kernestin_apina_xkoordinaatti, kernestin_apina_ykoordinaatti,text="Kernestin apina")

    for i in range(100):
        kernestin_apina_xkoordinaatti += 4
        kernestin_apina_ykoordinaatti = kernestin_apina_ykoordinaatti

        canvas.coords(kernestin_apina, kernestin_apina_xkoordinaatti, kernestin_apina_ykoordinaatti)
        time.sleep(0.5)

def opeta_apinalle_sana(apina_id):
    global tiedot
    sana = random.choice(hataviesti)
    tiedot['apina'][apina_id]['sana'] = sana

def luo_ernestin_apina_ja_laita_uimaan():
    global tiedot
    tiedot['apinamaara'] += 1
    apina_id = tiedot['apinamaara']
    #Tätä tiedon tallennusmuotoa kannattaa miettiä ja sisäistää...
    tiedot['apina'][apina_id] = {'nimi': 'Ernestin apinoita', 'x' : 180, 'y' : 200,'elossa' : 1, 'ID' : apina_id}
    winsound.Beep(440,500)
    time.sleep(0.5)

    #Havainnolistetaan apina näytölle
    apinakahva = canvas.create_text(tiedot['apina'][apina_id]['x'], tiedot['apina'][apina_id]['y'], text='E'+str(apina_id))
    
    #apinakahva.configure(fg='red')
    tiedot['apina'][apina_id]['kahva'] = apinakahva
    opeta_apinalle_sana(apina_id)

    for i in range(100):
        #Siirretään apinaa
        tiedot['apina'][apina_id]['x']=tiedot['apina'][apina_id]['x']+4
        tiedot['apina'][apina_id]['y']=tiedot['apina'][apina_id]['y']+np.random.randint(-2,2)

        canvas.coords(apinakahva, tiedot['apina'][apina_id]['x'], tiedot['apina'][apina_id]['y'])
        winsound.Beep(1000+apina_id*10,200)
        time.sleep(0.2)

        #Tarkistetaan, onko apina saavuttanut mantereen
        if tiedot['apina'][apina_id]['x'] >= 550:
            print(f"Apina {apina_id} saapui mantereelle ja sanoo: {tiedot['apina'][apina_id]['sana']}")
            winsound.Beep(100, 100)
            break
    
def luo_kernestin_apina_ja_laita_uimaan():
    global tiedot
    tiedot['apinamaara'] += 1
    apina_id = tiedot['apinamaara']
    tiedot['apina'][apina_id] = {'nimi': 'Kernestin apinoita', 'x' : 180, 'y' : 300,'elossa' : 1, 'ID' : apina_id}
    winsound.Beep(440,500)
    time.sleep(0.5)

    #Havainnolistetaan apina näytölle
    apinakahva = canvas.create_text(tiedot['apina'][apina_id]['x'], tiedot['apina'][apina_id]['y'], text='K'+str(apina_id))
    tiedot['apina'][apina_id]['kahva'] = apinakahva
    opeta_apinalle_sana(apina_id)

    for i in range(100):
        #Siirretään apinaa
        tiedot['apina'][apina_id]['x']=tiedot['apina'][apina_id]['x']+4
        tiedot['apina'][apina_id]['y']=tiedot['apina'][apina_id]['y']+np.random.randint(-2,2)

        canvas.coords(apinakahva, tiedot['apina'][apina_id]['x'], tiedot['apina'][apina_id]['y'])
        winsound.Beep(1000+apina_id*10,200)
        time.sleep(0.2)

        #Tarkistetaan, onko apina saavuttanut mantereen
        if tiedot['apina'][apina_id]['x'] >= 550:
            print(f"Apina {apina_id} saapui mantereelle ja sanoo: {tiedot['apina'][apina_id]['sana']}")
            winsound.Beep(100, 100)
            break    

def luo_ernestin_hai_apina():
    global tiedot
    tiedot['apinamaara'] += 1
    apina_id = tiedot['apinamaara']
    #Tätä tiedon tallennusmuotoa kannattaa miettiä ja sisäistää...
    tiedot['apina'][apina_id] = {'nimi': 'Ernestin apinoita', 'x' : 180, 'y' : 200,'elossa' : 1, 'ID' : apina_id}
    winsound.Beep(440,500)
    time.sleep(0.5)

    #Havainnolistetaan apina näytölle
    apinakahva = canvas.create_text(tiedot['apina'][apina_id]['x'], tiedot['apina'][apina_id]['y'], text='E'+str(apina_id))
    
    #apinakahva.configure(fg='red')
    tiedot['apina'][apina_id]['kahva'] = apinakahva
    opeta_apinalle_sana(apina_id)

    for i in range(100):
        #Siirretään apinaa
        tiedot['apina'][apina_id]['x']=tiedot['apina'][apina_id]['x']+4
        tiedot['apina'][apina_id]['y']=tiedot['apina'][apina_id]['y']+np.random.randint(-2,2)

        canvas.coords(apinakahva, tiedot['apina'][apina_id]['x'], tiedot['apina'][apina_id]['y'])
        winsound.Beep(1000+apina_id*10,200)
        time.sleep(0.2)

        #Tarkistetaan syökö hai apinan
        if random.random() < 0.00693:
            print(f"Hai söi apinan {apina_id}!")
            winsound.Beep(500, 500)
            canvas.delete(apinakahva)
            tiedot['apina'][apina_id]['elossa'] = 0
            break

        #Tarkistetaan, onko apina saavuttanut mantereen
        if tiedot['apina'][apina_id]['x'] >= 550:
            print(f"Apina {apina_id} saapui mantereelle ja sanoo: {tiedot['apina'][apina_id]['sana']}")
            break

def luo_kernestin_hai_apina():
    global tiedot
    tiedot['apinamaara'] += 1
    apina_id = tiedot['apinamaara']
    tiedot['apina'][apina_id] = {'nimi': 'Kernestin apinoita', 'x' : 180, 'y' : 300,'elossa' : 1, 'ID' : apina_id}
    winsound.Beep(440,500)
    time.sleep(0.5)

    #Havainnolistetaan apina näytölle
    apinakahva = canvas.create_text(tiedot['apina'][apina_id]['x'], tiedot['apina'][apina_id]['y'], text='K'+str(apina_id))
    tiedot['apina'][apina_id]['kahva'] = apinakahva
    opeta_apinalle_sana(apina_id)

    for i in range(100):
        #Siirretään apinaa
        tiedot['apina'][apina_id]['x']=tiedot['apina'][apina_id]['x']+4
        tiedot['apina'][apina_id]['y']=tiedot['apina'][apina_id]['y']+np.random.randint(-2,2)

        canvas.coords(apinakahva, tiedot['apina'][apina_id]['x'], tiedot['apina'][apina_id]['y'])
        winsound.Beep(1000+apina_id*10,200)
        time.sleep(0.2)

        #Tarkistetaan syökö hai apinan
        if random.random() < 0.00693:
            print(f"Hai söi apinan {apina_id}!")
            winsound.Beep(500, 500)
            canvas.delete(apinakahva)
            tiedot['apina'][apina_id]['elossa'] = 0
            break

        #Tarkistetaan, onko apina saavuttanut mantereen
        if tiedot['apina'][apina_id]['x'] >= 550:
            print(f"Apina {apina_id} saapui mantereelle ja sanoo: {tiedot['apina'][apina_id]['sana']}")
            break   

def ernestin_apina_saikeistin():
    kahva = threading.Thread(target=ernestin_apina)
    kahva.start()

def kernestin_apina_saikeistin():
    kahva = threading.Thread(target=kernestin_apina)
    kahva.start()

def luo_ernestin_apina_ja_laita_uimaan_saikeistin():
    kahva = threading.Thread(target=luo_ernestin_apina_ja_laita_uimaan)
    kahva.start()

def luo_kernestin_apina_ja_laita_uimaan_saikeistin():
    kahva = threading.Thread(target=luo_kernestin_apina_ja_laita_uimaan)
    kahva.start()    

def luo_ernestin_hai_apina_saikeistin():
    for _ in range(10):
        kahva = threading.Thread(target=luo_ernestin_hai_apina)
        kahva.start()

def luo_kernestin_hai_apina_saikeistin():
    for _ in range(10):
        kahva = threading.Thread(target=luo_kernestin_hai_apina)
        kahva.start()

def tarkkailija(kesto_sekunneissa):
    global tiedot
    alku_aika = time.time()  # Tallenna aloitusaika
    while True:
        elossa_olevat_apinat = 0
        for apina_id in tiedot['apina']:
            if tiedot['apina'][apina_id]['elossa'] == 1:
                elossa_olevat_apinat += 1
        print(f"Elossa olevia apinoita: {elossa_olevat_apinat}")
        
        # Tarkista, onko aika loppunut
        if time.time() - alku_aika > kesto_sekunneissa:
            print("Tarkkailu päättyi.")
            break

        time.sleep(1)

def tarkkaile_saikeistin(kesto_sekunneissa=10):
    kahva = threading.Thread(target=tarkkailija, args=(kesto_sekunneissa,))
    kahva.start() 

ernesti_eka_apina = tk.Button(text='Ernestin apina',command=ernestin_apina_saikeistin)
ernesti_eka_apina.place(x=30, y=400)

kernesti_eka_apina = tk.Button(text="Kernestin apina", command=kernestin_apina_saikeistin)
kernesti_eka_apina.place(x=250,y=400)

ernesti_lahettaa = tk.Button(text='Ernesti - sana',command=luo_ernestin_apina_ja_laita_uimaan_saikeistin)
ernesti_lahettaa.place(x=30,y=450)

kernesti_lahettaa = tk.Button(text='Kernesti - sana', command=luo_kernestin_apina_ja_laita_uimaan_saikeistin)
kernesti_lahettaa.place(x=250, y=450)

ernesti_riski_apina = tk.Button(text="Ernesti - hai", command=luo_ernestin_hai_apina_saikeistin)
ernesti_riski_apina.place(x=350, y=400)

kernesti_riski_apina = tk.Button(text="Kernesti - hai",command=luo_kernestin_hai_apina_saikeistin)
kernesti_riski_apina.place(x=350,y=450)

tarkkailija_painike=tk.Button(text='Tarkkaile 10s', command=lambda: tarkkaile_saikeistin(10))
tarkkailija_painike.place(x=150,y=450)

#Niksi
#ikkuna.after(5000,ikkuna.destroy)

ikkuna.mainloop()