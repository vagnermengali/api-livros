from flask import Flask, jsonify, render_template, request
import sqlite3
import re

app = Flask(__name__)


def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS LIVROS(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     titulo TEXT NOT NULL,
                     categoria TEXT NOT NULL,
                     autor TEXT NOT NULL,
                     imagem_url TEXT NOT NULL
                     );
        """)


@app.before_request
def before_first_request():
    init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/doar", methods=["POST"])
def doar():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi fornecido"}), 400

    campos_obrigatorios = ["titulo", "categoria", "autor", "imagem_url"]

    campos_faltantes = [
        campo
        for campo in campos_obrigatorios
        if not dados.get(campo) or not str(dados.get(campo)).strip()
    ]

    if campos_faltantes:
        return jsonify(
            {
                "erro": "Campos obrigatórios não fornecidos ou estão vazios",
                "campos_faltantes": campos_faltantes,
            }
        ), 400

    titulo = dados["titulo"].strip()
    categoria = dados["categoria"].strip()
    autor = dados["autor"].strip()
    imagem_url = dados["imagem_url"].strip()

    if not re.match(r"^https?://[^\s]+$", imagem_url):
        return jsonify({"erro": "URL da imagem inválida"}), 400

    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
                           VALUES (?,?,?,?)
""",
                (titulo, categoria, autor, imagem_url),
            )
            conn.commit()
        return jsonify(
            {
                "mensagem": "Livro cadastrado com sucesso",
                "livro": {
                    "titulo": titulo,
                    "categoria": categoria,
                    "autor": autor,
                    "imagem_url": imagem_url,
                },
            }
        ), 201

    except sqlite3.Error as e:
        return jsonify({"erro": "Erro ao cadastrar livro", "detalhe": str(e)}), 500


@app.route("/livros", methods=["GET"])
def listar_livros():
    try:
        with sqlite3.connect("database.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, titulo, categoria, autor, imagem_url
                FROM LIVROS
            """)
            livros = cursor.fetchall()
    except sqlite3.Error as e:
        return jsonify(
            {"erro": "Erro ao acessar o banco de dados", "detalhe": str(e)}
        ), 500

    livros_lista = [dict(livro) for livro in livros]

    return jsonify({"livros": livros_lista}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
