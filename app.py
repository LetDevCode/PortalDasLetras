from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template("produtos.html")

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

@app.route("/cadastrar_livro")
def cadastrar_livro():
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