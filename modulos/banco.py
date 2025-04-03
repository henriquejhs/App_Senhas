import sqlite3
import logging

ARQUIVO_BANCO = "senhas.db"

def inicializar_banco():
    conn = sqlite3.connect(ARQUIVO_BANCO)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credenciais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            usuario TEXT,
            senha TEXT,
            ip_link TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Banco de dados inicializado.")

def carregar_dados(fernet):
    try:
        conn = sqlite3.connect(ARQUIVO_BANCO)
        cursor = conn.cursor()
        cursor.execute("SELECT descricao, usuario, senha, ip_link FROM credenciais")
        dados = {}
        for row in cursor.fetchall():
            descricao = row[0]  # Descrição não está criptografada
            usuario = fernet.decrypt(row[1].encode()).decode() if row[1] else ""
            senha = fernet.decrypt(row[2].encode()).decode() if row[2] else ""
            ip_link = fernet.decrypt(row[3].encode()).decode() if row[3] else ""
            dados[descricao] = {"usuario": usuario, "senha": senha, "ip_link": ip_link}
        conn.close()
        logging.info("Dados carregados do banco de dados com sucesso.")
        return dados
    except Exception as e:
        logging.error(f"Falha ao carregar dados do banco de dados: {str(e)}")
        raise

def salvar_dados_todos(dados, fernet):
    try:
        conn = sqlite3.connect(ARQUIVO_BANCO)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM credenciais")
        for descricao, info in dados.items():
            usuario_criptografado = fernet.encrypt(info["usuario"].encode()).decode() if info["usuario"] else ""
            senha_criptografada = fernet.encrypt(info["senha"].encode()).decode() if info["senha"] else ""
            ip_link_criptografado = fernet.encrypt(info["ip_link"].encode()).decode() if info["ip_link"] else ""
            cursor.execute(
                "INSERT INTO credenciais (descricao, usuario, senha, ip_link) VALUES (?, ?, ?, ?)",
                (descricao, usuario_criptografado, senha_criptografada, ip_link_criptografado)
            )
        conn.commit()
        conn.close()
        logging.info("Dados salvos no banco de dados com sucesso.")
    except Exception as e:
        logging.error(f"Falha ao salvar dados no banco de dados: {str(e)}")
        raise
