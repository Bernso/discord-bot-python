import random

#user_password = input("Enter a password to be guessed: ")
user_password = "bernso"

def pass_guess(user_password):
    pass_length = len(user_password)
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890`~!@#$%^&*()_+-=|/?.>,<:;"{[]} \\'
    guessed_password = ""
    for _ in range(0, pass_length):
        guessed_password += random.choice(chars)
    if user_password == guessed_password:
        print(f"Password found! '{guessed_password}'")
    else:
        print(f"Invalid: '{guessed_password}'")
        pass_guess(user_password)

pass_guess(user_password)