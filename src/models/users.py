from __future__ import annotations

from flask import Request
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src import login_manager, mongo_client as mongo


@login_manager.user_loader
def load_user(email: str) -> User | None:
    db = mongo["users_database"]
    entity = db.users.find_one(
        {
            "$or": [
                {"email": email},
                {"username": email},
            ],
        },
    )

    if entity is None:
        return None

    user = User(entity)
    user.email = entity["email"]
    user.password_hash = entity["password_hash"]

    return user


@login_manager.request_loader
def request_loader(request: Request) -> User | None:
    email = request.form.get("email")
    if email is None:
        return None

    entity = mongo.users_database.users.find_one({"email": email})

    if entity is None:
        return None

    user = User(entity)

    return user if user.check_password(request.form["password"]) else None


class User(UserMixin):
    def __init__(self, entity: dict) -> None:
        for key, value in entity.items():
            setattr(self, key, value)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def set_password(self, new_password: str) -> None:
        self.password_hash = generate_password_hash(new_password)

    def get_id(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __hash__(self) -> int:
        return hash(self.email)
