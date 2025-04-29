# ui/login_page.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sqlite3
from database import db_helper as db
from utils import theme_manager as tm
from utils.ui_helpers import create_entry, create_button
from ui import settings_page

def login():
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (entered_username, entered_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("✅ Login Successful", f"Welcome, {entered_username}!")
        settings_page.set_username(entered_username)
        root.destroy()
        import ui.dashboard_page as dashboard
        dashboard.open_dashboard()
    else:
        messagebox.showerror("❌ Login Failed", "Invalid Username or Password.")

def open_login():
    global root, username_entry, password_entry

    root = tk.Tk()
    root.title("ClubConnect Login 🚀")
    root.geometry("500x700")
    root.config(bg=tm.get_theme()["bg"])
    root.resizable(False, False)

    def switch_theme():
        tm.toggle_theme()
        root.destroy()
        open_login()

    theme_btn = create_button(root, "Toggle Dark/Light Mode 🌗", switch_theme, font_size=10, width=20)
    theme_btn.pack(pady=10, anchor="ne", padx=10)

    # ====== Logo Area ======
    logo_path = os.path.join('assets', 'logos', 'clubconnect_logo.png')
    if os.path.exists(logo_path):
        img = Image.open(logo_path)
        img = img.resize((150, 150))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo, bg=tm.get_theme()["bg"])
        logo_label.image = logo
        logo_label.pack(pady=20)
    else:
        logo_label = tk.Label(root, text="ClubConnect", font=("Helvetica", 24, "bold"),
                              bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"])
        logo_label.pack(pady=40)

    title = tk.Label(root, text="🔑 Login to ClubConnect", font=("Helvetica", 20, "bold"),
                     bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"])
    title.pack(pady=10)

    username_label = tk.Label(root, text="👤 Username", font=("Helvetica", 14),
                              bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"])
    username_label.pack(pady=(30, 5))
    username_entry = create_entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="🔒 Password", font=("Helvetica", 14),
                              bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"])
    password_label.pack(pady=(20, 5))
    password_entry = create_entry(root)
    password_entry.config(show="*")
    password_entry.pack()

    login_btn = create_button(root, "Login ✅", login)
    login_btn.pack(pady=20)

    create_user_btn = create_button(root, "➕ Create New User", create_new_user)
    create_user_btn.pack(pady=5)

    forgot_btn = create_button(root, "🔄 Forgot Password?", forgot_password)
    forgot_btn.pack(pady=5)

    settings_btn = create_button(root, "⚙️ Open Settings", lambda: settings_page.open_settings(root))
    settings_btn.pack(pady=5)

    root.mainloop()

def create_new_user():
    new_user_window = tk.Toplevel()
    new_user_window.title("Create New User 🚀")
    new_user_window.geometry("400x400")
    new_user_window.config(bg=tm.get_theme()["bg"])

    tk.Label(new_user_window, text="➕ Create New User", font=("Helvetica", 18, "bold"),
             bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"]).pack(pady=20)

    tk.Label(new_user_window, text="👤 Username", font=("Helvetica", 14),
             bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"]).pack(pady=(10, 5))
    new_username = create_entry(new_user_window)
    new_username.pack()

    tk.Label(new_user_window, text="🔒 Password", font=("Helvetica", 14),
             bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"]).pack(pady=(10, 5))
    new_password = create_entry(new_user_window)
    new_password.pack()

    def save_new_user():
        username = new_username.get()
        password = new_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("🎉 Success", "User created successfully!")
        new_user_window.destroy()

    save_btn = create_button(new_user_window, "Save User", save_new_user)
    save_btn.pack(pady=20)

def forgot_password():
    forgot_window = tk.Toplevel()
    forgot_window.title("🔄 Reset Password")
    forgot_window.geometry("400x400")
    forgot_window.config(bg=tm.get_theme()["bg"])

    tk.Label(forgot_window, text="Reset Your Password", font=("Helvetica", 18, "bold"),
             bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"]).pack(pady=20)

    tk.Label(forgot_window, text="👤 Enter Username", font=("Helvetica", 14),
             bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"]).pack(pady=(10, 5))
    reset_username = create_entry(forgot_window)
    reset_username.pack()

    tk.Label(forgot_window, text="🔒 New Password", font=("Helvetica", 14),
             bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"]).pack(pady=(10, 5))
    reset_password = create_entry(forgot_window)
    reset_password.pack()

    def update_password():
        username = reset_username.get()
        new_pass = reset_password.get()

        if not username or not new_pass:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_pass, username))
        conn.commit()
        conn.close()

        messagebox.showinfo("✅ Password Reset", "Your password has been updated!")
        forgot_window.destroy()

    save_btn = create_button(forgot_window, "Save New Password", update_password)
    save_btn.pack(pady=20)

if __name__ == "__main__":
    open_login()
