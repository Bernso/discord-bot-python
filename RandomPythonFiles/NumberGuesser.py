import random
user_number = int(input("Enter a number to be guessed: "))
user_range = int(input("Enter a range of numbers to be guessed (one number): "))
guesses = 1
guessed_number = 0
while user_number != guessed_number:
    print(f"Guess {guesses}")
    guessed_number = random.randint(-1, user_range)
    guesses += 1
print(f"Number found! Your number is {guessed_number}, it took {guesses} guesses")
input()