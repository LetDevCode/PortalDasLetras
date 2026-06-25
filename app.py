from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

livros = [
    {
        "id": 1,
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "preco": "39.90"
    },
    {
        "id": 2,
        "titulo": "O Pequeno Príncipe",
        "autor": "Antoine de Saint-Exupéry",
        "preco": "29.90"
    },
    {
        "id": 3,
        "titulo": "Harry Potter",
        "autor": "J. K. Rowling",
        "preco": "59.90"
    }
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@app.route("/produtos")
def produtos():
    return render_template("produtos.html", livros=livros)


@app.route("/admin")
def admin():
    return render_template("admin.html", livros=livros)


@app.route("/cadastrar_livro", methods=["GET", "POST"])
def cadastrar_livro():

    if request.method == "POST":

        livro = {
            "id": len(livros) + 1,
            "titulo": request.form["titulo"],
            "autor": request.form["autor"],
            "preco": request.form["preco"]
        }

        livros.append(livro)

        return redirect(url_for("admin"))

    return render_template("cadastrar_livro.html")


@app.route("/pesquisar_livro", methods=["GET", "POST"])
def pesquisar_livro():

    resultado = livros

    if request.method == "POST":

        busca = request.form["busca"].lower()

        resultado = [
            livro for livro in livros
            if busca in livro["titulo"].lower()
        ]

    return render_template(
        "pesquisar_livro.html",
        resultado=resultado
    )


@app.route("/excluir_livro/<int:id>")
def excluir_livro(id):

    global livros

    livros = [livro for livro in livros if livro["id"] != id]

    return redirect(url_for("admin"))


@app.route("/editar_livro/<int:id>", methods=["GET", "POST"])
def editar_livro(id):

    livro = next((l for l in livros if l["id"] == id), None)

    if livro is None:
        return redirect(url_for("admin"))

    if request.method == "POST":

        livro["titulo"] = request.form["titulo"]
        livro["autor"] = request.form["autor"]
        livro["preco"] = request.form["preco"]

        return redirect(url_for("admin"))

    return render_template(
        "editar_livro.html",
        livro=livro
    )


if __name__ == "__main__":
    app.run(debug=True)