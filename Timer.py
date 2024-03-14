import time
timersTime = int(input("(in seconds) How long do you want the timer to be on for? "))
while timersTime > 0:
    print(f"{timersTime} seconds remaining")
    time.sleep(1)
    timersTime -= 1
print("Time up")