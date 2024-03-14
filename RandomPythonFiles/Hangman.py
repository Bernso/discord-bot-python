import getpass
import random
import os
import time


def guess(word, user_lives):
    if word == []:
        os.system('cls')
        print("You win!")
        input()
        quit()
    else:
        pass
    
    user_input = input("\nWhats your guess? ")
    
    if user_input in word:
        print("Letter in word!")
        word.remove(user_input)
        #print(word)
        
    else:
        if len(user_lives) == 1:
            print("Letter not in word")
            user_lives.remove(user_lives[0])
            print(f"You have {len(user_lives)} lives left")  
        else:
            print("Letter not in word")
            user_lives.remove(user_lives[0])
            print(f"You have {len(user_lives)} lives left")

def main():
    chars = 'qwertyuiopasdfghjklzxcvbnm'

    os.system('cls')
    user_name = input("Enter your name: ")
    os.system('cls')
    
    print(f"Hello, {user_name}")
    print("Welcome to Hangman\n")
    print("You have 10 lives")
    print("No uppercase allowed\n")
    print("(Words will always be in lowercase)")
    print("(Duplicate letters will have to be entered individually)")
    print("(The random word's length can range from 3 to 8 letters long)")
    print("(You have to type in the spaces if the it is longer than a word)")
    print("(It will tell you if the phrase you have to guess is longer than one word)")
    print()
    
    
    user_lives = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    user_input = input("Random word or not? (y/n) ")
    words = ['bean', 'potato', 'fire', 'gun', 'car', 'football', 'running' 'monkey', 'ice', 'pizza']
    
    if user_input.lower() == "y":
        user_input2 = input("An actual word or random letters? ")
        
        if user_input2.lower() == 'random letters':
            word = []
            
            for i in range(1, 5):
                word.append(random.choice(chars))
        
        elif user_input2.lower() == 'actual word':
            word = list(random.choice(words))
        else:
            os.system('cls')
            print("Please enter a valid option.")
            time.sleep(1)
            main()
    else:
        def user_word():
            
            word = [getpass.getpass("Enter a word: ")]
            word = list(word[0])
            
            
            for x in range(0, len(word)):
                if word[x] != word[x].lower():
                    os.system('cls')
                    print("No uppercase allowed")
                    time.sleep(1)
                    main()
                else:
                    pass
                
            return word
        
        
        word = user_word()
    os.system('cls')    
    print(f"\nThe word is {len(word)} charcters long.")
    if ' ' in list(word):
        print("It is two or more words long")
    
    while user_lives != []:
        guess(word, user_lives)
    os.system('cls')
    print("You lost")
    print(f"\nThe remaining letters were: {list(word)}")
    

if __name__ == "__main__":
    main()
    input()
    quit()