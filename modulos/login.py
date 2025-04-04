import tkinter as tk
from tkinter import messagebox
import hashlib
import os
import logging

ARQUIVO_SENHA_MESTRA = "senha_mestra.hash"

def hash_senha(senha):
    """Gera um hash SHA-256 da senha fornecida."""
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha_mestra(senha_digitada):
    """Verifica se a senha digitada corresponde ao hash armazenado."""
    if not os.path.exists(ARQUIVO_SENHA_MESTRA):
        return False  # Senha mestra ainda não foi definida
    with open(ARQUIVO_SENHA_MESTRA, "r") as arquivo:
        hash_armazenado = arquivo.read().strip()
    return hash_senha(senha_digitada) == hash_armazenado

def salvar_senha_mestra(senha):
    """Salva o hash da senha mestra no arquivo."""
    hash_senha_mestra = hash_senha(senha)
    with open(ARQUIVO_SENHA_MESTRA, "w") as arquivo:
        arquivo.write(hash_senha_mestra)
    logging.info("Senha mestra salva com sucesso.")

def criar_tela_login(janela, callback_sucesso):
    """Cria a tela de login ou configuração da senha mestra."""
    tela_login = tk.Toplevel(janela)
    tela_login.title("Login - Gerenciador de Senhas")
    tela_login.geometry("300x200")
    tela_login.resizable(False, False)
    tela_login.grab_set()

    # Verifica se é a primeira vez (sem senha mestra)
    primeira_vez = not os.path.exists(ARQUIVO_SENHA_MESTRA)

    if primeira_vez:
        tk.Label(tela_login, text="Defina sua senha mestra:", font=("Arial", 12)).pack(pady=10)
    else:
        tk.Label(tela_login, text="Digite sua senha mestra:", font=("Arial", 12)).pack(pady=10)

    entrada_senha = tk.Entry(tela_login, show="*", width=30)
    entrada_senha.pack(pady=10)
    entrada_senha.focus_set()

    if primeira_vez:
        tk.Label(tela_login, text="Confirme a senha mestra:").pack()
        entrada_confirmacao = tk.Entry(tela_login, show="*", width=30)
        entrada_confirmacao.pack(pady=10)

    def tentar_login():
        senha = entrada_senha.get()
        if primeira_vez:
            confirmacao = entrada_confirmacao.get()
            if not senha or not confirmacao:
                messagebox.showwarning("Erro", "Preencha ambos os campos!")
                logging.warning("Tentativa de definir senha mestra com campos vazios.")
                return
            if senha != confirmacao:
                messagebox.showwarning("Erro", "As senhas não coincidem!")
                logging.warning("Senhas mestras não coincidem na configuração.")
                return
            salvar_senha_mestra(senha)
            messagebox.showinfo("Sucesso", "Senha mestra definida com sucesso!")
            logging.info("Senha mestra definida pelo usuário.")
            tela_login.destroy()
            callback_sucesso()
        else:
            if not senha:
                messagebox.showwarning("Erro", "Digite a senha mestra!")
                logging.warning("Tentativa de login sem senha.")
                return
            if verificar_senha_mestra(senha):
                logging.info("Login bem-sucedido.")
                tela_login.destroy()
                callback_sucesso()
            else:
                messagebox.showerror("Erro", "Senha mestra incorreta!")
                logging.warning("Tentativa de login com senha mestra incorreta.")

    tk.Button(tela_login, text="Confirmar", command=tentar_login).pack(pady=10)

    # Permitir login com Enter
    entrada_senha.bind("<Return>", lambda event: tentar_login())
    if primeira_vez:
        entrada_confirmacao.bind("<Return>", lambda event: tentar_login())

    tela_login.wait_window()

def autenticar(janela, callback_sucesso):
    """Função principal para autenticação."""
    criar_tela_login(janela, callback_sucesso)