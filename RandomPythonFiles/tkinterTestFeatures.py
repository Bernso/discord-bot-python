import tkinter as tk
from tkinter import ttk

class app():
    def __init__(self):
        
        
        self.root = tk.Tk()
        self.root.geometry("350x250")
        self.root.title("Test By Bernso")
        self.mainframe = tk.Frame(self.root, background = "cyan")
        self.mainframe.pack(fill = 'both', expand = True)
        
        self.text = ttk.Label(self.mainframe, text = "Bernso", background='cyan', font = ("Gang Of Three", 30))
        self.text.grid(row = 0, column = 0)
        
        
        self.set_text_field = ttk.Entry(self.mainframe)
        self.set_text_field.grid(row = 1, column = 0, pady = 10, sticky = 'NWES')
        
        set_text_button = ttk.Button(self.mainframe, text = "Change the Text", command = lambda: set_text(self))
        set_text_button.grid(row = 1, column = 1, pady = 10)
        
        colour_options = ['red', 'blue', 'green', 'cyan', 'black', 'white']
        self.set_colour_field = ttk.Combobox(self.mainframe, values = colour_options)
        self.set_colour_field.grid(row = 2, column = 0, sticky = 'NWES', pady = 10)
        
        set_colour_button = ttk.Button(self.mainframe, text = "Change the Colour", command = lambda: set_colour(self))
        set_colour_button.grid(row = 2, column = 1, pady = 10)
        
        self.reverse_text = ttk.Button(self.mainframe, text = "Reverse the Text", command = lambda: reverse(self))
        self.reverse_text.grid(row = 3, column = 0, pady = 10)
        
        exiting = ttk.Button(self.mainframe, text = "Exit", command = exit)
        exiting.grid(row = 4, column = 0, pady = 10)
        
        def reverse(self):
            newtext = self.text.cget('text')
            reversed = newtext[::-1]
            self.text.config(text = reversed)
        
        def set_colour(self):
            newcolour = self.set_colour_field.get()
            self.text.config(foreground = newcolour)
        
        def set_text(self):
            newtext = self.set_text_field.get()
            self.text.configure(text = newtext)
        
        self.root.mainloop()
        return
        
if __name__ == '__main__':
    app()
    