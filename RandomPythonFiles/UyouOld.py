name = input("What is your name?\n")

age = int(input("How old are you?\n"))

if name.lower() == "jeff":
    print("\nYou where born in WW2")
elif name.lower() == "kacsper":
    print("\nYou where gassed in 1945 polish boi")
else:
    print("\nidk")

if age > 50:
    print("Do I have to explain?")
elif age <= 50:
    print("You are still young.")
else:
    print("Bro, how old even are you?")