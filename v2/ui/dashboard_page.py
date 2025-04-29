# ui/dashboard_page.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import db_helper as db
from utils import theme_manager as tm
from utils.ui_helpers import create_card, create_button

def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("ClubConnect Dashboard 📊")
    dashboard.geometry("1400x850")
    dashboard.config(bg=tm.get_theme()["bg"])
    dashboard.resizable(True, True)

    def switch_theme():
        tm.toggle_theme()
        dashboard.destroy()
        open_dashboard()

    # ====== Header ======
    header = tk.Frame(dashboard, bg=tm.get_theme()["header_bg"], height=60)
    header.pack(side="top", fill="x")

    title = tk.Label(header, text="📊 ClubConnect Dashboard", font=("Helvetica", 22, "bold"),
                     bg=tm.get_theme()["header_bg"], fg=tm.get_theme()["header_fg"])
    title.pack(pady=10, padx=20, side="left")

    theme_btn = create_button(header, "Toggle Dark/Light Mode 🌗", switch_theme, font_size=10, width=20)
    theme_btn.pack(side="right", padx=20)

    # ====== Main Layout ======
    main_frame = tk.Frame(dashboard, bg=tm.get_theme()["bg"])
    main_frame.pack(fill="both", expand=True)

    # ====== Left Panel (Big Metric Cards) ======
    left_panel = tk.Frame(main_frame, bg=tm.get_theme()["panel_left"], width=300)
    left_panel.pack(side="left", fill="y")

    total_members = db.get_total_members()
    total_awards = db.get_total_awards()
    top_performer_name, _ = db.get_top_performer()

    create_metric_card(left_panel, "👥", "Total Members", total_members)
    create_metric_card(left_panel, "🏆", "Total Awards", total_awards)
    create_metric_card(left_panel, "🎖️", "Top Performer", top_performer_name)

    # ====== Center Panel (Charts Grid 2x2) ======
    center_panel = tk.Frame(main_frame, bg=tm.get_theme()["bg"])
    center_panel.pack(side="left", fill="both", expand=True)

    chart_grid = tk.Frame(center_panel, bg=tm.get_theme()["bg"])
    chart_grid.pack(padx=20, pady=20)

    create_charts(chart_grid)

    # ====== Right Panel (Quick Buttons) ======
    right_panel = tk.Frame(main_frame, bg=tm.get_theme()["panel_right"], width=280)
    right_panel.pack(side="left", fill="y")

    manage_members_btn = create_button(right_panel, "Manage Members 👥", open_member_management)
    manage_members_btn.pack(pady=(50, 20))

    manage_awards_btn = create_button(right_panel, "Manage Awards 🏆", open_award_management)
    manage_awards_btn.pack(pady=20)

    backup_btn = create_button(right_panel, "Backup Database 💾", backup_database)
    backup_btn.pack(pady=20)

    dashboard.mainloop()

# ====== Functions for Metric Cards ======
def create_metric_card(parent, emoji, title, value):
    card = tk.Frame(parent, bg=tm.get_theme()["card_bg"], bd=2, relief="groove", width=250, height=150)
    card.pack(pady=20, padx=20)

    icon_label = tk.Label(card, text=emoji, font=("Helvetica", 32),
                          bg=tm.get_theme()["card_bg"], fg=tm.get_theme()["fg"])
    icon_label.place(relx=0.5, rely=0.2, anchor="center")

    title_label = tk.Label(card, text=title, font=("Helvetica", 14, "bold"),
                           bg=tm.get_theme()["card_bg"], fg=tm.get_theme()["fg"])
    title_label.place(relx=0.5, rely=0.55, anchor="center")

    value_label = tk.Label(card, text=str(value), font=("Helvetica", 18, "bold"),
                           bg=tm.get_theme()["card_bg"], fg=tm.get_theme()["fg"])
    value_label.place(relx=0.5, rely=0.8, anchor="center")

# ====== Function to Create 2x2 Charts ======
def create_charts(parent):
    awards_data = db.get_all_awards()
    members_data = db.get_all_members()

    # Awards by Category (Pie Chart)
    category_counts = {}
    for award in awards_data:
        category = award[3]
        category_counts[category] = category_counts.get(category, 0) + 1

    fig1 = Figure(figsize=(4, 3), dpi=100, facecolor=tm.get_theme()["chart_bg"])
    ax1 = fig1.add_subplot(111)
    ax1.pie(category_counts.values(), labels=category_counts.keys(), autopct='%1.1f%%', startangle=140)
    ax1.set_title("🏷️ Awards by Category", color=tm.get_theme()["fg"])

    pie_canvas = FigureCanvasTkAgg(fig1, master=parent)
    pie_canvas.draw()
    pie_canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)

    # Top Competitions (Bar Chart)
    competition_counts = {}
    for award in awards_data:
        competition = award[2]
        competition_counts[competition] = competition_counts.get(competition, 0) + 1

    fig2 = Figure(figsize=(4, 3), dpi=100, facecolor=tm.get_theme()["chart_bg"])
    ax2 = fig2.add_subplot(111)
    ax2.barh(list(competition_counts.keys()), list(competition_counts.values()), color=['#66b3ff', '#99ff99', '#ff9999'])
    ax2.set_xlabel('Number of Awards', color=tm.get_theme()["fg"])
    ax2.set_title('🏆 Top Competitions', color=tm.get_theme()["fg"])

    bar_canvas = FigureCanvasTkAgg(fig2, master=parent)
    bar_canvas.draw()
    bar_canvas.get_tk_widget().grid(row=0, column=1, padx=20, pady=20)

    # Awards Growth over Years (Line Chart)
    year_counts = {}
    for award in awards_data:
        year = award[4]
        year_counts[year] = year_counts.get(year, 0) + 1

    years = sorted(year_counts.keys())
    awards_per_year = [year_counts[y] for y in years]

    fig3 = Figure(figsize=(4, 3), dpi=100, facecolor=tm.get_theme()["chart_bg"])
    ax3 = fig3.add_subplot(111)
    ax3.plot(years, awards_per_year, marker='o', color='green')
    ax3.set_xlabel('Year', color=tm.get_theme()["fg"])
    ax3.set_ylabel('Awards', color=tm.get_theme()["fg"])
    ax3.set_title('📈 Awards Growth Over Years', color=tm.get_theme()["fg"])

    line_canvas = FigureCanvasTkAgg(fig3, master=parent)
    line_canvas.draw()
    line_canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=20)

    # Class-wise Student Distribution (Pie Chart)
    class_counts = {}
    for member in members_data:
        student_class = member[7]
        class_counts[student_class] = class_counts.get(student_class, 0) + 1

    fig4 = Figure(figsize=(4, 3), dpi=100, facecolor=tm.get_theme()["chart_bg"])
    ax4 = fig4.add_subplot(111)
    ax4.pie(class_counts.values(), labels=class_counts.keys(), autopct='%1.1f%%', startangle=140)
    ax4.set_title('📚 Class-wise Students', color=tm.get_theme()["fg"])

    class_canvas = FigureCanvasTkAgg(fig4, master=parent)
    class_canvas.draw()
    class_canvas.get_tk_widget().grid(row=1, column=1, padx=20, pady=20)

# ====== Other Functions ======
def open_member_management():
    import ui.member_management as member_mgmt
    member_mgmt.open_member_window()

def open_award_management():
    import ui.award_management as award_mgmt
    award_mgmt.open_award_window()

def backup_database():
    import shutil
    import datetime
    import os

    if not os.path.exists('backups'):
        os.makedirs('backups')

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"clubconnect_backup_{timestamp}.db"
    backup_path = os.path.join('backups', backup_filename)

    try:
        shutil.copy('database/clubconnect.db', backup_path)
        messagebox.showinfo("💾 Backup Successful", f"Backup created at: {backup_path}")
    except Exception as e:
        messagebox.showerror("❌ Backup Failed", str(e))

if __name__ == "__main__":
    open_dashboard()
