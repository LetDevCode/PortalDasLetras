from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "123456"
usuarios = []

# =========================
# BANCO EM MEMÓRIA (CRUD)
# =========================

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
        "titulo": "Harry Potter e a Pedra Filosofal",
        "autor": "J. K. Rowling",
        "preco": "59.90"
    },
    {
        "id": 4,
        "titulo": "O Senhor dos Anéis",
        "autor": "J. R. R. Tolkien",
        "preco": "89.90"
    },
    {
        "id": 5,
        "titulo": "1984",
        "autor": "George Orwell",
        "preco": "44.90"
    },
    {
        "id": 6,
        "titulo": "A Revolução dos Bichos",
        "autor": "George Orwell",
        "preco": "34.90"
    },
    {
        "id": 7,
        "titulo": "Orgulho e Preconceito",
        "autor": "Jane Austen",
        "preco": "49.90"
    },
    {
        "id": 8,
        "titulo": "Percy Jackson e o Ladrão de Raios",
        "autor": "Rick Riordan",
        "preco": "54.90"
    },
    {
        "id": 9,
        "titulo": "A Culpa é das Estrelas",
        "autor": "John Green",
        "preco": "39.90"
    },
    {
        "id": 10,
        "titulo": "Jogos Vorazes",
        "autor": "Suzanne Collins",
        "preco": "59.90"
    },
    {
        "id": 11,
        "titulo": "O Hobbit",
        "autor": "J. R. R. Tolkien",
        "preco": "64.90"
    },
    {
        "id": 12,
        "titulo": "Cem Anos de Solidão",
        "autor": "Gabriel García Márquez",
        "preco": "69.90"
    },
    {
        "id": 13,
        "titulo": "A Menina que Roubava Livros",
        "autor": "Markus Zusak",
        "preco": "49.90"
    },
    {
        "id": 14,
        "titulo": "O Código Da Vinci",
        "autor": "Dan Brown",
        "preco": "54.90"
    },
    {
        "id": 15,
        "titulo": "Crepúsculo",
        "autor": "Stephenie Meyer",
        "preco": "39.90"
    },
    {
        "id": 16,
        "titulo": "As Crônicas de Nárnia",
        "autor": "C. S. Lewis",
        "preco": "79.90"
    },
    {
        "id": 17,
        "titulo": "Memórias Póstumas de Brás Cubas",
        "autor": "Machado de Assis",
        "preco": "42.90"
    },
    {
        "id": 18,
        "titulo": "Capitães da Areia",
        "autor": "Jorge Amado",
        "preco": "36.90"
    },
    {
        "id": 19,
        "titulo": "O Alquimista",
        "autor": "Paulo Coelho",
        "preco": "45.90"
    },
    {
        "id": 20,
        "titulo": "Verity",
        "autor": "Colleen Hoover",
        "preco": "57.90"
    },
    {
        "id": 21,
        "titulo": "É Assim que Acaba",
        "autor": "Colleen Hoover",
        "preco": "52.90"
    },
    {
        "id": 22,
        "titulo": "A Biblioteca da Meia-Noite",
        "autor": "Matt Haig",
        "preco": "56.90"
    },
    {
        "id": 23,
        "titulo": "O Nome do Vento",
        "autor": "Patrick Rothfuss",
        "preco": "74.90"
    },
    {
        "id": 24,
        "titulo": "Duna",
        "autor": "Frank Herbert",
        "preco": "84.90"
    },
    {
        "id": 25,
        "titulo": "A Rainha Vermelha",
        "autor": "Victoria Aveyard",
        "preco": "47.90"
    }
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

        email = request.form["email"]
        senha = request.form["senha"]

        for usuario in usuarios:

            if usuario["email"] == email and usuario["senha"] == senha:

                session["usuario"] = usuario["nome"]

                return redirect(url_for("admin"))

        return render_template(
            "login.html",
            erro="E-mail ou senha inválidos."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))


# =========================
# CADASTRO (SÓ VISUAL)
# =========================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar = request.form["confirmar"]

        # verifica se as senhas são iguais
        if senha != confirmar:
            return render_template(
                "cadastro.html",
                erro="As senhas não coincidem."
            )

        # verifica se email já existe
        for usuario in usuarios:
            if usuario["email"] == email:
                return render_template(
                    "cadastro.html",
                    erro="Este e-mail já está cadastrado."
                )

        # cadastra usuário
        usuarios.append({
            "nome": nome,
            "email": email,
            "senha": senha
        })
         
        
        return redirect(url_for("login"))

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