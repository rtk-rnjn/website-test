import flask
from flask import render_template, request

from src import app, flask_login, login_manager
from src.utils.tio import Tio

users: dict[str, dict[str, str]] = {"email@domain.com": {"password": "p"}}


@app.route("/")
def index() -> str:
    return render_template("index.html", title="Index")


@app.route("/resources/universal_ide")
def universal_ide():
    return render_template(template_name_or_list="ide.html", title="IDE")


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email) -> User | None:
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request) -> User | None:
    email = request.form.get("email")
    if email not in users:
        return

    user = User()
    user.id = email

    user.is_authenticated = request.form["password"] == users[email]["password"]

    return user


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return """
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               """

    email = flask.request.form["email"]
    if flask.request.form["password"] == users[email]["password"]:
        print("User Input", email, flask.request.form["password"])
        print("User Data", email, users[email]["password"])

        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for("protected"))

    return "Bad login"


@app.route("/protected")
@flask_login.login_required
def protected():
    return "Logged in as: " + flask_login.current_user.id


@app.route("/api/tio", methods=["POST"])
async def tio():
    lang = request.get_json().get("language")
    code = request.get_json().get("code")

    if not lang or not code:
        return "Invalid request", 400

    tio = Tio(lang, code)
    st: str = await tio.send()
    return {"output": st, "language": lang, "code": code}
