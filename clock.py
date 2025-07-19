import tkinter as tk
from tkinter import font, colorchooser
import time
import pytz
from datetime import datetime
import json
import os

# Constants
SETTINGS_FILE = "clock_settings.json"

# Main window
root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-transparentcolor", "#010101")
root.configure(bg="#010101")

# Global settings
is_24_hour = True
current_alpha = 0.9
font_family = "DS-digital"
fntsize = 35
datesize = 20
style = "bold"
pop = "#010101"
colr = tk.StringVar(value="white")
date_colr = tk.StringVar(value="white")

# Create clock label
label = tk.Label(root, font=(font_family, fntsize, style), fg=colr.get(), bg=pop)
label.pack()
date_label = tk.Label(root, font=(font_family, datesize), fg=date_colr.get(), bg=pop)
date_label.pack()

# Timezone
home = pytz.timezone('Asia/Kolkata')

# Update time
def update_time():
    local_time = datetime.now(home)
    fmt = '%H:%M:%S' if is_24_hour else '%I:%M:%S %p'
    current_date = local_time.strftime("%a, %d %B %y")
    label.config(text=local_time.strftime(fmt))
    date_label.config(text=current_date)
    root.after(200, update_time)

# Dragging functions
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f"+{x}+{y}")

# Toggle 12/24 hour format
def toggle_format(event):
    global is_24_hour
    is_24_hour = not is_24_hour

# Close on Triple click
def close_app(event):
    root.destroy()

# Save and load settings
def save_settings():
    settings = {
        "font_family": font_family,
        "fntsize": fntsize,
        "datesize": datesize,
        "time_color": colr.get(),
        "date_color": date_colr.get(),
        "alpha": current_alpha,
        "is_24_hour": is_24_hour,
        "topmost": root.attributes("-topmost")
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def load_settings():
    global font_family, fntsize, datesize, current_alpha, is_24_hour
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            font_family = settings.get("font_family", font_family)
            fntsize = settings.get("fntsize", fntsize)
            datesize = settings.get("datesize", datesize)
            colr.set(settings.get("time_color", colr.get()))
            date_colr.set(settings.get("date_color", date_colr.get()))
            current_alpha = settings.get("alpha", current_alpha)
            is_24_hour = settings.get("is_24_hour", is_24_hour)
            root.attributes("-alpha", current_alpha)
            root.attributes("-topmost", settings.get("topmost", False))

            # Apply loaded settings
            label.config(font=(font_family, fntsize, style), fg=colr.get())
            date_label.config(font=(font_family, datesize), fg=date_colr.get())

# Settings window
def show_settings(event):
    settings_window = tk.Toplevel(root)
    settings_window.title("Clock Settings")
    settings_window.geometry("400x400")
    settings_window.resizable(0, 0)
    settings_window.attributes("-topmost", True)

    # Transparency slider
    tk.Label(settings_window, text="Transparency").pack()
    def update_alpha(val):
        global current_alpha
        current_alpha = float(val)
        root.attributes("-alpha", current_alpha)
    alpha_slider = tk.Scale(settings_window, from_=0.1, to=1.0, resolution=0.05,
                            orient='horizontal', command=update_alpha)
    alpha_slider.set(current_alpha)
    alpha_slider.pack()

    # Clock size slider
    def sizeadjust(size):
        global fntsize
        fntsize = int(size)
        label.config(font=(font_family, fntsize, style))
    clock_size_slider = tk.Scale(settings_window, from_=15, to=50,
                                 orient='horizontal', label="Clock Resizer", command=sizeadjust)
    clock_size_slider.set(fntsize)
    clock_size_slider.pack()

    # Date size slider
    def sizechang(size):
        global datesize
        datesize = int(size)
        date_label.config(font=(font_family, datesize))
    date_size_slider = tk.Scale(settings_window, from_=10, to=50,
                                orient='horizontal', label="Date Resizer", command=sizechang)
    date_size_slider.set(datesize)
    date_size_slider.pack()

    # Topmost checkbox
    topmost_var = tk.BooleanVar(value=root.attributes("-topmost"))
    def Tickcheck():
        root.attributes("-topmost", topmost_var.get())
    checkbutton = tk.Checkbutton(settings_window, text="Top Most",
                                 variable=topmost_var, command=Tickcheck)
    checkbutton.pack()

    # Choose clock color
    def Chosetimecolor():
        color_code = colorchooser.askcolor(title="Choose Clock Color")[1]
        if color_code:
            colr.set(color_code)
            label.config(fg=color_code)
    tk.Button(settings_window, text="Choose Clock Color", command=Chosetimecolor).pack(pady=5)

    # Choose date color
    def Chosedatecolor():
        color_code = colorchooser.askcolor(title="Choose Date Color")[1]
        if color_code:
            date_colr.set(color_code)
            date_label.config(fg=color_code)
    tk.Button(settings_window, text="Choose Date Color", command=Chosedatecolor).pack(pady=5)

    # Font dropdown
    def update_font(selected_font):
        global font_family
        font_family = selected_font
        label.config(font=(font_family, fntsize, style))
        date_label.config(font=(font_family, datesize))
    available_fonts = sorted(font.families())
    font_family_var = tk.StringVar(value=font_family)
    tk.Label(settings_window, text="Choose Font").pack()
    tk.OptionMenu(settings_window, font_family_var, *available_fonts, command=update_font).pack(pady=10)

    # Save button
    tk.Button(settings_window, text="Save Settings", command=save_settings).pack(pady=10)

    # Auto-save on close
    settings_window.protocol("WM_DELETE_WINDOW", lambda: (save_settings(), settings_window.destroy()))

# Bind events
label.bind("<Button-1>", start_move)
label.bind("<B1-Motion>", do_move)
label.bind("<Double-1>", toggle_format)
label.bind("<Triple-1>", close_app)
label.bind("<Button-3>", show_settings)

# Load settings and start clock
load_settings()
root.attributes("-alpha", current_alpha)
update_time()
root.mainloop()
