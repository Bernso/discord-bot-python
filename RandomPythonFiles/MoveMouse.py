import pyautogui
import random

timesMoved = 1

print("Press enter to Move your mouse to a random position on your screen:")
print("Type 'close' to close the aplicaiton.")
input()


while True:
    x = random.randint(0, 1081)
    y = random.randint(0, 921)
    pyautogui.moveTo(x, y, 0.05)
    print(f"Mouse moved {timesMoved} times.")
    userChoice = input()
    if userChoice.lower() == "close":
        quit()
    else:
        pass
    timesMoved +=1