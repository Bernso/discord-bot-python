import random
import os

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLUMNS = 3

SymbolCount = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

SymbolValue = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def checkWinnings(columns, lines, bet, values):
    winnings = 0
    winningLines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbolToCheck = column[line]
            if symbol != symbolToCheck:
                break
        else:
            winnings += values[symbol] * bet
            winningLines.append(line + 1)
    return winnings, winningLines

            

def getSoltMachineSpin(rows, cols, Symbols):
    allSymbols = []
    for symbol, SymbolCount in Symbols.items():
        for _ in range(SymbolCount):
            allSymbols.append(symbol)
    columns = []
    for _ in range(cols):
        column = []
        currentSymbols = allSymbols[:]
        for _ in range(rows):
            value = random.choice(currentSymbols)
            currentSymbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def printSlotMachine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) -1:
                print(column[row], end = " | ")
            else:
                print(column[row], end = "")
        print()
    

def deposit():
    while True:
        amount = input("How much would you like to deposit? £")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than £0")
        else:
            print("Please enter a number next time.")
    return amount


def GetNumberOfLines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES} lines): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(f"Number of lines must be greater than 0 and less than {MAX_LINES}.")
        else:
            print("Please enter a number next time.")
    return lines

def get_bet():
    while True:
        bet = input("How much would you like to bet on each line? ")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(f"Your bet must be between £{MIN_BET} and £{MAX_BET}")
        else:
            print("Please enter a number next time.")
    return bet

def main():
    balence = deposit()
    lines = GetNumberOfLines()
    
    
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balence:
            print(f"You do not have enough to bet that amount, your current balence is {balence}.")
        else:
            break
    
    
    print(f"You are betting £{bet} on {lines} lines. Your total bet is £{total_bet}")
    
    slots = getSoltMachineSpin(ROWS, COLUMNS, SymbolCount)
    printSlotMachine(slots)
    
    winnings = checkWinnings(slots, lines, bet, SymbolValue)
    print(f"You won £{winnings}!")
    q = input("Would you like to play again? ")
    if q.lower() == "yes":
        print("\n")
        main()
    else:
        os.system('cls')
        print("Bye, Bye")
        quit()
        
    
main()