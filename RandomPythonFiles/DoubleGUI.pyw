import customtkinter
import random

rates = {
    '5' : '6',
    '7' : '8'
}
print(rates["7"])
def chances():
    x = random.randint(1, 100)
    
    if 1 <= x <= 75:
        chances1.configure(text = "Common")
        print("Common")
    elif 76 <= x <= 90:
        chances1.configure(text = "Rare")
        print("Rare")
    elif x == 100:
        chances1.configure(text = "Dommy Mummy Blowjob")
        print("Ahh~")
    else:
        chances1.configure(text = "Arcane")
        print("Arcane")
    
    

def closerates():
    rates.destroy()

def openrates():
    rates.mainloop()


#System themes
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
customtkinter.set_widget_scaling(scaling_value = 1)

# Creating the resolution etc.
app = customtkinter.CTk()
app.geometry("540x420")
app.title("GUI by Bernso")
app.iconbitmap(r"C:\Users\benws\Desktop\YTDownload\Icon\Arhururan.ico")

disclamer1 = customtkinter.CTkLabel(app, text = "This is all based off of a random number generator.", font = ("Helvetica", 20, "bold"))
disclamer1.pack(padx = 20, pady = 5)

disclamer2 = customtkinter.CTkLabel(app, text = "To understand the rates see below:", font = ("Helvetica", 15))
disclamer2.pack(pady = 5, padx = 20)

opener = customtkinter.CTkButton(app, text = "Rates", command = openrates)
opener.pack(padx = 20, pady = 15)

question1 = customtkinter.CTkLabel(app, text = "Are you lucky?")
question1.pack(padx = 20, pady = 0)

randomiser = customtkinter.CTkButton(app, text = "Press me", command = chances)
randomiser.pack(padx = 20, pady = 20)

placeholder = customtkinter.CTkLabel(app, text = "You got:")
placeholder.pack(padx = 20)

chances1 = customtkinter.CTkLabel(app, text = "Result will show here")
chances1.pack(pady = 20)

exiting = customtkinter.CTkButton(app, text = "Exit", command = quit)
exiting.pack(padx = 20, pady = 20)




# Creating a second GUI
rates = customtkinter.CTk()
rates.geometry("240x230")
rates.title("Rates")
rates.iconbitmap(r"C:\Users\benws\Desktop\YTDownload\Icon\Arhururan.ico")

ratetitle = customtkinter.CTkLabel(rates, text = "Rates:")
ratetitle.pack(padx = 20, pady = 20)

rate1 = customtkinter.CTkLabel(rates, text = "Common - 75%")
rate1.pack(padx = 20)

rate2 = customtkinter.CTkLabel(rates, text = "Rare - 15%")
rate2.pack(padx = 20)

rate3 = customtkinter.CTkLabel(rates, text = "Arcane - 10%")
rate3.pack(padx = 20)

exiting = customtkinter.CTkButton(rates, text = "Go back", command = rates.destroy)
exiting.pack(padx = 20, pady = 20)






app.mainloop()