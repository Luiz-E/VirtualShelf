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
    _id = db.Column("id", db.Integer, primary_key=True)
    nome = db.Column("name", db.String(100))
    email = db.Column(db.String(100))
    senha = db.column(db.String(50))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

@app.route("/")
def home():
    return redirect(url_for("user", usr="guest"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["login"]
        found_user = users.query.filter_by(nome=user).first()
        if found_user:
            session["user"] = user
            return redirect(url_for("user"))
        else:
            return "Usuário Não Encontrado"
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/cadastro", methods=["POST", "GET"])
def cadastrar():
    if request.method == "POST":
        userName = request.form["nome"]
        userEmail = request.form["email"]
        userSenha = request.form["senha"]
        found_user = users.query.filter_by(nome = userName ).first()
        if found_user:
            session["user"] = userName
            return redirect(url_for("user"))
        else:
            usr = users(userName, userEmail, userSenha)
            db.session.add(usr)
            db.session.commit()
            return redirect(url_for("login"))
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

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/delete_all")
def delete_all():
    usersToBeDeleted = users.query.all()
    for user in usersToBeDeleted:
        users.query.filter_by(nome = user.nome).delete()
    db.session.commit()
    return redirect(url_for("login"))

@app.route("/delete_user/")
def delete():
    userToBeDeleted = session["user"]
    users.query.filter_by(nome = userToBeDeleted).delete()
    db.session.commit()
    session.pop("user", None)
    return redirect(url_for("cadastrar"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug="True")

