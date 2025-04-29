# utils/theme_manager.py

# Global Theme Manager for ClubConnect

theme_mode = "light"  # Default Mode

# Light Theme
LIGHT_THEME = {
    "bg": "#f0f8ff",  # Alice Blue background
    "fg": "#1a1a1a",  # Darker text
    "entry_bg": "#ffffff",
    "entry_fg": "#000000",
    "button_bg": "#1976D2",  # Fresh Blue Buttons
    "button_fg": "#ffffff",  # White text inside buttons
    "button_hover_bg": "#1565C0",  # Slightly darker blue on hover
    "button_hover_fg": "#ffffff",
    "card_bg": "#ffffff",
    "card_shadow": "#d0d0d0",
    "panel_left": "#E3F2FD",    # Soft Light Blue
    "panel_right": "#FFF8E1",   # Soft Light Yellow
    "header_bg": "#1976D2",     # Bright Header Blue
    "header_fg": "#ffffff",
    "chart_bg": "#ffffff",
    "chart_text": "#000000",
    "treeview_bg": "#f9f9f9",    # Light Gray background for tables
}

# Dark Theme
DARK_THEME = {
    "bg": "#121212",    # Very Dark
    "fg": "#ffffff",
    "entry_bg": "#1f1f1f",
    "entry_fg": "#ffffff",
    "button_bg": "#546E7A",    # Cool Blue-Gray Buttons
    "button_fg": "#ffffff",
    "button_hover_bg": "#78909C",
    "button_hover_fg": "#ffffff",
    "card_bg": "#1e1e1e",
    "card_shadow": "#333333",
    "panel_left": "#263238",
    "panel_right": "#37474F",
    "header_bg": "#263238",
    "header_fg": "#ffffff",
    "chart_bg": "#1e1e1e",
    "chart_text": "#ffffff",
    "treeview_bg": "#1f1f1f",   # Dark Treeview background
}

def get_theme():
    return DARK_THEME if theme_mode == "dark" else LIGHT_THEME

def toggle_theme():
    global theme_mode
    theme_mode = "dark" if theme_mode == "light" else "light"
