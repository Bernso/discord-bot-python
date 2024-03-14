import random
import os
from time import sleep

# 1 = Rock
# 2 = Paper
# 3 = Siccors

def Win():
    print("You Won!")
    question = input("Would you like to go again?\n")
    if question.lower() == "yes":
        sleep(1)
        os.system('cls')
        game()
    else:
        exit()

def Lose():
    question = input("Awww man, you lost.\n Want to try again? \n")
    if question.lower() == "yes":
        sleep(1)
        os.system('cls')
        game()
    else:
        exit()

def Draw(x):
    print(f"You both got {x}!\n Draw!")
    print("Let's go again!")
    sleep(3)
    os.system('cls')
    game()

def game():
    comp = random.randint(1,3)
    rps = input("\nRock, Paper or Siccors?\n")
    
    if (rps.lower() == "rock" and comp == 1):
        #print(f"\n\n The computer got: {comp}.")
        Draw(x = "Rock")
    
    elif (rps.lower() == "rock" and comp == 2):
        #print(f"\n\n The computer got: {comp}.")
        Lose()
    
    elif (rps.lower() == "rock" and comp == 3):
        #print(f"\n\n The computer got: {comp}.")
        Win()
        
    elif (rps.lower() == "paper" and comp == 2):
        #print(f"\n\n The computer got: {comp}.")
        Draw(x = "Paper")

    elif (rps.lower() == "paper" and comp == 1):
        #print(f"\n\n The computer got: {comp}.")
        Win()
    
    elif (rps.lower() == "paper" and comp == 3):
        #print(f"\n\n The computer got: {comp}.")
        Lose()
    
    elif (rps.lower() == "siccors" and comp == 3):
        #print(f"\n\n The computer got: {comp}.")
        Draw(x = "Siccors")
        
    elif (rps.lower() == "siccors" and comp == 1):
        #print(f"\n\n The computer got: {comp}.")
        Lose()
    
    else:
        #print(f"\n\n The computer got: {comp}.")
        Win()
                
game()
