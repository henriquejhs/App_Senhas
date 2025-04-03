import tkinter as tk
from criptografia import inicializar_criptografia
from banco import inicializar_banco
from interface import criar_interface, atualizar_lista, filtrar_lista
from export_import import exportar_arquivo, importar_arquivo

def main():
    janela = tk.Tk()
    fernet = inicializar_criptografia()
    inicializar_banco()
    criar_interface(janela, fernet, atualizar_lista, filtrar_lista, exportar_arquivo, importar_arquivo)
    janela.mainloop()

if __name__ == "__main__":
    main()
