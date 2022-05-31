### Installation des packages tkinter nécessaires : 
#   sudo apt-get install python3-tk python3-pil python3-pil.imagetk

import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import time


def AdjustWidth(n):
    # Ajuste la largeur de la fenêtre à la taille de l'écran de l'utilisateur
    x = n*root.winfo_screenwidth()/2000
    return round(x)

def AdjustHeight(n):
    # Ajuste la hauteur de la fenêtre à la taille de l'écran de l'utilisateur
    x = n*root.winfo_screenheight()/1080
    return round(x)

def FormularGeometry(l,h,x,y):
    # Ajuste la taille du formulaire
    X = str(AdjustWidth(x))
    Y = str(AdjustHeight(y))
    return str(l)+"x"+str(h)+"+"+X+"+"+Y

def Preparation(inbank):
    # Prépare une liste (tuiles) de 9 paths (9 images prises au hasard dans inbank)
    # Ces 9 paths sont ajoutés deux fois à la liste pour avoir 18 tuiles de jeu
    # La liste est ensuite mélangée
    # Lance à la fin la fonction de jeu Memory
    if os.name == 'posix': # Linux
        paths = [ file.path for file in os.scandir(inbank + "/") ]
    elif os.name == 'nt': # Windows
        paths = [ file.path for file in os.scandir(inbank + "\\") ]
    
    paths_of_tuile = random.sample(paths, 9)
    tuiles = [ ]
    for i in range(9):
        tuiles.append(paths_of_tuile[i])
        tuiles.append(paths_of_tuile[i])
    random.shuffle(tuiles)
    Memory(tuiles,inbank)

def Memory(tuiles,inbank):
    # Création de la fenêtre principale de jeu et initialisation de variables 
    global memory
    global lst_btn
    global lst_btn_clicked
    global n_click
    global lst_new_case
    global n_paire
    global start_time
    global n_bad_answer

    # Initialisation de la fenêtre tkinter
    memory = tk.Toplevel()
    memory.state("normal")
    memory.title("Memory")
    memory.config(bg = color)
    consigne = tk.Label(memory,
                        text = "Retrouvez les paires :",
                        font=("calibri",22),
                        pady=AdjustHeight(10),
                        bg = color)
    consigne.grid(row = 0, column = 0, columnspan = 2, sticky = "w")

    # Configuration de la taille des lignes et des colonnes de la fenêtre
    for i in range(1, 4):
        memory.rowconfigure(i, minsize = AdjustHeight(320))
    for i in range(0, 7):
        memory.columnconfigure(i, minsize = AdjustWidth(320))

    # Initialisation de variables
    start_time = time.time() # Caputurer l'heure au démarrage
    lst_btn = [ ] # Iniatilisation de la liste des boutons (tuiles)
    lst_btn_clicked = [ ] # Initialisation des boutons ayant été cliqués
    lst_new_case = [ ] # Initialisation des listes de label image
    n_click = 0 # Nombre de clics
    n_paire = 0 # Nombre de paires
    n_bad_answer = 0 # Nombre de mauvaises réponses

    # Chaque tuile :
    #   - affiche un point d'interrogation 
    #   - devient un bouton cliquable
    #   - le lien tkinter du bouton est ajouté à la variable lst_btn
    # Au clic se lance la fonction ShowTuile
    for i in range(len(tuiles)):
        img = ImageTk.PhotoImage(Image.open("question.png")) # Récupération de l'image
        btn = tk.Button(memory, # Création des boutons
                        image = img,
                        width = AdjustWidth(300),
                        height = AdjustHeight(300),
                        bg = "white",
                        command = lambda i=i: ShowTuile(tuiles,i,inbank))
        btn.image = img
        btn.grid(row=int(i//6)+1,column=int(i%6),padx=AdjustWidth(5),pady=AdjustHeight(5))
        lst_btn.append(btn)

def ShowTuile(tuiles,i,inbank):
    # Montre les tuiles au clic
    global memory
    global n_click
    global lst_btn
    global lst_btn_clicked
    global lst_new_case


    lst_btn_clicked.append(i) # La tuile i a été cliquée

    # Affichage de la tuile : 
    #   - le texte correspond au nom du fichier moins l'extension
    #   - l'image correspond au path (tuiles) de l'élément i
    #   - l'image est affichée dans un label tkinter
    txt = tuiles[i]
    if os.name == 'posix': # Linux
        txt = txt.split("/")[-1]
    elif os.name == 'nt': # Windows
        txt = txt.split("\\")[-1]
    txt = txt.split(".")[0]
    txt = txt.capitalize()
    txt = txt + "\n"
    img = ImageTk.PhotoImage(Image.open(tuiles[i]))
    new_case = tk.Label(memory,
                        text= txt,
                        image = img,
                        compound="bottom",
                        font = ("calibri",22),
                        width = AdjustWidth(300),
                        height = AdjustHeight(300),
                        bg="white")
    new_case.image=img
    new_case.grid(row=int(i//6)+1,column=int(i%6),padx=AdjustWidth(5),pady=AdjustHeight(5))
    lst_new_case.append(new_case)
    
    # Vérification du nombre de tuiles cliquée
    n_click+=1
    if n_click == 2:
        n_click = 0
        memory.update()
        time.sleep(1) 
        CheckAnswer(tuiles,inbank) # Vérification de la réponse avec la fonction CheckAnswer
        lst_btn_clicked = [ ] # Réinitialisation de la liste des boutons cliqués
    
def CheckAnswer(tuiles,inbank):
    # Vérifie si la réponse est correcte (si les deux tuiles sont identiques)
    global lst_new_case
    global lst_btn
    global n_paire
    global memory
    global start_time
    global n_bad_answer

    # Comparaison des deux paths et destruction des boutons si vraie
    if tuiles[lst_btn_clicked[0]] == tuiles[lst_btn_clicked[1]]: 
        lst_btn[lst_btn_clicked[0]].destroy()
        lst_btn[lst_btn_clicked[1]].destroy()
        lst_new_case[-2].destroy()
        lst_new_case[-1].destroy()
        n_paire +=1 # Une paire a été trouvée
        if n_paire == 9: # Toutes les paires ont été trouvées
            end_time = time.time() # Récupération de l'heure à la fin du jeu
            # Affichage des données de fin de jeu
            tk.Label(memory,
                     text="Temps : ",
                     font = ("calibri",22),
                     bg = color
                     ).grid(row=1,column=2,sticky="nw")

            tk.Label(memory,
                     text= str(round(end_time - start_time)) + " s",
                     font = ("calibri",22),
                     bg = color
                     ).grid(row=1,column=3,sticky="nw")

            tk.Label(memory,
                     text= "Mauvaises paires : ",
                     font = ("calibri",22),
                     bg = color
                     ).grid(row=1,column=2,sticky="w")

            tk.Label(memory,
                     text= str(n_bad_answer),
                     font = ("calibri",22),
                     bg = color
                     ).grid(row=1,column=3,sticky="w")

            tk.Label(memory,
                     text= "Refaire une partie ? ",
                     font = ("calibri",22),
                     bg = color
                     ).grid(row=1,column=2,sticky="sw")

            tk.Button(memory,
                      text= "Oui",
                      font = ("calibri",22),
                      bg = color,
                      width=AdjustWidth(8),
                      command = lambda inbank=inbank: NewGame(inbank) # Relance la fonction NewGame
                      ).grid(row=1,column=3,sticky="sw")
            
            tk.Button(memory,
                      text = "Non",
                      font = ("calibri",22),
                      bg = color,
                      width=AdjustWidth(8),
                      command = EndProgram # Lance la fonction EndProgram
                      ).grid(row=1,column=3,sticky="se")
    else: # Si les paths ne sont pas identiques recommencer un nouvel essai et ajout d'une mauvaise réponse
        lst_new_case[-2].destroy()
        lst_new_case[-1].destroy()
        n_bad_answer += 1

def NewGame(inbank):
    # Création d'un nouveau jeu
    memory.destroy()
    Preparation(inbank)
    
def EndProgram():
    # Destruction de toutes les fenêtres tkinter
    global root
    global memory
    memory.destroy()
    root.destroy()   

def AllScript():
    # Définition de la fenêtre root de tkinter et initialisation 
    global root
    global color
    global color_btn

    color = "antique white"
    color_btn = "floral white"

    # Récupération des dossier présents dans "banque"
    if os.name == 'posix': # Linux
        inbanks = [ folder.path for folder in os.scandir("banque/") if folder.is_dir() ]
    elif os.name == 'nt': # Windows
        inbanks = [ folder.path for folder in os.scandir("banque\\") if folder.is_dir() ]  
    
    #Initialisation de la fenêtre formulaire
    root = tk.Tk()
    root.title("Formulaire")
    root.geometry(FormularGeometry(450,320,700,200))
    root.config(bg = color)

    tk.Label(root,
         text = "Bienvenue sur le Mémory.\nChoisir un thème :",
         font = ("calibri",22),
         padx = AdjustWidth(20),
         pady = AdjustHeight(50),
         bg = color
         ).grid(row=0,columnspan=2)
    
    n=0
    for inbank in inbanks: # Affiche autant de boutons nommés que de dossiers présents dans banque
        txt = ''
        if os.name == 'posix':
            txt = inbank.split("/")[-1]
        elif os.name == 'nt':
            txt = inbank.split("\\")[-1]

        tk.Button(root,
                  text = txt,
                  width = 20,
                  bg = color_btn,
                  command = lambda inbank=inbank: Preparation(inbank) # Lance la fonction Preparation
                  ).grid(row=int(n/2)+1,column=int(n%2),padx=15,pady=15)
        n+=1
    root.mainloop()


if __name__ == '__main__':
    AllScript()
