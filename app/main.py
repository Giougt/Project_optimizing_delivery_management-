import tkinter as tk
from tkinter import messagebox

# --- Création de la fenêtre principale ---
window = tk.Tk()
window.title("Optimizing Delivery Management")
window.geometry("400x300")

# --- Création d'un Label global ---
label = tk.Label(window, text="Welcome", font=("Arial", 14))
label.pack(pady=20)  # Affichage du label dans la fenêtre

# --- Fonctions des menus ---
def window_home():
    """ Crée et affiche uniquement les éléments de la fenêtre 'home' """
    label.config(text="Welcome")  # Modification du label

def window_data_command():
    """ Affiche la page de commande """
    label.config(text="Page 1 - Accueil")  # Modification du texte du label

def exit_app():
    """ Quitte l'application """
    window.quit()

def a_propos():
    """ Affiche une boîte de dialogue avec les infos de l'application """
    messagebox.showinfo("À propos", "2025 Software Engineering - Optimizing Delivery Management")

# --- Création de la barre de menu ---
menu_bar = tk.Menu(window)

# Menu "Management"
menu_fichier = tk.Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Home page", command=window_home)
menu_fichier.add_separator()
menu_fichier.add_command(label="New command", command=window_data_command)
menu_bar.add_cascade(label="Management", menu=menu_fichier)
menu_fichier.add_separator()
menu_fichier.add_command(label="Exit software", command=exit_app)

# Menu "Aide"
menu_aide = tk.Menu(menu_bar, tearoff=0)
menu_aide.add_command(label="À propos", command=a_propos)
menu_bar.add_cascade(label="Aide", menu=menu_aide)

# Appliquer le menu à la fenêtre
window.config(menu=menu_bar)


# --- Boucle principale ---
window.mainloop()
