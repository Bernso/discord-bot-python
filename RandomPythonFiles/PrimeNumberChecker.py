def is_prime(number):
    if number <= 1:
        return False  
    if number <= 3:
        return True 

    if number % 2 == 0 or number % 3 == 0:
        return False  

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False  
        i += 6

    return True

number = int(input("Enter a number to check if it's prime: "))
if is_prime(number):
    print(f"{number} is a prime number.")
else:
    print(f"{number} is not a prime number.")
    