import tkinter as tk
from tkinter import messagebox

# --- Creating the main window ---
window = tk.Tk()
window.title("Optimizing Delivery Management")
window.geometry("400x400")

# --- Function to clear the window ---
def clear_window():
    """Removes widgets except the menu."""
    for widget in window.winfo_children():
        if isinstance(widget, tk.Menu):
            continue  # Do not remove the menu bar
        widget.destroy()

# --- Menu functions ---
def window_home(clear=True):
    """Displays only the home page."""
    if clear:
        clear_window()
    tk.Label(window, text="Welcome", font=("Arial", 14)).pack(pady=20)

def window_data_command(clear=True):
    """Displays the order form."""
    if clear:
        clear_window()

    # Adding labels and input fields
    tk.Label(window, text="Customer Name:").pack()
    entry_name = tk.Entry(window)
    entry_name.pack()

    tk.Label(window, text="Delivery Address:").pack()
    entry_address = tk.Entry(window)
    entry_address.pack()

    tk.Label(window, text="Weight (kg):").pack()
    entry_weight = tk.Entry(window)
    entry_weight.pack()

    tk.Label(window, text="Ordered Product:").pack()
    entry_product = tk.Entry(window)
    entry_product.pack()

    tk.Label(window, text="Delivery Date:").pack()
    entry_date = tk.Entry(window)
    entry_date.pack()

    tk.Label(window, text="Payment Method:").pack()
    entry_payment = tk.Entry(window)
    entry_payment.pack()

    # Button to validate the order
    def validate_order():
        """Validates the order and resets the fields."""
        name = entry_name.get()
        address = entry_address.get()
        weight = entry_weight.get()
        product = entry_product.get()
        date = entry_date.get()
        payment = entry_payment.get()

        if name and address and weight and product and date and payment:
            messagebox.showinfo("Order Sent", f"Order for {name} recorded!\n"
                                              f"Address: {address}\n"
                                              f"Weight: {weight} kg\n"
                                              f"Product: {product}\n"
                                              f"Delivery Date: {date}\n"
                                              f"Payment Method: {payment}")

            # Resetting the fields
            entry_name.delete(0, tk.END)
            entry_address.delete(0, tk.END)
            entry_weight.delete(0, tk.END)
            entry_product.delete(0, tk.END)
            entry_date.delete(0, tk.END)
            entry_payment.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Please fill in all the fields.")

    tk.Button(window, text="Send Order", command=validate_order).pack()
    tk.Button(window, text="Back to Home", command=window_home).pack(pady=10)

# --- Creating the menu ---
menu_bar = tk.Menu(window)
menu_file = tk.Menu(menu_bar, tearoff=0)
menu_file.add_command(label="Home page", command=lambda: window_home(True))
menu_file.add_separator()
menu_file.add_command(label="New order", command=lambda: window_data_command(True))
menu_file.add_separator()
menu_file.add_command(label="Exit software", command=window.quit)
menu_bar.add_cascade(label="Management", menu=menu_file)

menu_help = tk.Menu(menu_bar, tearoff=0)
menu_help.add_command(label="About", command=lambda: messagebox.showinfo("About", "2025 Software Engineering - Optimizing Delivery Management"))
menu_bar.add_cascade(label="Help", menu=menu_help)

window.config(menu=menu_bar)

# --- Displaying the home page ---
window_home(clear=False)

# --- Main loop ---
window.mainloop()
