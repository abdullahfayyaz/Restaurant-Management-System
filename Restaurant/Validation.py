import re


def is_valid_password(password):
    return all([
            len(password) >= 8,
            any(char.isupper() for char in password),
            any(char.islower() for char in password),
            any(char.isdigit() for char in password),
            any(char in "#$%&" for char in password)
    ])


def is_valid_username(username):
    return bool(re.match(r"^[a-zA-Z0-9_]{4,16}$", username))

