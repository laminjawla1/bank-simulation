import csv
import json
import uuid
import bcrypt
from constants import DB


class User:
    _users = {}

    def __init__(
        self,
        first_name,
        last_name,
        username,
        password,
        balance=0,
        user_id=None,
        withdrawal_count=0,
        deposit_count=0,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = self.hashpw(password.encode(encoding="utf-8")).decode(
            encoding="utf-8"
        )
        self.balance = balance
        self.withdrawal_count = withdrawal_count
        self.deposit_count = deposit_count

        if user_id is None:
            self.user_id = str(uuid.uuid4())
        else:
            self.user_id = user_id

    @classmethod
    def all():
        return User._users

    def hashpw(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @classmethod
    def get(self, user_id):
        for _id in User._users:
            if user_id == _id:
                return User._users[user_id]
        return None

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self):
        User._users[self.user_id] = self.__dict__
        with open("users.json", "w") as file:
            json.dump(User._users, file, indent=4)

    @classmethod
    def load_users(self):
        with open("users.json") as file:
            User._users = json.load(file)

    @property
    def get_balance(self):
        return f"D{self.balance:,.2f}"

    @property
    def get_withdrawal_count(self):
        return self.withdrawal_count

    @property
    def get_deposit_count(self):
        return self.deposit_count

    def __str__(self):
        return f"User: ID: {self.user_id}, {self.get_full_name}, Balance: {self.balance:,.2f}"
