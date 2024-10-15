import tkinter as tk
import numpy as np
import threading
import winsound 

ikkuna = tk.Tk()
ikkuna.title("Autiolla saarella")
ikkuna.geometry("600x700+700+10")

canvas = tk.Canvas(ikkuna, width=500, height=400, bg="lightblue")
canvas.pack(padx=0, pady=10)

# saari 
saari = canvas.create_oval(100, 100, 400, 300, fill="#F0E68C")

# metsäalue
metsa_x1, metsa_y1, metsa_x2, metsa_y2 = 310, 150, 370, 250
metsa = canvas.create_rectangle(metsa_x1, metsa_y1, metsa_x2, metsa_y2, fill="green")

# uima-allas 20x60 matriisina
allas = np.zeros([20, 60])
allas_kuva = canvas.create_rectangle(220, 200, 280, 220)

# Ernesti ja Kernesti uima-altaan reunoille
erne = canvas.create_oval(210, 210, 220, 220, fill="blue")
label_erne = canvas.create_text(210, 230, text="Ernesti", font=("Arial", 8))

kerne = canvas.create_oval(280, 210, 290, 220, fill="red")
label_kerne = canvas.create_text(280, 230, text="Kernesti", font=("Arial", 8))

# ojat matriisina
ernen_oja = np.ones(100) 
kernen_oja = np.ones(100)  

ernen_oja_kuva = []  
for i in range(100):
    x = 221
    y = 100 + i
    ernen_oja_kuva.append(canvas.create_line(x, y, x, y + 1, fill="yellow"))

kernen_oja_kuva = []
for i in range(100):
    x = 279
    y = 100 + i
    kernen_oja_kuva.append(canvas.create_line(x, y, x, y + 1, fill="yellow"))

# apinat metsässä
apinat = {}
for i in range(1, 20 + 1):
    x = np.random.randint(metsa_x1, metsa_x2 - 7)
    y = np.random.randint(metsa_y1, metsa_y2 - 7)
    apina_id = canvas.create_oval(x, y, x + 7, y + 7, fill="brown")
    
    apinat[f"apina{i}"] = {
        "id": apina_id,
        "x": x,
        "y": y,
        "status": "metsässä"
    }

ei_apinoita_label = None

# joutilas apina metsästä ojalle
def opasta_apina(x_ojan_reuna):
    global ei_apinoita_label
    if apinat:
        apina_avain = np.random.choice(list(apinat.keys()))  
        apina = apinat[apina_avain]

        uusi_y = np.random.randint(100, 200)

        apina["x"] = x_ojan_reuna
        apina["y"] = uusi_y

        canvas.after(0, lambda: canvas.coords(apina["id"], apina["x"] + 3, apina["y"] + 3, apina["x"] + 10, apina["y"] + 10))

        apina["status"] = "ojalla"

    else:
        if not ei_apinoita_label:
            ei_apinoita_label = canvas.create_text(250, 50, text="EI APINOITA ENÄÄ", font=("Arial", 16), fill="red")
            canvas.after(2000, lambda: canvas.delete(ei_apinoita_label))

def erne_opastaa_apinaa():
    threading.Thread(target=opasta_apina, args=(221,)).start()

def kerne_opastaa_apinaa():
    threading.Thread(target=opasta_apina, args=(279,)).start()

def apina_kaivamaan(apina, x, y, ojamatrix, oja_kaivuu):
    nopeus = 1 
    aloitus_indeksi = int(y - 100) 

    def kaiva(i):
        nonlocal nopeus
        if i < len(ojamatrix):
            if ojamatrix[i] == 1: 
                ojamatrix[i] = 0  

                winsound.Beep(500, 60)
                canvas.itemconfig(oja_kaivuu[i], fill="black")

                uusi_y = 100 + i 
                canvas.coords(apina["id"], x + 3, uusi_y + 3, x + 10, uusi_y + 10)

                canvas.after(int(nopeus * 1000), lambda: kaiva(i + 1))

                nopeus *= 2

    kaiva(aloitus_indeksi) 
    apina["status"] = "metsässä"

def ernen_apina_kaivaa():
    for apina_avain, apina_arvo in apinat.items():
        if apina_arvo["status"] == "ojalla":  
            threading.Thread(target=apina_kaivamaan, args=(apina_arvo, 221, apina_arvo["y"], ernen_oja, ernen_oja_kuva)).start()
            apina_arvo["status"] = "kaivaa"
            break

def kernen_apina_kaivaa():
    for apina_avain, apina_arvo in apinat.items():
        if apina_arvo["status"] == "ojalla":
            threading.Thread(target=apina_kaivamaan, args=(apina_arvo, 279, apina_arvo["y"], kernen_oja, kernen_oja_kuva)).start()
            apina_arvo["status"] = "kaivaa"
            break

# napit
erne_hae_apina_button = tk.Button(ikkuna, text="Ernesti, hae apina", command=erne_opastaa_apinaa)
erne_hae_apina_button.pack(padx=10, pady=10)

kerne_hae_apina_button = tk.Button(ikkuna, text="Kernesti, hae apina", command=kerne_opastaa_apinaa)
kerne_hae_apina_button.pack(padx=10, pady=10)

ernen_apina_toihin_button = tk.Button(ikkuna, text="Ernestin apina töihin", command=ernen_apina_kaivaa)
ernen_apina_toihin_button.pack(padx=10, pady=10)

kernen_apina_toihin_button = tk.Button(ikkuna, text="Kernestin apina töihin", command=kernen_apina_kaivaa)
kernen_apina_toihin_button.pack(padx=10, pady=10)

ikkuna.mainloop()
