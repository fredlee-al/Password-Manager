import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet
import os

# Generate and load key functions
def generate_key():
    return Fernet.generate_key()

def load_key():
    if not os.path.exists("secret.key"):
        key = generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    return open("secret.key", "rb").read()

# Encrypt and decrypt functions
def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

# Main application class
class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deezmanager - Password Manager")

        self.key = load_key()
        self.password_db = {}

        self.create_widgets()

    def create_widgets(self):
        self.add_button = tk.Button(self.root, text="Add Password", command=self.add_password)
        self.add_button.pack(pady=10)

        self.retrieve_button = tk.Button(self.root, text="Retrieve Password", command=self.retrieve_password)
        self.retrieve_button.pack(pady=10)

        self.show_button = tk.Button(self.root, text="Show All Passwords", command=self.show_passwords)
        self.show_button.pack(pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=10)

    def add_password(self):
        site = simpledialog.askstring("Input", "Enter the site name:")
        username = simpledialog.askstring("Input", "Enter the username:")
        password = simpledialog.askstring("Input", "Enter the password:")

        if site and username and password:
            encrypted_password = encrypt_message(password, self.key)
            self.password_db[site] = {'username': username, 'password': encrypted_password}
            messagebox.showinfo("Success", f"Password for {site} added successfully!")

    def retrieve_password(self):
        site = simpledialog.askstring("Input", "Enter the site name:")

        if site in self.password_db:
            username = self.password_db[site]['username']
            encrypted_password = self.password_db[site]['password']
            password = decrypt_message(encrypted_password, self.key)
            messagebox.showinfo("Password", f"Username: {username}\nPassword: {password}")
        else:
            messagebox.showerror("Error", "Site not found!")

    def show_passwords(self):
        if not self.password_db:
            messagebox.showinfo("Info", "No passwords stored.")
            return

        display_text = ""
        for site, creds in self.password_db.items():
            username = creds['username']
            password = decrypt_message(creds['password'], self.key)
            display_text += f"Site: {site}\nUsername: {username}\nPassword: {password}\n\n"

        messagebox.showinfo("All Passwords", display_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
