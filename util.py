import os
import json
from datetime import datetime


def clear():
    os.system("clear")


def add_to_ledger(
    entry_id, username, debit, credit, balance, date=datetime.utcnow().isoformat()
):
    with open("ledger.json", "a") as ledger:
        json.dump(
            {
                "entry_id": entry_id,
                "username": username,
                "debit": debit,
                "credit": credit,
                "balance": balance,
                "date": date,
            },
            ledger,
        )
