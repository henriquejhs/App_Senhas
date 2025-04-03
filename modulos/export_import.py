import json
from cryptography.fernet import Fernet
import logging
import tkinter as tk  # Adicionada a importação do tkinter como tk
from tkinter import filedialog, messagebox

def exportar_arquivo(janela, lista_senhas):
    janela_confirmacao = tk.Toplevel(janela)
    janela_confirmacao.title("Confirmar Exportação")
    janela_confirmacao.geometry("300x150")
    janela_confirmacao.resizable(False, False)
    janela_confirmacao.grab_set()

    tk.Label(janela_confirmacao, text="Escolha uma opção para exportar:", font=("Arial", 12)).pack(pady=10)
    escolha = tk.StringVar(value="")

    def exportar_todos():
        escolha.set("todos")
        janela_confirmacao.destroy()

    def exportar_selecionados():
        selecao = lista_senhas.curselection()
        if not selecao:
            messagebox.showwarning("Erro", "Nenhuma entrada selecionada para exportar!")
            logging.warning("Tentativa de exportar dados selecionados sem seleção.")
            return
        escolha.set("selecionados")
        janela_confirmacao.destroy()

    tk.Button(janela_confirmacao, text="Transferir todos os dados", command=exportar_todos, width=25).pack(pady=5)
    tk.Button(janela_confirmacao, text="Transferir apenas os selecionados", command=exportar_selecionados, width=25).pack(pady=5)

    janela_confirmacao.wait_window()
    if not escolha.get():
        return

    from banco import carregar_dados
    dados = carregar_dados(janela.fernet)
    dados_a_exportar = {}

    if escolha.get() == "todos":
        dados_a_exportar = dados
        logging.info("Usuário escolheu exportar todos os dados.")
    else:
        selecao = lista_senhas.curselection()
        for indice in selecao:
            descricao = lista_senhas.get(indice)
            dados_a_exportar[descricao] = dados[descricao]
        logging.info(f"Usuário escolheu exportar dados selecionados: {list(dados_a_exportar.keys())}")

    destino = filedialog.asksaveasfilename(
        defaultextension=".enc",
        filetypes=[("Arquivos criptografados", "*.enc"), ("Todos os arquivos", "*.*")],
        title="Exportar dados"
    )
    if destino:
        try:
            chave_export = Fernet.generate_key()
            fernet_export = Fernet(chave_export)
            logging.info("Chave temporária gerada para exportação.")

            chave_destino = destino.replace(".enc", "_key.key")
            with open(chave_destino, "wb") as arquivo_chave:
                arquivo_chave.write(chave_export)
            logging.info(f"Chave temporária salva em: {chave_destino}")

            dados_json = json.dumps(dados_a_exportar)
            logging.info(f"Dados convertidos para JSON: {dados_json}")

            dados_criptografados = fernet_export.encrypt(dados_json.encode())
            logging.info(f"Dados criptografados (tamanho): {len(dados_criptografados)} bytes")

            with open(destino, "wb") as arquivo:
                arquivo.write(dados_criptografados)

            messagebox.showinfo("Sucesso", f"Dados exportados com sucesso!\nArquivo exportado: {destino}\nChave de exportação: {chave_destino}\nEnvie ambos os arquivos para o outro usuário.")
            logging.info(f"Dados exportados para: {destino}")
        except Exception as e:
            logging.error(f"Falha ao exportar os dados: {str(e)}")
            messagebox.showerror("Erro", f"Falha ao exportar os dados: {str(e)}")

def importar_arquivo(janela, filtrar_lista):
    origem = filedialog.askopenfilename(
        filetypes=[("Arquivos criptografados", "*.enc"), ("Todos os arquivos", "*.*")],
        title="Selecionar arquivo de dados para importar"
    )
    if not origem:
        return

    chave_origem = filedialog.askopenfilename(
        filetypes=[("Arquivos de chave", "*.key"), ("Todos os arquivos", "*.*")],
        title="Selecionar a chave de exportação (export_key.key)"
    )
    if not chave_origem:
        messagebox.showwarning("Erro", "Nenhuma chave de exportação selecionada!")
        return

    try:
        with open(chave_origem, "rb") as arquivo_chave:
            chave_export = arquivo_chave.read()
        fernet_export = Fernet(chave_export)
        logging.info(f"Chave de exportação carregada de: {chave_origem}")

        with open(origem, "rb") as arquivo:
            dados_criptografados = arquivo.read()
        logging.info(f"Arquivo lido: {origem}, tamanho: {len(dados_criptografados)} bytes")

        dados_json = fernet_export.decrypt(dados_criptografados).decode()
        logging.info(f"Dados descriptografados: {dados_json}")

        dados_importados = json.loads(dados_json)
        logging.info(f"Dados importados (convertidos de JSON): {dados_importados}")

        from banco import carregar_dados, salvar_dados_todos
        dados_atuais = carregar_dados(janela.fernet)
        logging.info(f"Dados atuais antes da mesclagem: {dados_atuais}")

        dados_atuais.update(dados_importados)
        logging.info(f"Dados após mesclagem: {dados_atuais}")

        salvar_dados_todos(dados_atuais, janela.fernet)
        messagebox.showinfo("Sucesso", "Dados importados e mesclados com sucesso!")
        filtrar_lista()
        logging.info(f"Dados importados e mesclados de: {origem}")
    except Exception as e:
        logging.error(f"Falha ao importar os dados: {str(e)}")
        messagebox.showerror("Erro", f"Falha ao importar os dados: {str(e)}\nVerifique se a chave de exportação está correta.")
