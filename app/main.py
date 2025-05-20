#import file 
from data.db import get_connection

import assets.styles.style  

#import module
import tkinter as tk
from tkinter import messagebox, ttk

import webbrowser
import urllib.parse
from pathlib import Path
import urllib.parse
import pyautogui
import time

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
        window.config(menu="") 

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

    tk.Label(window, text="Username :", font=assets.styles.style.font_label,
             bg=assets.styles.style.bg_color, fg=assets.styles.style.label_color).pack()
    username_entry = tk.Entry(window, font=assets.styles.style.font_label)
    username_entry.pack()

    tk.Label(window, text="Password :", font=assets.styles.style.font_label,
             bg=assets.styles.style.bg_color, fg=assets.styles.style.label_color).pack()
    password_entry = tk.Entry(window, font=assets.styles.style.font_label, show="*")
    password_entry.pack()

    # send data user authentification
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

    def create_account(clear=True):
        if clear:
            clear_window()
            labels = ["name","lastname","email","country","age","password","confirm password","username"]
            entries = {}

            for label in labels:
                tk.Label(window, text=label + ":", font=assets.styles.style.font_label, bg=assets.styles.style.bg_color, fg=assets.styles.style.label_color).pack(pady=(assets.styles.style.padding_y // 2))
                entry = tk.Entry(window)
                entry.pack(padx=assets.styles.style.padding_x, pady=(0, assets.styles.style.padding_y))
                entries[label] = entry

            # function stock data user in MySql
            def send_data_user():
                data = {label: entry.get() for label, entry in entries.items()}
                if all(data.values()):
                    try:
                        cursor.execute(
                            """
                            INSERT INTO users_data (name,lastname,email,country,age)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (int(data["age"]), data["lastname"], data["email"],
                            data["country"], data["age"])
                        )
                        conn.commit()
                        for entry in entries.values():
                            entry.delete(0, tk.END)
                        cursor.execute(
                            """
                            INSERT INTO users (username,password)
                            VALUES (%s,%s)
                            """,
                            (data["username"], data["password"])
                        )
                        conn.commit()
                        messagebox.showinfo("Data user send sucessfuly ")
                        for entry in entries.values():
                            entry.delete(0, tk.END)
                    except Exception as e:
                        messagebox.showerror("Database Error", str(e))
                else:
                    messagebox.showwarning("Error", "Please fill in all the fields.")

            tk.Button(
                window,
                text="Send",
                font=assets.styles.style.font_button,
                bg=assets.styles.style.button_color,
                fg=assets.styles.style.button_text_color,
                command=send_data_user
            ).pack(pady=10)

            tk.Button(
                window,
                text="Back login",
                font=assets.styles.style.font_button,
                bg=assets.styles.style.button_color,
                fg=assets.styles.style.button_text_color,
                command=login_page
            ).pack(pady=10)


    tk.Button(
        window,
        text="Login",
        font=assets.styles.style.font_button,
        bg=assets.styles.style.button_color,
        fg=assets.styles.style.button_text_color,
        command=try_login
    ).pack(pady=10)

    tk.Button(
        window,
        text="Create an account",
        font=assets.styles.style.font_button,
        bg=assets.styles.style.button_color,
        fg=assets.styles.style.button_text_color,
        command=create_account
    ).pack(pady=10)

# for route visualize 
def open_latest_route_in_maps():
    try:
        cursor.execute(
            """
            SELECT start_address, delivery_address 
            FROM orders 
            ORDER BY id DESC 
            LIMIT 1
            """
        )
        result = cursor.fetchone()
        if result:
            start_address, delivery_address = result
            start_encoded = urllib.parse.quote_plus(start_address)
            end_encoded = urllib.parse.quote_plus(delivery_address)
            url = f"https://www.google.com/maps/dir/{start_encoded}/{end_encoded}"
            webbrowser.open(url)

            # Attendre que la carte s'affiche correctement
            time.sleep(8)

            # Créer dossier s'il n'existe pas
            images_path = Path("images")
            images_path.mkdir(exist_ok=True)

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            file_path = images_path / f"route_{timestamp}.png"
            pyautogui.screenshot().save(file_path)

            messagebox.showinfo("Screenshot Saved", f"Map screenshot saved as {file_path}")
        else:
            messagebox.showinfo("No Orders", "No orders found in the database.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open route or save screenshot:\n{e}")

# logout function
def logout():
    global connected
    connected = False
    update_menu_visibility()
    login_page(True)  # redirect home page

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
              command=open_latest_route_in_maps).pack(pady=assets.styles.style.padding_y)
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



def window_home_page(clear=True):
    if clear:
        clear_window()

    window.configure(bg=assets.styles.style.bg_color)

    # === Scrollable frame setup ===
    canvas = tk.Canvas(window, bg=assets.styles.style.bg_color, highlightthickness=0)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    outer_frame = tk.Frame(canvas, bg=assets.styles.style.bg_color)
    canvas.create_window((0, 0), window=outer_frame, anchor="n", width=window.winfo_width())

    outer_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === Title ===
    tk.Label(
        outer_frame,
        text="Welcome to the Delivery Management Optimization App",
        font=assets.styles.style.font_title,
        bg=assets.styles.style.bg_color,
        fg=assets.styles.style.label_color,
        wraplength=600,
        justify="center"
    ).pack(pady=(40, 30))

    def add_section(description, button_text, command):
        section = tk.Frame(outer_frame, bg=assets.styles.style.bg_color)
        section.pack(pady=20)

        tk.Label(
            section,
            text=description,
            font=assets.styles.style.font_label,
            bg=assets.styles.style.bg_color,
            fg=assets.styles.style.label_color,
            wraplength=500,
            justify="center"
        ).pack(pady=8)

        tk.Button(
            section,
            text=button_text,
            font=assets.styles.style.font_button,
            bg=assets.styles.style.button_color,
            fg=assets.styles.style.button_text_color,
            command=command,
            padx=20,
            pady=6
        ).pack(pady=10)

    # === Add sections (no images) ===
    add_section("Create a new delivery order quickly and easily.", "New Order", window_data_command)
    add_section("View your existing orders and track deliveries.", "View Orders", window_view_orders)
    add_section("Log out securely from the application.", "Logout", logout)

        
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
