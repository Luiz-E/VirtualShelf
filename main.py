from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/<usuario>")
def inicio(usuario):
    return render_template("usuario.html", nome = usuario)

@app.route("/<usuario>/lista-de-desejos")
def lista(usuario):
    return render_template("lista.html", nome = usuario)

@app.route("/<usuario>/estante")
def estante(usuario):
    return render_template("estante.html", nome = usuario)

@app.route("/<usuario>/configuracoes")
def config(usuario):
    return render_template("config.html", nome = usuario)

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)