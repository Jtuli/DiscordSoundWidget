# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pygetwindow as gw
from ctypes.wintypes import DOUBLE


#Récupérer le volume de discord
def get_discord_volume():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "Discord.exe":
            return volume.GetMasterVolume()


#Actualiser l'affichage du volume en %
def update_volume_label(): 
    volume = get_discord_volume()
    if volume is not None:
        volume_label.config(text=f"Volume Discord: {int(volume * 100)}%")
    else:
        volume_label.config(text="Discord non trouvé")

    root.after(1000, update_volume_label)

#Modifier le volume de discord
def update_volume(value):
    valeur = float(value)/ 100.0
    
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "Discord.exe":
            print(f"Volume mis à jour : {valeur}%")
            volume.SetMasterVolume(valeur, None)
            return volume.GetMasterVolume()
        

#Fermer la fenêtre grâce à un autre bouton
def on_close():
    
    root.destroy()
    
# Crée la fenêtre principale
root = tk.Tk()
root.title("Discord Volume Widget")
root.geometry('150x300')
root.resizable(False, False)

# Supprimer le bouton de fermeture
root.overrideredirect(True)

# Ajouter un événement pour gérer la fermeture de la fenêtre
root.protocol("WM_DELETE_WINDOW", on_close)

# Créer un bouton de fermeture personnalisé
button_close = tk.Button(root, text="Fermer", command=on_close)
button_close.pack(pady=10)

# Crée une étiquette pour afficher le volume
volume_label = tk.Label(root, text="Volume Discord: " )
volume_label.pack(padx=10, pady=10)

# Utilise une variable Tkinter pour stocker la valeur du volume
volume_slider = ttk.Scale(root, from_=0, to=100, orient="vertical", command=lambda value: update_volume(value))
volume_slider.set(get_discord_volume()*100)  # Définir la valeur initiale du volume à celui de discord
volume_slider.pack(padx=10, pady=10)

# Lance la mise à jour du volume
update_volume_label()

# Permettre de déplacer la fenêtre
root.bind("<ButtonPress-1>", root.start_move)
root.bind("<ButtonRelease-1>", root.stop_move)
root.bind("<B1-Motion>", root.on_motion)

def start_move(root, event):
    root.x = event.x
    root.y = event.y

def stop_move(self, event):
    root.x = None
    root.y = None

def on_motion(root, event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")


# Démarre la boucle principale de l'interface graphique
root.mainloop()
