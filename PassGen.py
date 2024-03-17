import random
def main():
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    specialchars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890`~!@#$%^&*()_+-=|/?.>,<:;"{[]} ''\\'
    print("Default charcter length is 16.\n")
    pass_length = 16 #int(input("How long do you want your password to be? "))

    print("Your passwords are: \n")
    random_password = ""
    for _ in range(0, int(pass_length)):
        random_password += random.choice(specialchars)
    print(f"With special characters: {random_password}")
    
    random_password = ""
    for _ in range(0, int(pass_length)):
        random_password += random.choice(chars)
    print(f"Without special charcters: {random_password}")

main()
