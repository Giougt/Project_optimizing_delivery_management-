import tkinter as tk
from tkinter import messagebox

# --- Fonctions des menus ---
def nouvelle_window():
    messagebox.showinfo("Nouveau", "Nouvelle fenêtre ouverte !")

def exit_app():
    window.quit()

def a_propos():
    messagebox.showinfo("À propos", "App de test Tkinter\nCréée avec ❤️ en Python")

# --- Création de la fenêtre principale ---
window = tk.Tk()
window.title("Optimizing_delivery_management")
window.geometry("400x300")

# --- Création de la barre de menu ---
menu_bar = tk.Menu(window)

# Menu "Fichier"
menu_fichier = tk.Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Nouveau", command=nouvelle_window)
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=exit_app)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

# Menu "Aide"
menu_aide = tk.Menu(menu_bar, tearoff=0)
menu_aide.add_command(label="À propos", command=a_propos)
menu_bar.add_cascade(label="Aide", menu=menu_aide)

# Appliquer le menu à la fenêtre
window.config(menu=menu_bar)

# --- Corps de la fenêtre ---
label = tk.Label(window, text="Welcome", font=("Arial", 14))
label.pack(pady=50)

# --- Boucle principale ---
window.mainloop()
