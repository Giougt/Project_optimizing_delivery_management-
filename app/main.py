import tkinter as tk
from tkinter import messagebox

# --- Création de la fenêtre principale ---
window = tk.Tk()
window.title("Optimizing Delivery Management")
window.geometry("400x400")

# --- Fonction pour nettoyer la fenêtre ---
def clear_window():
    """Supprime les widgets sauf le menu."""
    for widget in window.winfo_children():
        if isinstance(widget, tk.Menu):
            continue  # Ne supprime pas la barre de menu
        widget.destroy()

# --- Fonctions des menus ---
def window_home(clear=True):
    """Affiche uniquement la page d'accueil."""
    if clear:
        clear_window()
    tk.Label(window, text="Welcome", font=("Arial", 14)).pack(pady=20)

def window_data_command(clear=True):
    """Affiche le formulaire de commande."""
    if clear:
        clear_window()

    # Ajout des labels et champs de saisie
    tk.Label(window, text="Nom du Client:").pack()
    entry_nom = tk.Entry(window)
    entry_nom.pack()

    tk.Label(window, text="Adresse de Livraison:").pack()
    entry_adresse = tk.Entry(window)
    entry_adresse.pack()

    tk.Label(window, text="Poids (kg):").pack()
    entry_poids = tk.Entry(window)
    entry_poids.pack()

    tk.Label(window, text="Produit Commandé:").pack()
    entry_produit = tk.Entry(window)
    entry_produit.pack()

    tk.Label(window, text="Date de Livraison:").pack()
    entry_date = tk.Entry(window)
    entry_date.pack()

    tk.Label(window, text="Mode de Paiement:").pack()
    entry_paiement = tk.Entry(window)
    entry_paiement.pack()

    # Bouton pour valider la commande
    def valider_commande():
        """Valide la commande et réinitialise les champs."""
        nom = entry_nom.get()
        adresse = entry_adresse.get()
        poids = entry_poids.get()
        produit = entry_produit.get()
        date = entry_date.get()
        paiement = entry_paiement.get()

        if nom and adresse and poids and produit and date and paiement:
            messagebox.showinfo("Commande envoyée", f"Commande de {nom} enregistrée !\n"
                                                    f"Adresse: {adresse}\n"
                                                    f"Poids: {poids} kg\n"
                                                    f"Produit: {produit}\n"
                                                    f"Date de Livraison: {date}\n"
                                                    f"Mode de Paiement: {paiement}")

            # Réinitialisation des champs
            entry_nom.delete(0, tk.END)
            entry_adresse.delete(0, tk.END)
            entry_poids.delete(0, tk.END)
            entry_produit.delete(0, tk.END)
            entry_date.delete(0, tk.END)
            entry_paiement.delete(0, tk.END)
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

    tk.Button(window, text="Envoyer Commande", command=valider_commande).pack()
    tk.Button(window, text="Retour à l'accueil", command=window_home).pack(pady=10)

# --- Création du menu ---
menu_bar = tk.Menu(window)
menu_fichier = tk.Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Home page", command=lambda: window_home(True))
menu_fichier.add_separator()
menu_fichier.add_command(label="New command", command=lambda: window_data_command(True))
menu_fichier.add_separator()
menu_fichier.add_command(label="Exit software", command=window.quit)
menu_bar.add_cascade(label="Management", menu=menu_fichier)

menu_aide = tk.Menu(menu_bar, tearoff=0)
menu_aide.add_command(label="À propos", command=lambda: messagebox.showinfo("À propos", "2025 Software Engineering - Optimizing Delivery Management"))
menu_bar.add_cascade(label="Aide", menu=menu_aide)

window.config(menu=menu_bar)

# --- Affichage de la page d'accueil ---
window_home(clear=False)

# --- Boucle principale ---
window.mainloop()
