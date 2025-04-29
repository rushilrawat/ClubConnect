# ui/settings_page.py

import tkinter as tk
from tkinter import ttk
from utils import theme_manager as tm

# This will store selected font globally
current_font = "Helvetica"
current_username = "Guest"

def open_settings(parent_window):
    settings_window = tk.Toplevel(parent_window)
    settings_window.title("Settings - ClubConnect")
    settings_window.geometry("300x500")
    settings_window.config(bg=tm.get_theme()["bg"])
    settings_window.resizable(False, False)

    # ====== Title ======
    title = tk.Label(settings_window, text="⚙️ Settings", font=("Helvetica", 20, "bold"),
                     bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"])
    title.pack(pady=20)

    # ====== Font Selection ======
    font_label = tk.Label(settings_window, text="Select Font:", font=("Helvetica", 14),
                          bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"])
    font_label.pack(pady=(10, 5))

    font_options = ["Helvetica", "Arial", "Times New Roman", "Courier New", "Comic Sans MS"]
    selected_font = tk.StringVar(value=current_font)

    font_dropdown = ttk.Combobox(settings_window, textvariable=selected_font,
                                 values=font_options, font=("Helvetica", 12))
    font_dropdown.pack(pady=5)

    def apply_font():
        global current_font
        current_font = selected_font.get()
        tk.messagebox.showinfo("Font Changed", f"New Font: {current_font}")

    font_btn = tk.Button(settings_window, text="Apply Font",
                         command=apply_font, bg=tm.get_theme()["button_bg"],
                         fg=tm.get_theme()["button_fg"], font=("Helvetica", 12),
                         relief="flat", padx=10, pady=5)
    font_btn.pack(pady=10)

    # ====== Theme Toggle ======
    theme_label = tk.Label(settings_window, text="Theme:", font=("Helvetica", 14),
                           bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"])
    theme_label.pack(pady=(20, 5))

    theme_btn = tk.Button(settings_window, text="Toggle Dark/Light Mode",
                          command=lambda: [tm.toggle_theme(), settings_window.destroy()],
                          bg=tm.get_theme()["button_bg"], fg=tm.get_theme()["button_fg"],
                          font=("Helvetica", 12), relief="flat", padx=10, pady=5)
    theme_btn.pack(pady=10)

    # ====== Current User Display ======
    user_label = tk.Label(settings_window, text=f"👤 Current User:\n{current_username}",
                          font=("Helvetica", 14), bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"])
    user_label.pack(pady=40)

    settings_window.mainloop()

# Utility to set current username (during login)
def set_username(username):
    global current_username
    current_username = username
