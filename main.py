import time
import sys
from util import clear
from user import User
from getpass import getpass
from datetime import datetime
from auth import authenticate, register
from account import load_ledger, deposit, withdraw, Ledger


def main():
    User.load_users()
    clear()
    while True:
        print("########## WELCOME TO YOUR BANK ##########")
        print("1. LOGIN\n2. REGISTER\n0. Quit")
        choice = int(input("Choose: "))

        match choice:
            case 1:
                clear()
                print("########## LOGIN ##########")

                username = input("Username: ")
                password = getpass("Password: ")

                user = authenticate(username, password)
                if user is not None:
                    load_ledger(user)
                    bank(user)

                clear()
                print("Invalid credentials")
                time.sleep(1.5)
            case 2:
                clear()
                print("########## REGISTER ##########")

                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                username = input("Username: ")
                password = getpass("Password: ")

                if register(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                ):
                    print("Registeration successfully completed")
                else:
                    print("Registration failed")
            case 0:
                clear()
                print("Program quitting...")
                sys.exit(0)
            case _:
                clear()
                print("Invalid command")


def bank(user):
    clear()
    while True:
        print("WELCOME, %s.\n" % user.get_full_name.upper())
        print("1.DASHBOARD\n2.DEPOSIT\n3.WITHDRAW\n4.LEDGER\n5.LOGOUT")
        choice = int(input("\nChoose: "))

        match choice:
            case 1:
                dashboard(user)
            case 2:
                clear()
                print("########## DEPOSIT #########")
                amount = float(input("Amount: "))
                deposit(user, amount)
            case 3:
                clear()
                print("########## WITHDRAW #########")
                print(f"Balance: %s" % user.get_balance)
                amount = float(input("Amount: "))
                withdraw(user, amount)
            case 4:
                ledger(user)
            case 5:
                clear()
                print("Logged out successfully")
                sys.exit(0)
            case _:
                clear("Invalid Command")


def dashboard(user):
    clear()
    print("===========================")
    print(f"CLIENT: {user.get_full_name}")
    print(f"ACCOUNT BALANCE: {user.get_balance}")
    print("---------------------------")
    print(f"DEPOSITS: {user.get_deposit_count}")
    print(f"WITHDRAWALS: {user.get_withdrawal_count}")
    print("===========================\n")


def ledger(user):
    clear()
    # Filter ledger entries to include only those for the specified user
    entries = {
        entry_id: entry
        for entry_id, entry in Ledger.ledger.items()
        if entry["username"] == user.username
    }
    # Sort entries by date, parsing date strings to datetime objects for comparison
    sorted_entries = dict(
        sorted(
            entries.items(),
            key=lambda item: datetime.fromisoformat(item[1]["date"]),
            reverse=True
        )
    )
    
    print("LEDGER".center(40))
    print(f'{"DEBIT":<15}{"CREDIT":<15}{"BALANCE"}')
    print("---------------------------------------------")
    for entry_id, entry in sorted_entries.items():
        if entry.get("debit") == "":
            print(
                f'{"-":<15}D{entry.get("credit"):<15,.2f}D{entry.get("balance"):,.2f}'
            )
        else:
            print(f'D{entry.get("debit"):<15,.2f}{"-":<15}D{entry.get("balance"):,.2f}')
        print("---------------------------------------------")


if __name__ == "__main__":
    main()
