from customtkinter import *


app = CTk()
app.title("Test")
app.geometry("500x400")


btn = CTkButton(master = app, text = "Click Me!", corner_radius = 180, fg_color = "transparent", hover_color = "#198458", border_color = "#35b5ca", border_width = 2)
btn.place(relx = 0.5, rely = 0.5, anchor = "s")


app.mainloop()
