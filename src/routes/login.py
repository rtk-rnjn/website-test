import flask

from src import app, flask_login, login_manager


class User(flask_login.UserMixin):
    pass


users: dict[str, dict[str, str]] = {"email@domain.com": {"password": "p"}}


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
