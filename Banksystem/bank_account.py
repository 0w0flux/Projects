import csv
import random


def main_menu():

    print("\n=====================================")
    print("Welcome to the bank of Python!")
    print("=====================================")

    while True:
        try:
            choice = int(input("Please choose what you want to do: \n1. Create Account\n2. Login\n3. Exit\n"))
            if choice not in [1, 2, 3]:
                raise ValueError
            return choice
        except ValueError:
            print("Please enter a valid option\n")

file_path = "Banksystem/bank_accounts.csv"

def load_accounts():
    accounts = [] # List of tuples (account_number, pin, balance) puts all the accounts in a list
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)

        for row in reader:
            account_number = int(row[0]) # set the account number to the first value in the row
            pin = int(row[1])
            balance = float(row[2])
            accounts.append((account_number, pin, balance)) # Appends the values to the accounts list to check if the account number already exists
    return accounts

def create_account():
    accounts = load_accounts()

    while True:
        account_number = random.randint(100, 999)
        print(f"\nYour account number is: {account_number}")  

        if any(account[0] == account_number for account in accounts): # Checks if the account number already exists
            print("Account number already exists. Please try again.")      

        try:
            pin = input("Enter your PIN (4 digits): ")
            if len(pin) != 4 or not pin.isdigit():
                raise ValueError
            break
        except ValueError:
            print("PIN must be 4 digits.")

        accounts.append([account_number, int(pin), 0.0]) # Appends the account number, pin and balance to the accounts list
        

    with open(file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=";") 
        writer.writerow([account_number, int(pin), 0.0]) # Writes the account number, pin and balance to the csv file

    print("Account created successfully!\n")
    process()

def login():

    accounts = load_accounts()
    
    while True:
        try:
            account_number = int(input("Please enter your Account Number: "))
            if any(account[0] == account_number for account in accounts):
                if account_number == 0:
                    raise ValueError("Please enter a valid account number")
                break # Breaks the loop if the account number is valid
            else:
                print("Account number does not exist. Please try again.")
                continue # Continues the loop if the account number does not exist

        except ValueError:
            print("Please enter a valid account number")
    
    while True:
        try:
            pin = input("Please enter your PIN: ")

            if len(pin) != 4 or not pin.isdigit():
                raise ValueError("PIN must be 4 digits")
            pin = int(pin)
    
            if any(account[0] == account_number and account[1] == pin for account in accounts):
                return account_number
            else:
                print("Invalid PIN. Please try again.")
                continue

        except ValueError:
            print("Please enter a valid PIN")
            continue
            
def account_menu(account_number):

    while True:
        try:
            choice = int(input("\nPlease choose what you want to do: \n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Logout\n5. Close Account\n"))
            if choice not in [1, 2, 3, 4, 5]:
                raise ValueError
            if choice == 1:
                check_balance(account_number)
            elif choice == 2:
                deposit(account_number)
            elif choice == 3:
                withdraw(account_number)
            elif choice == 4:
                print("Logged out successfully!")
                process()
            elif choice == 5:
                close_account(account_number)
                print("Account closed successfully!")
                process()
        except ValueError:
            print("Please enter a valid option")

def check_balance(account_number):
    accounts = load_accounts()
    for account in accounts:
        if account[0] == account_number:
            print(f"\nYour balance is: {account[2]:.2f}")
            break

def deposit(account_number):
    accounts = load_accounts()
    amount = float(input("Enter the amount you want to deposit: "))

    updated_accounts = []

    for account in accounts:
        if account[0] == account_number:
            new_balance = account[2] + amount
            updated_accounts.append([account[0], account[1], new_balance])
            print(f"\nDeposited {amount:.2f} successfully!")
        else:
            updated_accounts.append(account)

    with open(file_path, "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["account_number", "pin", "balance"])
        writer.writerows(updated_accounts)

def withdraw(account_number):
    accounts = load_accounts()
    amount = float(input("Enter the amount you want to withdraw: "))

    updated_accounts = []

    for account in accounts:
        if account[0] == account_number:
            if account[2] < amount:
                print("Insufficient funds.")
            else:
                new_balance = account[2] - amount
                updated_accounts.append([account[0], account[1], new_balance])
                print(f"\nWithdrew {amount:.2f} successfully!")

    with open(file_path, "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["account_number", "pin", "balance"])
        writer.writerows(updated_accounts)

def close_account(account_number):

    accounts = load_accounts()
    account_to_close = None

    for account in accounts:
        if account[0] == account_number:
            account_to_close = account
            break

    if not account_to_close:
        print("Account not found")
        return
    
    try:
        verify = int(input("To close your account, please enter your PIN: "))
        if verify == account_to_close[1]:
            print("Account closed successfully!")
        else:
            print("Invalid PIN. Please try again.")
            return
        
    except ValueError:
        print("Please enter a valid PIN")

    updated_accounts = [account for account in accounts if account[0] != account_number]

    with open(file_path, "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["account_number", "pin", "balance"])
        writer.writerows(updated_accounts)

def process():
    while True:
        choice = main_menu()
        if choice == 1:
            create_account()
        elif choice == 2:
            account_number = login()
            if account_number:
                print("Login successful!")
                account_menu(account_number)
                break
        elif choice == 3:
            print("Thank you for using the bank of Python!")
            exit()
        else:
            print("Please enter a valid option")
            main_menu()

if __name__ == "__main__":
    process()
