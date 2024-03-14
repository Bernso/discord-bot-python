perfectedNumber = int(input("Enter a number: "))
allnums = []
for divisor in range(1, perfectedNumber):
    if (perfectedNumber % divisor == 0):
        print(divisor)
        allnums.append(divisor)

if sum(allnums) == perfectedNumber:
    print(f"{perfectedNumber} is a perfect number")
else:
    print(f"{perfectedNumber} is not a perfect number")
input()