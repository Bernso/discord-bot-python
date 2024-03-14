import customtkinter
import tkinter as tk
from tkinter import *

global timespressed
timespressed = 0

def buttonpress():
    global timespressed
    timespressed += 1
    button.configure(text = f"You have pressed the button {timespressed} time(s)")

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App Frame
app = customtkinter.CTk()
app.geometry("720x200")
app.title("Click da button")
app.iconbitmap(r"C:\Users\benws\Desktop\YTDownload\Icon\Arhururan.ico")

button = customtkinter.CTkButton(app, text = "Click Me", width = 40, height = 5, font = ("Helvetica", 35, "bold"), command = buttonpress)
button.pack(padx = 20, pady = 20)

button2 = customtkinter.CTkButton(app, text = "Exit", width = 40, height = 5, font = ("Helvectica", 20, "bold"), command = exit)
button2.pack(padx = 20, pady = 20)


# Run app
app.mainloop()