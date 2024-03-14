from time import sleep
from itertools import cycle
from os import system
system('cls')


colours = [
    ('Green', 2),
    ('Yellow', 0.5),
    ('Red', 2)
]


colours2 = cycle(colours)
while True:
    c, s = next(colours2)
    print(c)
    sleep(s)
    system('cls')