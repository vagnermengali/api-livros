from flask import Flask, jsonify, render_template, request
import sqlite3
import re
import os
import logging
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

db_path = os.getenv("DB_PATH", "database.db")
logging.basicConfig(level=logging.INFO)

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS LIVROS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                image_url TEXT NOT NULL
            );
            """
        )

with app.app_context():
    init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/doar", methods=["POST"])
def doar():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado foi fornecido"}), 400

    campos_obrigatorios = ["titulo", "categoria", "autor", "image_url"]
    campos_faltantes = [campo for campo in campos_obrigatorios if not dados.get(campo, "").strip()]

    if campos_faltantes:
        return jsonify({
            "erro": "Campos obrigatórios não fornecidos ou estão vazios",
            "campos_faltantes": campos_faltantes,
        }), 400

    titulo, categoria, autor, image_url = (dados[campo].strip() for campo in campos_obrigatorios)

    if not re.match(r"^https?://[^\s]+$", image_url):
        return jsonify({"erro": "URL da imagem inválida"}), 400

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO LIVROS (titulo, categoria, autor, image_url) VALUES (?, ?, ?, ?)",
                (titulo, categoria, autor, image_url)
            )
            conn.commit()
        return jsonify({
            "mensagem": "Livro cadastrado com sucesso",
            "livro": {"titulo": titulo, "categoria": categoria, "autor": autor, "image_url": image_url},
        }), 201
    except sqlite3.Error as e:
        logging.error(f"Erro ao cadastrar livro: {e}")
        return jsonify({"erro": "Erro ao cadastrar livro", "detalhe": str(e)}), 500

@app.route("/livros", methods=["GET"])
def listar_livros():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        offset = (page - 1) * per_page

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM LIVROS LIMIT ? OFFSET ?", (per_page, offset))
            livros = [dict(livro) for livro in cursor.fetchall()]
        return jsonify({"livros": livros, "page": page, "per_page": per_page}), 200
    except sqlite3.Error as e:
        logging.error(f"Erro ao acessar o banco de dados: {e}")
        return jsonify({"erro": "Erro ao acessar o banco de dados", "detalhe": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
