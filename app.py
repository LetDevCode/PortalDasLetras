from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
livros = [
    {
        "id": 1,
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "preco": "39.90"
    }
]
# Páginas públicas

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/produtos")
def produtos():
    return render_template("produtos.html", livros=livros)

# Login e cadastro

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

# Área administrativa

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/cadastrar_livro", methods=["GET", "POST"])
def cadastrar_livro():

    if request.method == "POST":

        novo_livro = {
            "id": len(livros) + 1,
            "titulo": request.form["titulo"],
            "autor": request.form["autor"],
            "preco": request.form["preco"]
        }

        livros.append(novo_livro)

        return redirect(url_for("produtos"))

    return render_template("cadastrar_livro.html")

@app.route("/editar_livro")
def editar_livro():
    return render_template("editar_livro.html")

@app.route("/excluir_livro")
def excluir_livro():
    return render_template("excluir_livro.html")

@app.route("/pesquisar_livro")
def pesquisar_livro():
    return render_template("pesquisar_livro.html")


if __name__ == "__main__":
    app.run(debug=True)