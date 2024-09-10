

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

#luodaan viidakko
fig, ax = plt.subplots()
viidakko = np.zeros([100, 100], dtype=int)
ax.imshow(viidakko, cmap='terrain', origin='lower')

#määritetään napit
ax_aloita_button = plt.axes([0.4, 0.05, 0.2, 0.075])  
ax_lopeta_button = plt.axes([0.01, 0.01, 0.2, 0.075]) 
aloita_button = Button(ax_aloita_button, 'aloita')
lopeta_button = Button(ax_lopeta_button, 'lopeta')

def aloita(event):

    def rng(x, y):
        return np.random.randint(x, y)

    #sijainnit
    ernesti_aloitus = np.array([rng(1, 100), rng(1, 100)])
    kernesti_aloitus = np.array([rng(1, 100), rng(1, 100)])

    #tapaamispaikan määritys
    tapaamispaikkaX = (ernesti_aloitus[0] + kernesti_aloitus[0]) / 2
    tapaamispaikkaY = (ernesti_aloitus[1] + kernesti_aloitus[1]) / 2 
    tapaamispaikka = (int(tapaamispaikkaX), int(tapaamispaikkaY))
    print(tapaamispaikka)

    num_steps = 20

    plt.ion()
    tolerance = 1e-2

    for step in range(num_steps):
        ax.clear()
        ax.imshow(viidakko, cmap='terrain', origin='lower') 

        # Lasketaan sijainti askelille
        ernesti_sijainti = ernesti_aloitus + (np.array(tapaamispaikka) - ernesti_aloitus) * (step + 1) / num_steps
        kernesti_sijainti = kernesti_aloitus + (np.array(tapaamispaikka) - kernesti_aloitus) * (step + 1) / num_steps

        # Näytetään kaverukset kartalla
        ax.scatter(ernesti_sijainti[0], ernesti_sijainti[1], color='blue', marker='o', s=50, label='Ernesti')
        ax.scatter(kernesti_sijainti[0], kernesti_sijainti[1], color='red', marker='o', s=50, label='Kernesti')
        ax.legend()

        plt.draw()
        plt.pause(0.5)  

        if abs(ernesti_sijainti[0] - kernesti_sijainti[0]) < tolerance and abs(ernesti_sijainti[1] - kernesti_sijainti[1]) < tolerance:
            print('Vau, onpa mukava nähdä taas!')
            break

    plt.ioff()  
    plt.show() 

def lopeta(event):
    exit()

aloita_button.on_clicked(aloita)
lopeta_button.on_clicked(lopeta)

plt.show()

