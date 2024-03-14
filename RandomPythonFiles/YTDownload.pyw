import customtkinter
import tkinter as tk
import os
from pytube import YouTube
from tkinter import *


# Creates a download folder
Videos = "Videos"
if not os.path.exists(Videos):
    os.makedirs(Videos)


# Creates an icon folder
Icon = "Icon"
if not os.path.exists(Icon):
    os.makedirs(Icon)


# Downloading the video
def startdownload():
    try:
        ytLink = link.get()
        ytobject = YouTube(ytLink, on_progress_callback = on_progress)
        title.configure(text = ytobject.title)
        finish_label.configure(text = "") 
        video = ytobject.streams.get_highest_resolution()
        video.download(Videos)
        finish_label.configure(text = "Download Complete!")
    except:
        finish_label.configure(text = "YT link is invalid")


# Showing how much more of the download there is left to do
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_ondownload = bytes_downloaded / total_size * 100
    per = str(int(percentage_ondownload))   
    pPercent.configure(text = per + "%")
    pPercent.update()
    
    # Update progress bar
    progressbar.set(float(percentage_ondownload / 100))


# Shows where the file was downloaded
def WhereFilePath():
    file_path = os.getcwd()
    fpath.configure(text = file_path + "\\Videos")

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


# The app frame 
app = customtkinter.CTk()
app.geometry("750x400")
app.title("YouTube Downloader by Bernso")
app.iconbitmap(r"C:\Users\benws\Desktop\YTDownload\Icon\Arhururan.ico")


# Adding UI elements
title =  customtkinter.CTkLabel(app, text = "Enter a YT link:", width = 40, height = 5, font = ("Helvetica", 35, "bold"))
title.pack(padx = 20, pady = 20)


# Finished downloaded
finish_label = customtkinter.CTkLabel(app, text = "")
finish_label.pack()


# Link input
url_var = tk.StringVar()
link = customtkinter.CTkEntry(app, width = 350, height = 40, textvariable = url_var)
link.pack()


# Progress %
pPercent = customtkinter.CTkLabel(app, text = "0%")
pPercent.pack()


# Progress bar
progressbar = customtkinter.CTkProgressBar(app, width = 350)
progressbar.set(0)
progressbar.pack(padx = 10, pady = 10)


# Download button
download = customtkinter.CTkButton(app, text = "Download", command = startdownload)
download.pack(padx = 20, pady = 20)


# File path 
fpath = customtkinter.CTkButton(app, text = "Where was my file downloaded?", command = WhereFilePath) 
fpath.pack()


# Close Button
Close = customtkinter.CTkButton(app, text = "Close/Quit", command = quit)
Close.pack(padx = 20, pady = 20)


# Run app
app.mainloop()

