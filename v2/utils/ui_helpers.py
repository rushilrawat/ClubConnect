# utils/ui_helpers.py

import tkinter as tk
from utils import theme_manager as tm

def create_entry(parent, width=25, font_size=14):
    entry = tk.Entry(parent,
                     font=("Helvetica", font_size),
                     width=width,
                     bg=tm.get_theme()["entry_bg"],
                     fg=tm.get_theme()["entry_fg"],
                     insertbackground=tm.get_theme()["entry_fg"],  # Cursor color
                     highlightthickness=1,
                     relief="flat",
                     highlightbackground=tm.get_theme()["button_bg"],
                     highlightcolor=tm.get_theme()["button_hover_bg"])
    entry.configure(borderwidth=2)
    return entry

def create_button(parent, text, command, font_size=14, width=20, height=None):
    button = tk.Button(parent, text=text, command=command,
                       font=("Helvetica", font_size),
                       width=width,
                       bg=tm.get_theme()["button_bg"],
                       fg=tm.get_theme()["button_fg"],
                       activebackground=tm.get_theme()["button_hover_bg"],
                       activeforeground=tm.get_theme()["button_hover_fg"],
                       relief="flat",
                       bd=0,
                       padx=10, pady=5)
    button.configure(borderwidth=0, highlightthickness=0)

    # Add hover effect manually
    def on_enter(e):
        button.config(bg=tm.get_theme()["button_hover_bg"], fg=tm.get_theme()["button_hover_fg"])
    def on_leave(e):
        button.config(bg=tm.get_theme()["button_bg"], fg=tm.get_theme()["button_fg"])

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return button

def create_card(parent, width=300, height=150):
    card = tk.Frame(parent,
                    bg=tm.get_theme()["card_bg"],
                    bd=0,
                    highlightbackground=tm.get_theme()["card_shadow"],
                    highlightthickness=2,
                    width=width,
                    height=height)
    return card
