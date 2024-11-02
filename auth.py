import csv
import bcrypt
from user import User
from util import clear
from constants import DB


def authenticate(username, password):
    for uid, user in User._users.items():
        u_name = user.get("username")
        p_word = user.get("password")

        if u_name == username and password_correct(
            password.encode(encoding="utf-8"), p_word.encode(encoding="utf-8")
        ):
            return User(
                user_id=uid,
                username=user.get("username"),
                password=password,
                first_name=user.get("first_name"),
                last_name=user.get("last_name"),
                balance=user.get("balance"),
                withdrawal_count=user.get("withdrawal_count"),
                deposit_count=user.get("deposit_count"),
            )


def register(first_name, last_name, username, password):
    if usernameExists(username):
        clear()
        print("Username taken")
        return False
    user = User(
        first_name=first_name, last_name=last_name, username=username, password=password
    )
    user.save()

    clear()
    return True


def usernameExists(username):
    for user_id, user in User._users.items():
        if user.get("username") == username:
            return True
    return False


def password_correct(password, hashed):
    return bcrypt.checkpw(password, hashed)
