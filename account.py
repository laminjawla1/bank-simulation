import time
import json
from uuid import uuid4
from datetime import datetime
from util import clear, add_to_ledger


class Ledger:
    ledger = {}

    def __init__(
        self, username, debit="", credit="", balance=0.0, date=None, entry_id=None
    ):
        self.username = username
        self.debit = debit
        self.credit = credit
        self.balance = balance
        self.entry_id = entry_id or str(uuid4())
        self.date = datetime.utcnow() if date is None else datetime.fromisoformat(date)

    def save(self):
        """Save the current entry to the ledger dictionary."""
        Ledger.ledger[self.entry_id] = self.to_dict()

    @classmethod
    def commit(cls):
        """Write all ledger entries to the JSON file."""
        with open("ledger.json", "w") as file:
            json.dump(cls.ledger, file, indent=4)

    def to_dict(self):
        """Convert ledger entry to a dictionary format."""
        dictionary = self.__dict__.copy()
        dictionary["date"] = self.date.isoformat()
        return dictionary


def deposit(user, amount):
    """Handles deposit transactions for the user."""
    user.balance += amount
    user.deposit_count += 1
    user.save()
    print(
        f"Account credited with: D{amount:,.2f}\nCurrent balance is: {user.get_balance}\n"
    )
    Ledger(username=user.username, credit=amount, balance=user.balance).save()
    Ledger.commit()
    time.sleep(2)


def withdraw(user, amount):
    """Handles withdrawal transactions for the user."""
    if user.balance < amount:
        print("Insufficient funds to withdraw\n")
    else:
        user.balance -= amount
        user.withdrawal_count += 1
        user.save()
        print(
            f"Account debited with: D{amount:,.2f}\nCurrent balance is: {user.get_balance}\n"
        )
        Ledger(username=user.username, debit=amount, balance=user.balance).save()
        Ledger.commit()
        time.sleep(2)


def load_ledger(user):
    """Loads ledger entries from a JSON file, filtering by user if necessary."""
    try:
        with open("ledger.json") as file:
            entries = json.load(file)
            Ledger.ledger.clear()  # Clear any existing ledger entries to avoid duplication.
            for entry_id, entry_data in entries.items():
                if entry_data["username"] == user.username:
                    entry = Ledger(
                        entry_id=entry_id,
                        username=entry_data["username"],
                        debit=entry_data.get("debit"),
                        credit=entry_data.get("credit"),
                        balance=entry_data["balance"],
                        date=entry_data["date"]
                    )
                    entry.save()
            Ledger.commit()
    except (FileNotFoundError, json.JSONDecodeError):
        print("No ledger data found or file is corrupt.")
