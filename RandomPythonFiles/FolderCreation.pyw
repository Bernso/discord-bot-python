import os
import random

for o in range (0,10000):
    for s in range(0,64000):
        
        x = random.randint(1,6200000)

    # Variable Naming The Folder
    i = f"Beans {x}"


    # Making The Folder
    os.makedirs(i)



