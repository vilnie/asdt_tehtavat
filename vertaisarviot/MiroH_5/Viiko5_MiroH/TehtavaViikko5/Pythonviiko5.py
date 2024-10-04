import threading as th 
import tkinter as tk
from pathlib import Path
import os
from time import sleep
import winsound as ws
import random as rand
ikkuna = tk.Tk()
path = Path(__file__).resolve().parent
os.chdir(path=path)

ikkuna.geometry("1200x400")
canvas = tk.Canvas(width="1200",height="200",background="lightblue")

canvas.create_rectangle(1,1,100,200,fill="lightgreen")
canvas.create_text(50,100,text="Autiosaari")

canvas.create_rectangle(1200,1,1100,200,fill="lightgray")
canvas.create_text(1150,100,text="Mantere")

canvas.pack()

eernesti = tk.PhotoImage(file="./erne.png").subsample(6,6)
keernesti = tk.PhotoImage(file="./kerne.png").subsample(6,6)
monkey = tk.PhotoImage(file="./Monkey.png").subsample(12,12)
vene = tk.PhotoImage(file="./vene.png").subsample(6,6)
vene2 = tk.PhotoImage(file="./vene2.png").subsample(6,6)
vahti1  = tk.PhotoImage(file="./Eeteri.png").subsample(8,8)
vahti2  = tk.PhotoImage(file="./Pohteri.png").subsample(8,8)

canvas.create_image(80,25,image=eernesti)
canvas.create_image(80,175,image=keernesti)
Eeteripointer = canvas.create_image(1170,25, image=vahti1)
Pohteripointer = canvas.create_image(1170,175, image=vahti2)
Potheri = []
Eteri = []
Resepti = {
    "apina": 1,
    "kg perunoita" : 2,
    "dl kuohukermaa" :3,
    "tl mustapippuria":2,
    "tl suolaa" : 1,
}

Eernesti = {
    "name": "eernesti",
    "x_loc": 60,
    "y_loc": 25,
    "delivered": [],
    "Message": ["Apua", "Olemme", "Autiosaarella","jumissa", "meita", "on", "kaksi", "nalka", "jano", "vene"],
}

Keernesti = {
    "name": "keernesti",
    "x_loc": 60,
    "y_loc": 175,
    "delivered": [],
    "Message": ["Apua", "Olemme", "Autiosaarella","jumissa", "meita", "on", "kaksi", "nalka", "jano", "vene"],
}
for i in range(10):
    Keernesti["delivered"].append("")
    Eernesti["delivered"].append("")
    Potheri.append("")
    Eteri.append("")

Apinat = {

}

def makeabeep(f,d): 
    ws.Beep(f,d)

def animoivene(name): 
    animaatio = canvas.create_image(name["x_loc"]+1040,name["y_loc"],image=vene)
    for i in range(20):
        sleep(0.2)
        canvas.move(animaatio,-50,0)
    
    
def messagecheck(number,i): 
    if(Apinat[number]["sender"] == "keernesti"):
        print("keernesti: ", Apinat[number]["message"])
        Potheri[i] = Apinat[number]["message"]
    else:
        print("Eernesti: ", Apinat[number]["message"])
        Eteri[i] = Apinat[number]["message"]

def Guardvision(name,list,dict): 
    nameofguard = ""
    nameofsender= ""
    if(name == 7):
        nameofguard = "eeteri"
        nameofsender= "keernesti"
    else: 
        nameofguard = "pohteri"
        nameofsender= "keernesti"
    print(nameofguard)
    yvalue = canvas.coords(name)
    yvalue = yvalue[1]
    boatsent = False
    while(1): 
        if(boatsent):
            break
        sleep(0.4)
        for i in Apinat:
            if(Apinat[i]["state"] == True and Apinat[i]["y_loc"] == yvalue):
                if(Apinat[i]["x_loc"] > 900 and Apinat[i]["x_loc"] < 1099):
                    print(nameofguard, "sees a monkey")
        values = 0
        for i in range(10): 
            if(list[i] != ""):
                values = values +1
            else:
                break
            if(values == 10):
                print("venelahtee")
                animoivene(dict)
                print(nameofsender, " juhlii!")
                th.Thread(target=makeabeep, args=(200,400,)).start()

                boatsent = True
    Eapina = 0
    Kapina = 0
    for a in Apinat:
        if(Apinat[a]["sender"] == "eernesti" and Apinat[a]["state"] == True):
            Eapina = Eapina + 1
        if(Apinat[a]["sender"] == "keernesti" and Apinat[a]["state"] == True):
            Kapina = Kapina + 1 
    print("Keernesti Apinat ", Kapina)
    print("Eernesti Apinat ", Eapina)
    Resepti[1] = {
                "apina": 1,
                "kg perunoita" : 2,
                "dl kuohukermaa" :3,
                "tl mustapippuria":2,
                "tl suolaa" : 1,
            } 
    Resepti[2] = {
                "apina": 1,
                "kg perunoita" : 2,
                "dl kuohukermaa" :3,
                "tl mustapippuria":2,
                "tl suolaa" : 1,
    }
    if(Kapina != 0): 
        for i in range(Kapina-1):
            Resepti[1]["apina"] = Resepti[1]["apina"]+1
            Resepti[1]["kg perunoita"] = Resepti[1]["kg perunoita"]+2
            Resepti[1]["dl kuohukermaa"] = Resepti[1]["dl kuohukermaa"]+3
            Resepti[1]["tl mustapippuria"] = Resepti[1]["tl mustapippuria"]+2
            Resepti[1]["tl suolaa"] = Resepti[1]["tl suolaa"]+2
    if(Eapina != 0): 
        for i in range(Eapina-1):
            Resepti[2]["apina"] = Resepti[2]["apina"]+1
            Resepti[2]["kg perunoita"] = Resepti[2]["kg perunoita"]+2
            Resepti[2]["dl kuohukermaa"] = Resepti[2]["dl kuohukermaa"]+3
            Resepti[2]["tl mustapippuria"] = Resepti[2]["tl mustapippuria"]+2
            Resepti[2]["tl suolaa"] = Resepti[2]["tl suolaa"]+2
    print(" ")
    print("Keernestin soppa")
    print("Apina: " ,Resepti[1]["apina"], " kpl")
    print("Perunaa: ",Resepti[1]["kg perunoita"], " kg")
    print("Kuohukermaa: ", Resepti[1]["dl kuohukermaa"], " dl")
    print("Mustapippuria: ", Resepti[1]["tl mustapippuria"], " tl")
    print("Suolaa: ", Resepti[1]["tl suolaa"], " tl")
    print("Juhlialle: " , Kapina*4)
    print(" ")
    print(" ")
    print("Eernestin soppa")
    print("Apina: " ,Resepti[2]["apina"], " kpl")
    print("Perunaa: ",Resepti[2]["kg perunoita"], " kg")
    print("Kuohukermaa: ", Resepti[2]["dl kuohukermaa"], " dl")
    print("Mustapippuria: ", Resepti[2]["tl mustapippuria"], " tl")
    print("Suolaa: ", Resepti[2]["tl suolaa"], " tl")
    print("Juhlialle: " , Eapina*4)

def sendamonkey(name):
    x = name["x_loc"]+40
    y = name["y_loc"]
    ivalue = 0
    print(x,y)

    apinanumero = len(Apinat)+1

    Apinat[apinanumero] = {
        "message": "",
        "sender": name["name"],
        "state": True,
        "x_loc": x,
        "y_loc": y
    }

    Monkeyname = "Monkey " + str(len(Apinat))

    print(Monkeyname)
    for i in range(len(name["delivered"])):
        if(name["Message"][i] != name["delivered"][i]):
            Apinat[apinanumero]["message"] = name["Message"][i]
            name["delivered"][i] = name["Message"][i]
            ivalue = i
            break

    print(Apinat[apinanumero])
    monkeypointer = canvas.create_image(x,y,image=monkey,tag=Monkeyname)

    for i in range(100): 
        randomvalue = rand.randint(0,200)
        if randomvalue == 100:
            name["delivered"][ivalue] = ""
            Apinat[apinanumero]["state"] = False
            t2 = th.Thread(target=makeabeep, args=(200,200,))
            t2.start()
            t2.join()
            sleep(0.05)
            break
        canvas.move(monkeypointer,10,0)
        Apinat[apinanumero]["x_loc"] = Apinat[apinanumero]["x_loc"] + 10

        if(i==99):
            t3 = th.Thread(target=makeabeep, args=(400,100,))
            t4 =th.Thread(target=makeabeep, args=(200,100,))
            t3.start()
            t4.start()
            t3.join()
            t4.join()
            name["delivered"].append(Apinat[apinanumero]["message"])
            th.Thread(target=messagecheck,args=(apinanumero,ivalue,)).start()
        sleep(0.1)
        th.Thread(target=makeabeep, args=(100,60,)).start()
    canvas.delete(monkeypointer)

def multisender(name): 
    for i in range(10): 
        th.Thread(target=sendamonkey,args=(name,)).start()
        sleep(0.5)

eernestibtn = tk.Button(ikkuna, text="Eernestibutton",width=20,height=5, command= lambda: th.Thread(target=sendamonkey,args=(Eernesti,)).start())

keernestibtn = tk.Button(ikkuna, text="KeernestiButton",width=20,height=5, command= lambda: th.Thread(target=sendamonkey,args=(Keernesti,)).start())
multisenderkern = tk.Button(ikkuna, text="10 Keernesti",width=20,height=5, command= lambda: th.Thread(target=multisender,args=(Keernesti,)).start())
multisenderern = tk.Button(ikkuna, text="10 Eernesti",width=20,height=5, command= lambda: th.Thread(target=multisender,args=(Eernesti,)).start())
th.Thread(target=Guardvision, args=(Eeteripointer,Eteri,Eernesti,)).start()
th.Thread(target=Guardvision, args=(Pohteripointer,Potheri,Keernesti,)).start()
eernestibtn.place(y=200,x=600)
keernestibtn.place(y=200,x=400)
multisenderkern.place(y=300, x=600)
multisenderern.place(y=300, x=400)
ikkuna.mainloop()