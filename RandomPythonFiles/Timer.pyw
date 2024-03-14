import time
import customtkinter

import tkinter as tk


def start_timer():
    seconds = int(entry.get())
    countdown_timer(seconds)


def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        TimeRemaining.set(f"Time remaining: {i} seconds")
        app.update()
        time.sleep(1)
    TimeRemaining.set("Time's up!")


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("520x330")
app.title("Timer by Bernso")
app.iconbitmap(r"C:\Users\benws\Desktop\YTDownload\Icon\Arhururan.ico")
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")


title = customtkinter.CTkLabel(app, text="Timer", width=40, height=5, font=("Helvetica", 35, "bold"))
title.pack(padx=20, pady=20)


timebox = tk.StringVar()
entry = customtkinter.CTkEntry(app, width=350, height=40, textvariable=timebox)
entry.pack()


button = customtkinter.CTkButton(app, text="Start", width=40, height=5, font=("Helvetica", 35, "bold"), command=start_timer)
button.pack(padx=20, pady=20)


TimeRemaining = tk.StringVar()
TimeRemaining.set("Time Remaining:")


TimeLeft = customtkinter.CTkEntry(app, width = 350, height = 40, textvariable = TimeRemaining)
TimeLeft.pack()


exit_button = customtkinter.CTkButton(app, text="Exit", width=40, height=5, font=("Helvetica", 35, "bold"), command=exit)
exit_button.pack(padx=20, pady=20)


app.mainloop()