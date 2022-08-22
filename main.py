from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("user", usr="guest"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
         user = request.form["nm"]
         return redirect(url_for("user",usr=user))
    else:
        return render_template("login.html")

@app.route("/cadastro", methods=["POST", "GET"])
def cadastrar():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("cadastro.html")


@app.route("/<usr>")
def user(usr):
    return render_template("usuario.html", usr=usr)

@app.route("/<usr>/lista")
def lista(usr):
    return render_template("lista.html", usr=usr)

if __name__ == "__main__":
    app.run(debug="True")