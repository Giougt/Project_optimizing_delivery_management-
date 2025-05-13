#import file 
from data.db import get_connection


import assets.styles.style   # Import du fichier style.py

#import module
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# --- Creating the main window ---
window = tk.Tk()
window.title("Optimizing Delivery Management")
window.geometry("700x700")
window.configure(bg=assets.styles.style.bg_color)

# --- Database connection ---
conn = get_connection()
cursor = conn.cursor()

# for connection state 
connected = False

# --- Function to clear the window ---
def clear_window():
    for widget in window.winfo_children():
        if isinstance(widget, tk.Menu):
            continue
        widget.destroy()

# hide menu if disconnect 
def update_menu_visibility():
    if connected:
        window.config(menu=menu_bar)
    else:
        window.config(menu="")  # Cache le menu

# --- Menu functions ---
def login_page(clear=True):
    global connected
    if clear:
        clear_window()

    update_menu_visibility()

    tk.Label(
        window,
        text="Login",
        font=assets.styles.style.font_title,
        bg=assets.styles.style.bg_color,
        fg=assets.styles.style.label_color
    ).pack(pady=assets.styles.style.padding_y)

    tk.Label(window, text="Nom d'utilisateur :", font=assets.styles.style.font_label,
             bg=assets.styles.style.bg_color, fg=assets.styles.style.label_color).pack()
    username_entry = tk.Entry(window, font=assets.styles.style.font_label)
    username_entry.pack()

    tk.Label(window, text="Mot de passe :", font=assets.styles.style.font_label,
             bg=assets.styles.style.bg_color, fg=assets.styles.style.label_color).pack()
    password_entry = tk.Entry(window, font=assets.styles.style.font_label, show="*")
    password_entry.pack()

    def try_login():
        global connected
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showwarning("Error", "Please fill in all fields")
            return

        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
            if user:
                connected = True
                update_menu_visibility()
                messagebox.showinfo("Sucess connexion", f"Welcome, {username} !")
                window_home_page(True)
            else:
                messagebox.showerror("Connexion Denied", "Username or password incorrect.")
        except Exception as e:
            messagebox.showerror("Error database", str(e))

    tk.Button(
        window,
        text="Login",
        font=assets.styles.style.font_button,
        bg=assets.styles.style.button_color,
        fg=assets.styles.style.button_text_color,
        command=try_login
    ).pack(pady=10)

# logout function
def logout():
    global connected
    connected = False
    update_menu_visibility()
    login_page(True)  # Redirection home page 

# command function
def window_data_command(clear=True):
    if clear:
        clear_window()

    labels = ["Customer Name", "Delivery Address", "Start Address", "Weight (kg)", "Ordered Product", "Delivery Date", "Payment Method", "Price"]
    entries = {}

    for label in labels:
        tk.Label(window, text=label + ":", font=assets.styles.style.font_label, bg=assets.styles.style.bg_color, fg=assets.styles.style.label_color).pack(pady=(assets.styles.style.padding_y // 2))
        entry = tk.Entry(window)
        entry.pack(padx=assets.styles.style.padding_x, pady=(0, assets.styles.style.padding_y))
        entries[label] = entry

    def validate_order():
        data = {label: entry.get() for label, entry in entries.items()}
        if all(data.values()):
            try:
                cursor.execute(
                    """
                    INSERT INTO orders (customer_name, delivery_address, start_address, weight, product, delivery_date, payment_method, price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (data["Customer Name"], data["Delivery Address"], data["Start Address"],
                     data["Weight (kg)"], data["Ordered Product"], data["Delivery Date"],
                     data["Payment Method"], data["Price"])
                )
                conn.commit()
                messagebox.showinfo("Order Sent", f"Order for {data['Customer Name']} recorded!")
                for entry in entries.values():
                    entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Error", "Please fill in all the fields.")

    tk.Button(window, text="Send Order", font=assets.styles.style.font_button, bg=assets.styles.style.button_color, fg=assets.styles.style.button_text_color, command=validate_order).pack(pady=assets.styles.style.padding_y)
    tk.Button(window, text="Visualize Route", font=assets.styles.style.font_button, bg=assets.styles.style.button_color, fg=assets.styles.style.button_text_color,
              command=lambda: messagebox.showinfo("Route", "Feature coming soon!")).pack(pady=assets.styles.style.padding_y)
    tk.Button(window, text="Back to Home", font=assets.styles.style.font_button, bg=assets.styles.style.button_color, fg=assets.styles.style.button_text_color,
              command=window_home_page).pack(pady=assets.styles.style.padding_y)

def window_view_orders(clear=True):
    if clear:
        clear_window()

    tk.Label(window, text="All Orders", font=assets.styles.style.font_title, bg=assets.styles.style.bg_color, fg=assets.styles.style.label_color).pack(pady=assets.styles.style.padding_y)

    tree = ttk.Treeview(window, columns=("ID", "Name", "Delivery Address", "Start Address", "Weight", "Product", "Date", "Payment", "Price"), show='headings')
    
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(expand=True, fill='both', padx=assets.styles.style.padding_x, pady=assets.styles.style.padding_y)

    try:
        cursor.execute("SELECT id, customer_name, delivery_address, start_address, weight, product, delivery_date, payment_method, price FROM orders")
        orders = cursor.fetchall()
        for order in orders:
            tree.insert("", tk.END, values=order)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

    tk.Button(window, text="Back to Home", font=assets.styles.style.font_button, bg=assets.styles.style.button_color, fg=assets.styles.style.button_text_color,
              command=window_home_page).pack(pady=assets.styles.style.padding_y)


def load_local_image(path, size=(150, 150)):
    try:
        im = Image.open(path)
        im = im.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(im)
    except Exception as e:
        print(f"Erreur chargement image: {e}")
        return None

def window_home_page(clear=True):
    if clear:
        clear_window()

    window.configure(bg=assets.styles.style.bg_color)

    # === Scrollable frame setup ===
    canvas = tk.Canvas(window, bg=assets.styles.style.bg_color, highlightthickness=0)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=assets.styles.style.bg_color)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === Content inside scrollable frame ===
    tk.Label(
        scroll_frame,
        text="Welcome to the Delivery Management Optimization App",
        font=assets.styles.style.font_title,
        bg=assets.styles.style.bg_color,
        fg=assets.styles.style.label_color
    ).pack(pady=30)

    def add_section(image_path, description, button_text, command):
        img = load_local_image(image_path)
        if img:
            lbl = tk.Label(scroll_frame, image=img, bg=assets.styles.style.bg_color)
            lbl.image = img  # Prevent garbage collection
            lbl.pack(pady=5)

        tk.Label(
            scroll_frame,
            text=description,
            font=assets.styles.style.font_label,
            bg=assets.styles.style.bg_color,
            fg=assets.styles.style.label_color,
            wraplength=400,
            justify="center"
        ).pack(pady=5)

        tk.Button(
            scroll_frame,
            text=button_text,
            font=assets.styles.style.font_button,
            bg=assets.styles.style.button_color,
            fg=assets.styles.style.button_text_color,
            command=command
        ).pack(pady=10)

    add_section("images/two_packs.png", "Create a new delivery order quickly and easily.", "New Order", window_data_command)
    add_section("images/two_packs.png", "View your existing orders and track deliveries.", "View Orders", window_view_orders)
    add_section("images/two_packs.png", "Log out securely from the application.", "Logout", logout)


# --- Creating the menu ---
menu_bar = tk.Menu(window)
menu_file = tk.Menu(menu_bar, tearoff=0)
menu_file.add_command(label="New Order", command=lambda: window_data_command(True))
menu_file.add_separator()
menu_file.add_command(label="View Orders", command=lambda: window_view_orders(True))
menu_file.add_separator()
menu_file.add_command(label="Logout", command=logout)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=window.quit)
menu_bar.add_cascade(label="Management", menu=menu_file)

menu_help = tk.Menu(menu_bar, tearoff=0)
menu_help.add_command(label="About", command=lambda: messagebox.showinfo("About", "2025 Software Engineering - Optimizing Delivery Management"))
menu_bar.add_cascade(label="Help", menu=menu_help)

window.config(menu=menu_bar)

# --- Displaying the home page ---
login_page(clear=False)

# --- Main loop ---
window.mainloop()
