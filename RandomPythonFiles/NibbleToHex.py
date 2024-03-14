

def nibbleToHex(binary):
    hextobinarydictionary = {
        "0000"  : '0',
        "0001"  : '1',
        "0010"  : '2',
        "0011"  : '3',
        "0100"  : '4',
        "0101"  : '5',
        "0110"  : '6',
        "0111"  : '7',
        "1000"  : '8',
        "1001"  : '9',
        "1010"  : 'A',
        "1011"  : 'B',
        "1100"  : 'C',
        "1101"  : 'D',
        "1110"  : 'E',
        "1111"  : 'F'
    }
    
    hexString = ''
    for length in range(0, len(binary), 4):
        nibble = binary[length:length+4]
        hexString += hextobinarydictionary[nibble]
    
    return hexString




def singularValueFunction(value):
    if ((value == 1) or (value == 0)):
        return str(value)
    else:
        print("Invalid\nRestarting...\n")
        return singularValueFunction(int(input("Enter a number: ")))


def user_input():
    binaryString = ""
    numberOfNumbers = int(input("How many numbers would you like in your string? "))
    if numberOfNumbers % 4 == 0:
        print("Valid string")
    else:
        print("Invalid string\nRestaring...\n")
        user_input()
    print("Input must be 1 or 0")
    for _ in range(0, numberOfNumbers):
        SingularValue = int(input("Enter a number: "))
        binaryString += singularValueFunction(SingularValue)
        print(f"The current values: {binaryString}")
        
        
    print(f"\nThe final value is: {nibbleToHex(binaryString)}")
    


user_input()