# Documentação da API Livros

## 🔍 Descrição
A **API Livros** é uma API REST simples para gerenciamento de livros, desenvolvida com Flask e SQLite.
Permite cadastrar novos livros, listar os livros cadastrados e consultar informações de cada livro.

## 📝 Requisitos
- Python 3.13 ou superior
- Dependências listadas em `requirements.txt` ou `pyproject.toml`

## ✨ Instalação
### Usando `pip`
1. Clone o repositório ou baixe os arquivos da API.
2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   ```
3. Ative o ambiente virtual:
   - No Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Usando `Poetry`
1. Clone o repositório ou baixe os arquivos da API.
2. Instale as dependências:
   ```bash
   poetry install
   ```

## 💪 Configuração Inicial
Nenhuma configuração adicional é necessária. O banco de dados SQLite (`database.db`) será criado automaticamente na primeira execução.

## 🚀 Como Executar a API
Execute o seguinte comando para iniciar a API:
```bash
python app.py
```
Ou, caso esteja usando Flask CLI:
```bash
flask run
```
A API estará disponível em: `http://127.0.0.1:5000`

## 🛠️ Rotas Disponíveis
| Método | Endpoint   | Descrição |
|---------|-----------|------------|
| `GET`   | `/`       | Página inicial da API |
| `POST`  | `/livros` | Cadastrar um novo livro |
| `GET`   | `/livros` | Listar todos os livros cadastrados |

---

## 📚 Endpoints

### 🔖 Home
- **URL:** `/`
- **Método:** `GET`
- **Descrição:** Exibe uma mensagem informando que a API está funcionando.

---

### ➕ Cadastrar Livro
- **URL:** `/livros`
- **Método:** `POST`
- **Descrição:** Cadastra um novo livro no sistema.

**Corpo da Requisição (JSON):**
```json
{
  "titulo": "Título do livro",
  "categoria": "Categoria do livro",
  "autor": "Nome do autor",
  "imagem_url": "https://url-da-imagem.com"
}
```

**Respostas:**
- `201 Created`: Livro cadastrado com sucesso.
- `400 Bad Request`: Dados inválidos ou incompletos.
- `500 Internal Server Error`: Erro ao acessar o banco de dados.

---

### 📖 Listar Livros
- **URL:** `/livros`
- **Método:** `GET`
- **Descrição:** Retorna todos os livros cadastrados no sistema.

**Respostas:**
- `200 OK`: Lista de livros retornada com sucesso.
- `500 Internal Server Error`: Erro ao acessar o banco de dados.

---

## 💳 Estrutura do Banco de Dados

Tabela: `livros`

| Campo      | Tipo    | Descrição                           |
|------------|---------|-------------------------------------|
| `id`         | INTEGER | ID do livro (chave primária)        |
| `titulo`     | TEXT    | Título do livro                     |
| `categoria`  | TEXT    | Categoria do livro                  |
| `autor`      | TEXT    | Nome do autor                       |
| `imagem_url` | TEXT    | URL da imagem de capa               |

## 📊 Validações
- Todos os campos são obrigatórios.
- A URL da imagem deve começar com `http://` ou `https://`.

## 📂 Exemplos de Uso

### ➕ Cadastrar um Livro
**Requisição:**
```bash
POST /livros
Content-Type: application/json

{
  "titulo": "O Senhor dos Anéis",
  "categoria": "Fantasia",
  "autor": "J.R.R. Tolkien",
  "imagem_url": "https://example.com/capa.jpg"
}
```

**Resposta:**
```json
{
  "mensagem": "Livro cadastrado com sucesso",
  "livro": {
    "id": 1,
    "titulo": "O Senhor dos Anéis",
    "categoria": "Fantasia",
    "autor": "J.R.R. Tolkien",
    "imagem_url": "https://example.com/capa.jpg"
  }
}
```

---

### 📖 Listar Todos os Livros
**Requisição:**
```bash
GET /livros
```

**Resposta:**
```json
{
  "livros": [
    {
      "id": 1,
      "titulo": "O Senhor dos Anéis",
      "categoria": "Fantasia",
      "autor": "J.R.R. Tolkien",
      "imagem_url": "https://example.com/capa.jpg"
    },
    {
      "id": 2,
      "titulo": "Harry Potter e a Pedra Filosofal",
      "categoria": "Fantasia",
      "autor": "J.K. Rowling",
      "imagem_url": "https://example.com/capa2.jpg"
    }
  ]
}
```

---

## 🌟 Contribuição
Se você deseja contribuir com este projeto, fique à vontade para abrir um Pull Request!

## ⚖️ Licença
Este projeto está sob a licença MIT.

