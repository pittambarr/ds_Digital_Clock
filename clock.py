import tkinter as tk
from tkinter import colorchooser
import time
import pytz
from datetime import datetime
# Main window
root = tk.Tk()
root.overrideredirect(True)
# root.attributes("-topmost", True)
root.wm_attributes("-transparentcolor",'#E9DFEC')
root.configure(bg='#E9DFEC')

# Global settings
is_24_hour = True
current_alpha = 0.9  # Default transparency
font_family="DS"
fntsize=35
datesize=20
pop='#E9DFEC'
colr= "white"
date_colr="white"
# Create clock label
label = tk.Label(root, font=(font_family, fntsize,'italic'), fg=colr,bg=pop)
label.pack()
date_label = tk.Label(root, font=(font_family, datesize, "italic"), fg=date_colr, bg=pop)
date_label.pack()
# Update time
def update_time():
    home=pytz.timezone('Asia/Kolkata')
    local_time=datetime.now(home)
    fmt = '%H:%M:%S' if is_24_hour else '%I:%M:%S %p'
    current_date = local_time.strftime("%a, %d %B %y")  # Get current date
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

# Show settings menu
def show_settings(event):
    settings_window = tk.Toplevel(root)
    settings_window.title("Clock Settings")
    settings_window.geometry("300x300")
    settings_window.resizable(0,0)
    settings_window.attributes("-topmost", True)

    tk.Label(settings_window, text="Transparency").pack()

    def update_alpha(val):
        global current_alpha
        current_alpha = float(val)
        root.attributes("-alpha", current_alpha)

    slider = tk.Scale(settings_window, from_=0.1, to=1.0,
                      resolution=0.05, orient='horizontal',
                      command=update_alpha)
    slider.set(current_alpha)
    slider.pack()

    #Change Clock Size 
    def sizeadjust(size):
        size=int(size)
        label.config(font=(font_family, size,'italic'))
    scale = tk.Scale(settings_window, from_=15, to=50, orient='horizontal', label="Clock Resizer",
                              command=sizeadjust)
    scale.set(fntsize)
    scale.pack()
    
    #Change Date Size 
    def sizechang(size):
        size=int(size)
        date_label.config(font=(font_family, size,'italic'))
    scale = tk.Scale(settings_window, from_=10, to=50, orient='horizontal', label="Date Resizer",
                              command=sizechang)
    scale.set(datesize)
    scale.pack()

    def Tickcheck():
        root.attributes("-topmost",True)
    checkbutton=tk.Checkbutton(settings_window,text="Top Most",command=Tickcheck)
    checkbutton.pack()
    #Change Time Font color
    def Chosetimecolor():
        color_code = colorchooser.askcolor(title="Choose Text Color")[1]
        if color_code:
            colr.set(color_code)
            label.config(fg=color_code)
    bg_button = tk.Button(settings_window, text="Choose Clock Color", command=Chosetimecolor)
    bg_button.pack(pady=5)
    colr=tk.StringVar()

   

    #Change Date Font color
    def Chosedatecolor():
        color_code = colorchooser.askcolor(title="Choose Date Color")[1]
        if color_code:
            date_colr.set(color_code)
            date_label.config(fg=color_code)
    bg_button = tk.Button(settings_window, text="Choose Date Color", command=Chosedatecolor)
    bg_button.pack(pady=5)
    date_colr=tk.StringVar()

    
# Bind events
label.bind("<Button-1>", start_move)
label.bind("<B1-Motion>", do_move)
label.bind("<Double-1>", toggle_format)
label.bind("<Triple-1>", close_app)     # Triple click to close
label.bind("<Button-3>", show_settings)  # Right click for settings

# Set initial transparency
root.attributes("-alpha", current_alpha)

# Start clock
update_time()
root.mainloop()
