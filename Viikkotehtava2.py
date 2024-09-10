

import numpy as np
import matplotlib.pyplot as plt
import tkinter
from tkinter import ttk
import random
import time
import winsound
import threading
import tkinter.messagebox as messagebox

#luodaan dictionary ennätysajoille (ois voinu laittaa erilliseen tiedostoon, mutta 
#en sisällyttänyt samoja aikoja kahdesti, niin jäi lyhyeksi)
world_records = {
    10.8: {"year": 1900, "holder": "Frank Jarvis"},
    10.6: {"year": 1912, "holder": "Donald Lippincott"},
    10.4: {"year": 1921, "holder": "Charlie Paddock"},
    10.3: {"year": 1930, "holder": "Percy Williams"},
    10.2: {"year": 1956, "holder": "Willie Williams"},
    10.0: {"year": 1960, "holder": "Armin Hary"},
    9.95: {"year": 1968, "holder": "Jim Hines"},
    9.93: {"year": 1983, "holder": "Calvin Smith"},
    9.79: {"year": 1988, "holder": "Ben Johnson"},
    9.86: {"year": 1991, "holder": "Carl Lewis"},
    9.85: {"year": 1994, "holder": "Leroy Burrell"},
    9.84: {"year": 1996, "holder": "Donovan Bailey"},
    9.77: {"year": 2005, "holder": "Asafa Powell"},
    9.72: {"year": 2008, "holder": "Usain Bolt"},
    9.58: {"year": 2009, "holder": "Usain Bolt"},
    None: {"year": 2050, "holder": None},
    5.3: {"year": None, "holder": "Lion1"},
    5.4: {"year": None, "holder": "Lion2"},
    5.8: {"year": None, "holder": "Lion3"},
    6.0: {"year": None, "holder": "Lion4"},
    6.1: {"year": None, "holder": "Lion5"},
    6.2: {"year": None, "holder": "Lion6"},
    6.3: {"year": None, "holder": "Lion7"},
    6.6: {"year": None, "holder": "Lion8"},
    6.8: {"year": None, "holder": "Lion9"},
    6.9: {"year": None, "holder": "Lion10"},
}

#luodaan omat arrayt ajoille ja vuosille
times = [time for time in world_records if world_records[time]["year"] is not None]
years = [world_records[time]["year"] for time in times]

#tehdään graafi
plt.figure(figsize=(10, 6))
plt.plot(years, times, marker='o', linestyle='-', color='b', label='World Record Progression')
plt.xlabel('Year')
plt.ylabel('100m World Record Time (seconds)')
plt.title('Progression of 100m World Record Time (1900-2050)')
plt.gca().invert_yaxis()
plt.legend()
#plt.show()


#luodaan tkinterillä graafinen käyttöliittymä
root = tkinter.Tk()
root.title('Ernestin ja Kernestin seikkailut')

canvas = tkinter.Canvas(root, width=500, height=200)
canvas.pack()

start_line = canvas.create_line(100, 50, 100, 150, fill="black", width=5)
finish_line = canvas.create_line(500, 50, 500, 150, fill="red", width=5)

ernesti = canvas.create_rectangle(80, 60, 100, 80, fill="blue")
kernesti = canvas.create_rectangle(80, 100, 100, 120, fill="green")

ernesti_time = 0
kernesti_time = 0

# Funktio, joka simuloi Ernestin juoksuar
def run_ernesti():
    global ernesti_time
    canvas.coords(ernesti, 80, 60, 100, 80)
    ernest_speed = random.uniform(0.3, 0.25)
    start_time = time.time()
    for _ in range(100, 500, 10):
        canvas.move(ernesti, 10, 0)
        root.update()
        time.sleep(ernest_speed)
    end_time = time.time()
    ernesti_time = end_time - start_time
    print("Ernesti saapui maaliin!")
    root.after(0, check_winner)

# Funktio, joka simuloi Kernestin juoksua
def run_kernesti():
    global kernesti_time
    canvas.coords(kernesti, 80, 120, 100, 140)
    kernest_speed = random.uniform(0.3, 0.25)
    start_time = time.time()
    for _ in range(100, 500, 10):
        canvas.move(kernesti, 10, 0)
        root.update()
        time.sleep(kernest_speed)
    end_time = time.time()
    kernesti_time = end_time - start_time    
    print("Kernesti saapui maaliin!")
    root.after(0, check_winner)

#Tarkastetaan voittaja ja luodaan ilmoitus
def check_winner():
    if ernesti_time > 0 and kernesti_time > 0:
        if ernesti_time < kernesti_time:
            winner = f"Ernesti voitti ajalla {ernesti_time:.2f} sekuntia!"
        elif kernesti_time < ernesti_time:
            winner = f"Kernesti voitti ajalla {kernesti_time:.2f} sekuntia!"
        else:
            winner = "Ernesti ja Kernesti päätyivät tasapeliin!"
        
        messagebox.showinfo("Kisa päättyi!", winner)

def start_running():
    ernest_thread = threading.Thread(target=run_ernesti)
    kernest_thread = threading.Thread(target=run_kernesti)

    ernest_thread.start()
    kernest_thread.start()

#Painikkeet juoksujen käynnistämiseen
ernesti_button = tkinter.Button(root, text="Aloita", command=start_running)
ernesti_button.pack()

root.mainloop()
