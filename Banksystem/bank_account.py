import csv
import random


def main_menu():

    print("\n=====================================")
    print("Welcome to the bank of Python!")
    print("=====================================")

    while True:
        try:
            choose = int(input("Please choose what you want to do: \n1. Create Account\n2. Login\n3. Exit\n"))
            if choose not in [1, 2, 3]:
                raise ValueError
            return choose
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
                return True
            else:
                print("Invalid PIN. Please try again.")
                continue

        except ValueError:
            print("Please enter a valid PIN")
            continue
        

    
def account_menu():
    pass




def process():
    while True:
        choice = main_menu()
        if choice == 1:
            create_account()
        elif choice == 2:
            login()
            print("Login successful!")
            break
        elif choice == 3:
            print("Thank you for using the bank of Python!")
            exit()
        else:
            print("Please enter a valid option")
            main_menu()

if __name__ == "__main__":
    process()
