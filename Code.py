import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import re
import random

class CustomerService:
    def __init__(self, db_name="customer_database.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            email TEXT,
                            phone TEXT)''')
        self.conn.commit()

    def add_customer(self, name, email, phone):
        if not self.validate_email(email):
            return "Invalid email format."
        if not self.validate_phone(phone):
            return "Invalid phone format."
        self.cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
        self.conn.commit()
        return f"Customer {name} added successfully."

    def remove_customer(self, customer_id):
        self.cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
        self.conn.commit()
        return "Customer removed successfully." if self.cursor.rowcount > 0 else "Customer not found."

    def display_customer_info(self, customer_id):
        self.cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
        customer = self.cursor.fetchone()
        if customer:
            return f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}"
        else:
            return "Customer not found."

    def validate_email(self, email):
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

    def validate_phone(self, phone):
        return bool(re.match(r"^\d{3}-\d{3}-\d{4}$", phone))

    def __del__(self):
        self.conn.close()

def add_customer_dialog():
    name = simpledialog.askstring("Input", "Enter customer name:")
    email = simpledialog.askstring("Input", "Enter customer email:")
    phone = simpledialog.askstring("Input", "Enter customer phone (format: xxx-xxx-xxxx):")
    result = service.add_customer(name, email, phone)
    messagebox.showinfo("Result", result)

def remove_customer_dialog():
    customer_id = simpledialog.askstring("Input", "Enter customer ID to remove:")
    result = service.remove_customer(customer_id)
    messagebox.showinfo("Result", result)

def display_customer_info_dialog():
    customer_id = simpledialog.askstring("Input", "Enter customer ID to display info:")
    result = service.display_customer_info(customer_id)
    messagebox.showinfo("Customer Info", result)

def random_color():
    return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'

def on_enter(e):
    e.widget['background'] = random_color()

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

service = CustomerService()

root = tk.Tk()
root.title("Customer Service System")
root.config(bg='black')
root.state('zoomed')  # Maximize the window to fit the screen size

button_properties = {'padx': 20, 'pady': 10, 'bd': 4}
buttons = [
    tk.Button(root, text="Add Customer", command=add_customer_dialog, **button_properties),
    tk.Button(root, text="Remove Customer", command=remove_customer_dialog, **button_properties),
    tk.Button(root, text="Display Customer Info", command=display_customer_info_dialog, **button_properties),
    tk.Button(root, text="Exit", command=root.destroy, **button_properties)
]

for button in buttons:
    button.pack(fill=tk.X, padx=80, pady=15)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

root.mainloop()
