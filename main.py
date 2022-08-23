from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=10)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer)


@app.route("/")
def home():
    return redirect(url_for("user", usr="guest"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/cadastro", methods=["POST", "GET"])
def cadastrar():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("cadastro.html")


@app.route("/user")
def user():
    if "user" in session:
        return render_template("usuario.html")
    else:
        return redirect(url_for("login"))


@app.route("/user/lista")
def lista():
    return render_template("lista.html")


@app.route("/user/estante")
def estante():
    return render_template("estante.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug="True")
