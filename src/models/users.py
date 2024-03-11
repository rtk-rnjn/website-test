from __future__ import annotations

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src import app, login_manager


def _return_admin(email: str) -> User | None:
    if email == "admin@admin.com":
        user = User()
        user.email = email
        user.is_admin = True

        return user


@login_manager.user_loader
def load_user(email: str) -> User | None:
    admin = _return_admin(email)
    if admin is not None:
        return admin

    db = app.mongo["users_database"]
    entity = db.users.find_one({"email": email})

    if entity is None:
        return None

    user = User()
    user.email = entity["email"]
    user.password_hash = entity["password_hash"]

    return user


@login_manager.request_loader
def request_loader(request) -> User | None:
    email = request.form.get("email")
    admin = _return_admin(email)
    if admin is not None:
        return admin

    db = app.mongo["users_database"]
    entity = db.users.find_one({"email": email})

    if entity is None:
        return None

    user = User()
    user.email = entity["email"]
    user.password_hash = entity["password_hash"]

    if not user.check_password(request.form["password"]):
        return None

    return user


class User(UserMixin):
    email: str
    password_hash: str

    is_admin = False

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def set_password(self, new_password: str) -> None:
        self.password_hash = generate_password_hash(new_password)

    def get_id(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __eq__(self, other: User) -> bool:
        return self.email == other.email

    def __hash__(self) -> int:
        return hash(self.email)
