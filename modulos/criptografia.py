import os
from cryptography.fernet import Fernet
import logging

# Configuração do logging
logging.basicConfig(
    filename="app_senha.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ARQUIVO_CHAVE = "chave.key"

def carregar_chave():
    if os.path.exists(ARQUIVO_CHAVE):
        with open(ARQUIVO_CHAVE, "rb") as arquivo_chave:
            chave = arquivo_chave.read()
            logging.info("Chave de criptografia local carregada do arquivo existente.")
            return chave
    else:
        chave = Fernet.generate_key()
        with open(ARQUIVO_CHAVE, "wb") as arquivo_chave:
            arquivo_chave.write(chave)
        logging.info("Nova chave de criptografia local gerada e salva.")
        return chave

def inicializar_criptografia():
    chave = carregar_chave()
    return Fernet(chave)
