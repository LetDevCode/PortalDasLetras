from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "123456"

# =========================
# BANCO EM MEMÓRIA (CRUD)
# =========================

livros = [
    {"id": 1, "titulo": "Dom Casmurro", "autor": "Machado de Assis", "preco": "39.90"},
    {"id": 2, "titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "preco": "29.90"},
    {"id": 3, "titulo": "Harry Potter", "autor": "J. K. Rowling", "preco": "59.90"}
]

# =========================
# PÁGINAS PRINCIPAIS
# =========================

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


# =========================
# LOGIN / LOGOUT
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        # login simples (para trabalho)
        if email and senha:
            session["usuario"] = email
            return redirect(url_for("admin"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))


# =========================
# CADASTRO (SÓ VISUAL)
# =========================

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


# =========================
# ADMIN (PROTEGIDO)
# =========================

@app.route("/admin")
def admin():

    if "usuario" not in session:
        return redirect(url_for("login"))

    total = len(livros)

    valor_medio = (
        sum(float(l["preco"]) for l in livros) / total
        if total > 0 else 0
    )

    livro_caro = (
        max(livros, key=lambda x: float(x["preco"]))
        if livros else None
    )

    livro_barato = (
        min(livros, key=lambda x: float(x["preco"]))
        if livros else None
    )

    valor_total = sum(
        float(l["preco"])
        for l in livros
    )

    return render_template(
        "admin.html",
        usuario=session["usuario"],
        livros=livros,
        total=total,
        valor_medio=valor_medio,
        livro_caro=livro_caro,
        livro_barato=livro_barato,
        valor_total=valor_total
    )


# =========================
# CRUD - CADASTRAR
# =========================

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

        return redirect(url_for("admin"))

    return render_template("cadastrar_livro.html")


# =========================
# CRUD - PESQUISAR
# =========================

@app.route("/pesquisar_livro", methods=["GET", "POST"])
def pesquisar_livro():

    resultado = livros

    if request.method == "POST":
        busca = request.form.get("busca", "").lower()

        resultado = [
            livro for livro in livros
            if busca in livro["titulo"].lower()
        ]

    return render_template("pesquisar_livro.html", resultado=resultado)


# =========================
# CRUD - EXCLUIR
# =========================

@app.route("/excluir_livro/<int:id>")
def excluir_livro(id):

    global livros
    livros = [livro for livro in livros if livro["id"] != id]

    return redirect(url_for("admin"))


# =========================
# CRUD - EDITAR
# =========================

@app.route("/editar_livro/<int:id>", methods=["GET", "POST"])
def editar_livro(id):

    livro = next((l for l in livros if l["id"] == id), None)

    if not livro:
        return redirect(url_for("admin"))

    if request.method == "POST":

        livro["titulo"] = request.form["titulo"]
        livro["autor"] = request.form["autor"]
        livro["preco"] = request.form["preco"]

        return redirect(url_for("admin"))

    return render_template("editar_livro.html", livro=livro)


# =========================
# START APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)