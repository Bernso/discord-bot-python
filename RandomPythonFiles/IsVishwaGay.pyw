import customtkinter
import tkinter as tk
import random

def vishwagay():
    gay = random.randint(1,2)
    if gay == 1:
        gay = "You Are Gay"
    else:
        gay = "You Are Not Gay"
    button.configure(text = gay)


app = customtkinter.CTk()
app.geometry("1520x630")
app.title("Vishwa is a Monkey")
app.iconbitmap(r"C:\Users\benws\Desktop\YTDownload\Icon\Arhururan.ico")
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")


title = customtkinter.CTkLabel(app, text = "Vishwa are you gay?", width = 40, height = 5, font = ("Helvetica", 135, "bold"))
title.pack(padx = 20, pady = 20)

button = customtkinter.CTkButton(app, text = "Is Vishwa Gay?", width = 40, height = 5, font = ("helvectica", 135, "bold"), command = vishwagay)
button.pack(padx = 20, pady = 20)

button2 = customtkinter.CTkButton(app, text = "Exit", width = 40, height = 5, font = ("helvectica", 135, "bold"), command = exit)
button2.pack(padx = 20, pady = 20)

# Run app
app.mainloop()