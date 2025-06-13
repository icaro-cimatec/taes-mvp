# 🧵 Arteza – Plataforma de Artesanato

**Arteza** é uma plataforma web que conecta artesãos locais com clientes de todo o Brasil, permitindo o cadastro de produtos, exibição em catálogo, carrinho de compras e avaliações.

---

## ✅ Funcionalidades implementadas

### Sprint 1 – MVP
- Cadastro e login de artesãos
- Cadastro de produtos (nome, descrição, preço)
- Listagem pública de produtos
- Estrutura em camadas (MVC)
- Segurança com JWT e `.env`
- Banco de dados SQLite com SQLAlchemy

### Sprint 2 – Experiência de compra
- Carrinho de compras com JavaScript (`localStorage`)
- Checkout simulado
- Avaliação de produtos (comentários + nota)
- Testes com Pytest
- Organização do frontend com HTML/JS puro

---

## 🧱 Tecnologias

- Python 3.10+
- Flask
- SQLAlchemy (ORM)
- Flask-CORS
- JWT (`pyjwt`)
- dotenv (`python-dotenv`)
- HTML5, CSS3, JavaScript
- SQLite (banco local)
- Pytest (testes)
- Bandit, Flake8 (DevSecOps)

---

## 📦 Instalação

```bash
git clone https://github.com/icaro-cimatec/taes-mvp.git
cd taes-mvp
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
