# ui/award_management.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import db_helper as db
from utils import theme_manager as tm
from utils.ui_helpers import create_entry, create_button
import pandas as pd

def open_award_window():
    window = tk.Toplevel()
    window.title("Manage Awards 🏆 - ClubConnect")
    window.geometry("1400x850")
    window.config(bg=tm.get_theme()["bg"])
    window.resizable(True, True)

    # Grid setup
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    def switch_theme():
        tm.toggle_theme()
        window.destroy()
        open_award_window()

    # ====== Header ======
    header = tk.Frame(window, bg=tm.get_theme()["header_bg"], height=60)
    header.grid(row=0, column=0, columnspan=3, sticky="nsew")

    title = tk.Label(header, text="Manage Awards 🏆", font=("Helvetica", 22, "bold"),
                     bg=tm.get_theme()["header_bg"], fg=tm.get_theme()["header_fg"])
    title.pack(side="left", padx=20)

    theme_btn = create_button(header, "Toggle Dark/Light Mode 🌗", switch_theme, font_size=10, width=20)
    theme_btn.pack(side="right", padx=20)

    # ====== Left Panel (Search Area) ======
    left_panel = tk.Frame(window, bg=tm.get_theme()["panel_left"], width=300)
    left_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(left_panel, text="🔎 Search by Member Name:", font=("Helvetica", 14),
             bg=tm.get_theme()["panel_left"], fg=tm.get_theme()["fg"]).pack(pady=(20, 5))
    search_entry = create_entry(left_panel, width=25)
    search_entry.pack(pady=5)

    search_btn = create_button(left_panel, "Search 🔎", lambda: search_awards(), font_size=12, width=24)
    search_btn.pack(pady=(30, 10))

    reset_btn = create_button(left_panel, "Reset Fields 🔄", lambda: reset_fields(), font_size=12, width=24)
    reset_btn.pack(pady=10)

    export_btn = create_button(left_panel, "Export Awards 📄", lambda: export_awards(), font_size=12, width=24)
    export_btn.pack(pady=(30, 10))

    # ====== Center Panel (Table with Scrollbars inside Card) ======
    center_panel = tk.Frame(window, bg=tm.get_theme()["bg"])
    center_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    center_panel.grid_rowconfigure(0, weight=1)
    center_panel.grid_columnconfigure(0, weight=1)

    table_card = tk.Frame(center_panel, bg="#f9f9f9", bd=2, relief="ridge")
    table_card.grid(row=0, column=0, sticky="nsew")

    columns = ("ID", "Member Name", "Competition", "Category", "Year", "Prize")

    tree_scroll_y = ttk.Scrollbar(table_card, orient="vertical")
    tree_scroll_y.pack(side="right", fill="y")

    tree_scroll_x = ttk.Scrollbar(table_card, orient="horizontal")
    tree_scroll_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(table_card, columns=columns, show="headings",
                        yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    tree.pack(fill="both", expand=True)

    for col in columns:
        width = 180 if col in ("Member Name", "Competition") else 150
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="center")

    def refresh_table(data=None):
        for row in tree.get_children():
            tree.delete(row)
        if data is None:
            data = db.get_all_awards()
        for award in data:
            tree.insert("", "end", values=award)

    refresh_table()

    # ====== Right Panel (Action Buttons) ======
    right_panel = tk.Frame(window, bg=tm.get_theme()["panel_right"], width=300)
    right_panel.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

    add_btn = create_button(right_panel, "Add Award ➕", lambda: add_award(), font_size=12, width=24)
    add_btn.pack(pady=(50, 20))

    delete_btn = create_button(right_panel, "Delete Award 🗑️", lambda: delete_award(), font_size=12, width=24)
    delete_btn.pack(pady=10)

    delete_all_btn = create_button(right_panel, "Delete All Awards 🗑️", lambda: delete_all_awards(), font_size=12, width=24)
    delete_all_btn.pack(pady=10)

    back_btn = create_button(right_panel, "⬅️ Back to Dashboard", lambda: window.destroy(), font_size=12, width=24)
    back_btn.pack(pady=40)

    # ====== Functions ======
    def search_awards():
        all_awards = db.get_all_awards()
        filtered = []
        for a in all_awards:
            if search_entry.get().lower() in a[1].lower():
                filtered.append(a)
        refresh_table(filtered)

    def reset_fields():
        search_entry.delete(0, 'end')

    def add_award():
        add_window = tk.Toplevel()
        add_window.title("Add Award ➕")
        add_window.geometry("400x500")
        add_window.config(bg=tm.get_theme()["bg"])

        members_data = db.get_all_members()
        member_options = [f"{m[0]} - {m[1]}" for m in members_data]

        tk.Label(add_window, text="Select Member 👤", font=("Helvetica", 14),
                 bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"]).pack(pady=5)
        selected_member = tk.StringVar()
        member_dropdown = ttk.Combobox(add_window, textvariable=selected_member,
                                       values=member_options, font=("Helvetica", 12))
        member_dropdown.pack(pady=5)

        fields = ["Competition Name 🏆", "Category 🏷️", "Year 📅", "Prize 🥇"]
        entries = {}

        for field in fields:
            tk.Label(add_window, text=field, font=("Helvetica", 14),
                     bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"]).pack(pady=5)
            entries[field] = create_entry(add_window)
            entries[field].pack(pady=5)

        def save_award():
            if not selected_member.get() or any(entries[f].get() == "" for f in fields):
                messagebox.showerror("Error", "Please fill all fields!")
                return

            member_id = selected_member.get().split(" - ")[0]
            competition_name = entries["Competition Name 🏆"].get()
            category = entries["Category 🏷️"].get()
            year = entries["Year 📅"].get()
            prize = entries["Prize 🥇"].get()

            db.add_award(member_id, competition_name, category, year, prize)
            refresh_table()
            add_window.destroy()
            messagebox.showinfo("🎉 Success", "Award added successfully!")

        save_btn = create_button(add_window, "Save Award", save_award)
        save_btn.pack(pady=20)

    def delete_award():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select an award to delete!")
            return
        values = tree.item(selected, 'values')
        award_id = values[0]
        confirm = messagebox.askyesno("Confirm", f"Delete award {values[2]} for {values[1]}?")
        if confirm:
            db.delete_award(award_id)
            refresh_table()
            messagebox.showinfo("🎯 Success", "Award deleted!")

    def delete_all_awards():
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete ALL awards?")
        if confirm:
            db.clear_all_awards()
            refresh_table()
            messagebox.showinfo("🎯 Success", "All awards deleted!")

    def export_awards():
        path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                            filetypes=[("Excel Files", "*.xlsx")])
        if path:
            all_awards = db.get_all_awards()
            df = pd.DataFrame(all_awards, columns=["ID", "Member Name", "Competition", "Category", "Year", "Prize"])
            df.to_excel(path, index=False)
            messagebox.showinfo("✅ Exported", f"Awards exported to {path}")

    window.mainloop()
