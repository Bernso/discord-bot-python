import random
def main():
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890`~!@#$%^&*()_+-=|/?.>,<:;"{[]} \\'

    print("Must be an intiger.")
    pass_length = int(input("How long do you want your password to be? "))

    
    random_password = ""
    for _ in range(0, int(pass_length)):
        random_password += random.choice(chars)
    print(f"Your password is: {random_password}")

main()
input()