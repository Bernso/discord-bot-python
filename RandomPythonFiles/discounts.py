import random


discount = int(input("Enter a discount: " ))
price = int(input("Enter the price for the product that you are buying: £"))

discount /= 100
discount -= 1
discount *= -1
price2 = price * discount 

question1 = input(f"Is this the price you where expecting once the discount had been applied?\n £{price2}\n")
if question1.lower() == "yes":
    print("Ok then no more trouble for me!")
    print(f"Your new price with the discount is: £{price2}\n")
else:
    print("Oh, so your are a money hungry business man?")
    price2 = random.randint(5673489234,3648723648723684)
    input(f"Does this number sound better for you? £{price2}\n")
    print("Sad.")



input()