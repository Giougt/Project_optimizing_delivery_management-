#import file 
from data.db import get_connection


import assets.styles.style   # Import du fichier style.py

#import module
import tkinter as tk
from tkinter import messagebox, ttk


# --- Creating the main window ---
window = tk.Tk()
window.title("Optimizing Delivery Management")
window.geometry("700x700")
window.configure(bg=assets.styles.style.bg_color)

# --- Database connection ---
conn = get_connection()
cursor = conn.cursor()

# --- Function to clear the window ---
def clear_window():
    for widget in window.winfo_children():
        if isinstance(widget, tk.Menu):
            continue
        widget.destroy()

# --- Menu functions ---
def window_home(clear=True):
    if clear:
        clear_window()
    tk.Label(window, text="Welcome", font=assets.styles.style.font_title, bg=assets.styles.style.bg_color, fg=assets.styles.style.label_color).pack(pady=assets.styles.style.padding_y)

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
              command=window_home).pack(pady=assets.styles.style.padding_y)

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
              command=window_home).pack(pady=assets.styles.style.padding_y)

# --- Creating the menu ---
menu_bar = tk.Menu(window)
menu_file = tk.Menu(menu_bar, tearoff=0)
menu_file.add_command(label="Home", command=lambda: window_home(True))
menu_file.add_separator()
menu_file.add_command(label="New Order", command=lambda: window_data_command(True))
menu_file.add_separator()
menu_file.add_command(label="View Orders", command=lambda: window_view_orders(True))
menu_file.add_separator()
menu_file.add_command(label="Exit", command=window.quit)
menu_bar.add_cascade(label="Management", menu=menu_file)

menu_help = tk.Menu(menu_bar, tearoff=0)
menu_help.add_command(label="About", command=lambda: messagebox.showinfo("About", "2025 Software Engineering - Optimizing Delivery Management"))
menu_bar.add_cascade(label="Help", menu=menu_help)

window.config(menu=menu_bar)

# --- Displaying the home page ---
window_home(clear=False)

# --- Main loop ---
window.mainloop()
