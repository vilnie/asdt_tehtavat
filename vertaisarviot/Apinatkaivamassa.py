import numpy as np
import matplotlib.pyplot as plt
import threading
import time
import winsound
import random

# Määrittele uima-allas (20x60 matriisi, kaikki arvot 0, koska se on tyhjä)
uima_allas = np.zeros((20, 60))

# Määrittele ojat (100x1 matriisi, kaikki arvot 1, koska ojassa on vielä hiekkaa)
ernestin_oja = np.ones((100, 1))  # 1 kuvaa hiekkaa ojassa
kernestin_oja = np.ones((100, 1))  # 1 kuvaa hiekkaa ojassa

# Tulosta uima-allas ja ojat, jotta nähdään niiden alustava tila
print("Uima-allas matriisi (tyhjä):")
print(uima_allas)

print("\nErnestin oja (hiekkaa):")
print(ernestin_oja)

print("\nKernestin oja (hiekkaa):")
print(kernestin_oja)

# Piirrä saari ja allas graafisesti

# Luo valtameri (sininen tausta)
ocean = np.ones((300, 300, 3))  # 300x300 pikseliä
ocean[:, :, 2] = 1  # Sininen valtameri

# Luo hiekkasaari (keltainen keskellä)
sand_color = [1.0, 0.9, 0.6]  # Keltainen hiekka (RGB-arvot)
ocean[100:200, 100:200] = sand_color  # Hiekkasaari keskellä

# Piirrä uima-allas saarelle (20x60, keltaisen hiekan alueella)
pool_color = [0.7, 0.7, 0.7]  # Harmaa väri, koska se on tyhjää painauma
ocean[120:140, 130:190] = pool_color  # Uima-allas

# Piirrä ojat (suunnitelmat ojista, joissa vielä hiekkaa)
# Ernestin oja (1 = hiekkaa)
oja_color = [0.9, 0.7, 0.5]  # Vaaleanruskea väri ojille (hiekka)
ocean[140:240, 135:136] = oja_color  # Ernestin oja hiekalla

# Kernestin oja (1 = hiekkaa)
ocean[140:240, 185:186] = oja_color  # Kernestin oja hiekalla

# Piirrä metsäalue (vihreä alue saarelle)
forest_color = [0.0, 0.5, 0.0]  # Tummanvihreä väri metsälle
ocean[150:180, 160:190] = forest_color  # Metsäalue saarelle

# Piirrä kuva
plt.imshow(ocean)
plt.title("Autio saari: uima-allas, ojat ja metsäalue")
plt.axis('off')  # Piilota akselit
plt.show()

# --- Apinakaivuu --- 

# Luodaan apinat (10 apinaa metsässä)
apinat = ["Apina_" + str(i) for i in range(1, 11)]
kernest_apinat = ["Kernest_Apina_" + str(i) for i in range(1, 11)]

# Funktio hakee joutilaan apinan metsästä (eli listasta)
def hae_joutilas_apina(apinat_lista):
    if apinat_lista:
        return apinat_lista.pop(0)  # Palauttaa ja poistaa ensimmäisen joutilaan apinan listasta
    return None

# Funktio, joka antaa apinalle lapion ja opastaa ojan reunalle (Ernestin oja)
def opasta_apina_ojalle(apina, aloituskohta):
    print(f"{apina} on saanut lapion ja siirtyy Ernestin ojalle.")
    return aloituskohta

# Kaivamisfunktio (simuloidaan apinan kaivuu ajan myötä väsymisilmiöiden kanssa)
def kaiva_ojaa(apina, oja, aloituskohta, ojan_nimi):
    print(f"{apina} alkaa kaivaa ojaa kohdasta {aloituskohta}.")
    
    kaivuunopeus = 1  # Ensimmäinen metri kaivetaan sekunnissa
    kohta = aloituskohta
    
    while kohta < len(oja) and oja[kohta] == 1:  # Kaivaa kunnes kohtaa kaivamatonta maata
        print(f"{apina} kaivaa metrin kohdassa {kohta}.")
        oja[kohta] = 0  # Päivitä ojan kohta kaivetuksi (0 = kaivettu)
        
        # Havainnollistetaan kaivuu
        print_ojatila(ernestin_oja, kernestin_oja)
        
        # Ääniefekti kaivamisesta
        winsound.Beep(1000, 200)  # 1000 Hz ääni 200 ms ajan
        
        # Aseta viive fysiologisten rajoitteiden perusteella
        time.sleep(kaivuunopeus)
        
        # Seuraava kaivuunopeus on kaksinkertainen, apina väsyy
        kaivuunopeus *= 2
        kohta += 1
        
    print(f"{apina} on valmis kaivuun osalta.")

# Funktio, joka tulostaa ojan tilan
def print_ojatila(ernestin_oja, kernestin_oja):
    ernestin_tila = "".join(["#" if cell == 1 else "." for cell in ernestin_oja])
    kernestin_tila = "".join(["#" if cell == 1 else "." for cell in kernestin_oja])
    print(f"Ernestin oja: {ernestin_tila}")
    print(f"Kernestin oja: {kernestin_tila}")

# Apina hakee lapion ja opastetaan ojan reunalle
apina = hae_joutilas_apina(apinat)
kernest_apina = hae_joutilas_apina(kernest_apinat)

if apina:
    aloituskohta = opasta_apina_ojalle(apina, 0)
    
    # Luodaan säie kaivuutyölle
    kaivuu_saeie = threading.Thread(target=kaiva_ojaa, args=(apina, ernestin_oja, aloituskohta, "Ernestin oja"))
    
    # Käynnistetään kaivuu
    kaivuu_saeie.start()
else:
    print("Ei joutilaita apinoita metsässä!")

# Toiminto apinoiden lisäämiseen
def lisaa_apina(ojat, ojan_nimi):
    apina = hae_joutilas_apina(apinat)  # Voit vaihtaa apinat-listan, jos lisätään Kernestille
    if apina:
        aloituskohta = 0
        # Etsi ensimmäinen kaivamaton kohta
        while aloituskohta < len(ojat) and ojat[aloituskohta] != 1:
            aloituskohta += 1
            
        if aloituskohta < len(ojat):
            opasta_apina_ojalle(apina, aloituskohta)
            kaivuu_saeie = threading.Thread(target=kaiva_ojaa, args=(apina, ojat, aloituskohta, ojan_nimi))
            kaivuu_saeie.start()
        else:
            print(f"{ojan_nimi} on jo kokonaan kaivettu.")
    else:
        print("Ei joutilaita apinoita metsässä!")

# Lisää uusi apina Ernestin ojaan
lisaa_apina(ernestin_oja, "Ernestin oja")

# Lisää uusi apina Kernestin ojaan
lisaa_apina(kernestin_oja, "Kernestin oja")

# --- Ojan täyttäminen ---
def tayta_oja(oja):
    for i in range(len(oja)):
        oja[i] = 1  # Muutetaan kaikki arvot takaisin "ykkösiksi"
        
# Täytetään ojat
tayta_oja(ernestin_oja)
tayta_oja(kernestin_oja)

# Uimaan lisäämisen toiminnallisuus
def tayta_uima_allas():
    for i in range(20):  # Täytetään uima-allasta 20 kertaa
        for j in range(60):
            if uima_allas[i][j] == 0:  # Tarkista onko allas tyhjää
                uima_allas[i][j] = 1  # Täytetään allas
                winsound.Beep(500, 200)  # 500 Hz ääni 200 ms ajan
                print(f"Uima-allasta täytetään kohdassa ({i}, {j}).")
                time.sleep(0.5)  # Viive täyttämisessä

# Käynnistetään uima-altaan täyttö
uima_allas_thread = threading.Thread(target=tayta_uima_allas)
uima_allas_thread.start()

# Funktio apinoiden sijoittamiseen
def sijoita_apinat(ojat, ojan_nimi):
    for i in range(10):
        apina = hae_joutilas_apina(apinat)
        if apina:
            # Sijoita apina satunnaisesti uima-altaan ja meren välille
            satunnainen_kohta = random.randint(0, 59)  # Satunnainen x-koordinaatti uima-altaalla
            print(f"{apina} on sijoitettu sijaintiin {satunnainen_kohta} {ojan_nimi} välillä.")
            kaivuu_saeie = threading.Thread(target=lisaa_apina, args=(ojat, ojan_nimi))
            kaivuu_saeie.start()
            time.sleep(1)  # Viive ennen seuraavaa apinaa
        else:
            print("Ei joutilaita apinoita metsässä!")

# Sijoitetaan apinat Ernestin ojaan
sijoita_apinat(ernestin_oja, "Ernestin oja")

# Sijoitetaan apinat Kernestin ojaan
sijoita_apinat(kernestin_oja, "Kernestin oja")
