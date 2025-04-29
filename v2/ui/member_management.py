# ui/member_management.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import db_helper as db
from utils import theme_manager as tm
from utils.ui_helpers import create_entry, create_button
import pandas as pd

def open_member_window():
    window = tk.Toplevel()
    window.title("Manage Members 👥 - ClubConnect")
    window.geometry("1400x850")
    window.config(bg=tm.get_theme()["bg"])
    window.resizable(True, True)

    # Grid setup
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    def switch_theme():
        tm.toggle_theme()
        window.destroy()
        open_member_window()

    # ====== Header ======
    header = tk.Frame(window, bg=tm.get_theme()["header_bg"], height=60)
    header.grid(row=0, column=0, columnspan=3, sticky="nsew")

    title = tk.Label(header, text="Manage Members 👥", font=("Helvetica", 22, "bold"),
                     bg=tm.get_theme()["header_bg"], fg=tm.get_theme()["header_fg"])
    title.pack(side="left", padx=20)

    theme_btn = create_button(header, "Toggle Dark/Light Mode 🌗", switch_theme, font_size=10, width=20)
    theme_btn.pack(side="right", padx=20)

    # ====== Left Panel (Search Area) ======
    left_panel = tk.Frame(window, bg=tm.get_theme()["panel_left"], width=300)
    left_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(left_panel, text="🔎 Search Name:", font=("Helvetica", 14),
             bg=tm.get_theme()["panel_left"], fg=tm.get_theme()["fg"]).pack(pady=(20, 5))
    search_entry = create_entry(left_panel, width=25)
    search_entry.pack(pady=5)

    tk.Label(left_panel, text="🏫 Class:", font=("Helvetica", 14),
             bg=tm.get_theme()["panel_left"], fg=tm.get_theme()["fg"]).pack(pady=(20, 5))
    class_var = tk.StringVar()
    class_dropdown = ttk.Combobox(left_panel, textvariable=class_var,
                                  values=["", "IX", "X", "XI", "XII"], font=("Helvetica", 12), width=22)
    class_dropdown.pack(pady=5)

    tk.Label(left_panel, text="🏢 Section:", font=("Helvetica", 14),
             bg=tm.get_theme()["panel_left"], fg=tm.get_theme()["fg"]).pack(pady=(20, 5))
    section_var = tk.StringVar()
    section_dropdown = ttk.Combobox(left_panel, textvariable=section_var,
                                    values=["", "A", "B", "C", "D", "E"], font=("Helvetica", 12), width=22)
    section_dropdown.pack(pady=5)

    search_btn = create_button(left_panel, "Search 🔎", lambda: search_members(), font_size=12, width=24)
    search_btn.pack(pady=(30, 10))

    reset_btn = create_button(left_panel, "Reset Fields 🔄", lambda: reset_fields(), font_size=12, width=24)
    reset_btn.pack(pady=10)

    export_btn = create_button(left_panel, "Export Members 📄", lambda: export_members(), font_size=12, width=24)
    export_btn.pack(pady=(30, 10))

    # ====== Center Panel (Table with Scrollbars inside Card) ======
    center_panel = tk.Frame(window, bg=tm.get_theme()["bg"])
    center_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    center_panel.grid_rowconfigure(0, weight=1)
    center_panel.grid_columnconfigure(0, weight=1)

    table_card = tk.Frame(center_panel, bg="#f9f9f9", bd=2, relief="ridge")
    table_card.grid(row=0, column=0, sticky="nsew")

    columns = ("ID", "Name", "Email", "Phone", "Gender", "Admission No", "Class", "Section", "Club")

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
        width = 200 if col in ("Name", "Email") else 150
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="center")

    def refresh_table(data=None):
        for row in tree.get_children():
            tree.delete(row)
        if data is None:
            data = db.get_all_members()
        for member in data:
            tree.insert("", "end", values=member)

    refresh_table()

    # ====== Right Panel (Action Buttons) ======
    right_panel = tk.Frame(window, bg=tm.get_theme()["panel_right"], width=300)
    right_panel.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

    add_btn = create_button(right_panel, "Add Member ➕", lambda: add_member(), font_size=12, width=24)
    add_btn.pack(pady=(50, 20))

    delete_btn = create_button(right_panel, "Delete Member 🗑️", lambda: delete_member(), font_size=12, width=24)
    delete_btn.pack(pady=10)

    delete_all_btn = create_button(right_panel, "Delete All Members 🗑️", lambda: delete_all_members(), font_size=12, width=24)
    delete_all_btn.pack(pady=10)

    back_btn = create_button(right_panel, "⬅️ Back to Dashboard", lambda: window.destroy(), font_size=12, width=24)
    back_btn.pack(pady=40)

    # ====== Functions ======
    def search_members():
        all_members = db.get_all_members()
        filtered = []
        for m in all_members:
            if (search_entry.get().lower() in m[1].lower()) and \
               (class_var.get() == "" or class_var.get() == m[7]) and \
               (section_var.get() == "" or section_var.get() == m[8]):
                filtered.append(m)
        refresh_table(filtered)

    def reset_fields():
        search_entry.delete(0, 'end')
        class_var.set("")
        section_var.set("")

    def add_member():
        add_window = tk.Toplevel()
        add_window.title("Add Member ➕")
        add_window.geometry("400x600")
        add_window.config(bg=tm.get_theme()["bg"])

        fields = ["Name", "Email", "Phone", "DOB", "Gender", "Admission No", "Class", "Section", "Club"]
        entries = {}

        for idx, field in enumerate(fields):
            tk.Label(add_window, text=field, font=("Helvetica", 14),
                     bg=tm.get_theme()["bg"], fg=tm.get_theme()["fg"]).pack(pady=5)
            entries[field] = create_entry(add_window)
            entries[field].pack(pady=5)

        def save_member():
            values = [entries[f].get() for f in fields]
            if "" in values:
                messagebox.showerror("Error", "Please fill all fields!")
            else:
                db.add_member(*values)
                refresh_table()
                add_window.destroy()
                messagebox.showinfo("🎉 Success", "Member added!")

        save_btn = create_button(add_window, "Save Member", save_member)
        save_btn.pack(pady=20)

    def delete_member():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a member to delete!")
            return
        values = tree.item(selected, 'values')
        member_id = values[0]
        confirm = messagebox.askyesno("Confirm", f"Delete member {values[1]}?")
        if confirm:
            db.delete_member(member_id)
            refresh_table()
            messagebox.showinfo("🎯 Success", "Member deleted!")

    def delete_all_members():
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete ALL members?")
        if confirm:
            db.clear_all_members()
            refresh_table()
            messagebox.showinfo("🎯 Success", "All members deleted!")

    def export_members():
        path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                            filetypes=[("Excel Files", "*.xlsx")])
        if path:
            all_members = db.get_all_members()
            df = pd.DataFrame(all_members, columns=["ID", "Name", "Email", "Phone", "Gender",
                                                     "Admission No", "Class", "Section", "Club"])
            df.to_excel(path, index=False)
            messagebox.showinfo("✅ Exported", f"Members exported to {path}")

    window.mainloop()
