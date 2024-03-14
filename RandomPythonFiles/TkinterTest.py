import tkinter as tk
import random

def beans():
    text.configure(text = random.randint(1,999))


app = tk.Tk()

app.geometry("1000x500")

text = tk.Label(text = "WSG", command = beans)
text.pack()

app.mainloop()
