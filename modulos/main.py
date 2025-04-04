import tkinter as tk
from criptografia import inicializar_criptografia
from banco import inicializar_banco
from interface import criar_interface, atualizar_lista, filtrar_lista
from export_import import exportar_arquivo, importar_arquivo
from login import autenticar  # Importação do novo módulo de login

def iniciar_interface(janela):
    """Inicia a interface principal após autenticação."""
    fernet = inicializar_criptografia()
    inicializar_banco()
    criar_interface(janela, fernet, atualizar_lista, filtrar_lista, exportar_arquivo, importar_arquivo)

def main():
    janela = tk.Tk()
    janela.withdraw()  # Esconde a janela principal até o login ser concluído
    autenticar(janela, lambda: [janela.deiconify(), iniciar_interface(janela)])  # Mostra a janela e inicia a interface após login
    janela.mainloop()

if __name__ == "__main__":
    main()
