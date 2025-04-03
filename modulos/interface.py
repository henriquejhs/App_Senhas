import tkinter as tk
from tkinter import messagebox
import pyperclip
import logging

def criar_interface(janela, fernet, atualizar_lista, filtrar_lista, exportar_arquivo, importar_arquivo):
    janela.title("Gerenciador de senhas - José Henrique")
    janela.geometry("600x500")
    janela.fernet = fernet

    # Frame para o título e pesquisa
    frame_topo = tk.Frame(janela)
    frame_topo.pack(fill=tk.X, pady=5)

    tk.Label(frame_topo, text="Gerenciador de senhas - José Henrique", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Label(frame_topo, text="Pesquisar (Descrição ou IP/Link):").pack(side=tk.LEFT, padx=5)
    entrada_pesquisa = tk.Entry(frame_topo)
    entrada_pesquisa.pack(side=tk.LEFT, padx=5)
    entrada_pesquisa.bind("<KeyRelease>", lambda event: filtrar_lista(entrada_pesquisa))

    # Frame principal para dividir a lista e os dados
    frame_principal = tk.Frame(janela)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Frame para a lista de descrições (esquerda)
    frame_lista = tk.Frame(frame_principal)
    frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(frame_lista, text="Descrições salvas:").pack(anchor="w")
    lista_senhas = tk.Listbox(frame_lista, height=15, selectmode=tk.EXTENDED)
    lista_senhas.pack(fill=tk.BOTH, expand=True)
    janela.lista_senhas = lista_senhas

    # Frame para os botões Exportar, Importar, Editar e Eliminar
    frame_botoes_lista = tk.Frame(frame_lista)
    frame_botoes_lista.pack(fill=tk.X, pady=5)

    tk.Button(frame_botoes_lista, text="Exportar", command=lambda: exportar_arquivo(janela, lista_senhas)).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes_lista, text="Importar", command=lambda: importar_arquivo(janela, lambda: filtrar_lista(entrada_pesquisa))).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes_lista, text="Editar", command=lambda: editar_dados(janela, lista_senhas, lambda: filtrar_lista(entrada_pesquisa))).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes_lista, text="Eliminar", command=lambda: eliminar_dado(janela, lista_senhas, lambda: filtrar_lista(entrada_pesquisa))).pack(side=tk.LEFT, padx=5)

    # Frame para exibição dos dados (direita)
    frame_dados = tk.Frame(frame_principal)
    frame_dados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    descricao_atual = tk.StringVar()
    usuario_atual = tk.StringVar()
    senha_atual = tk.StringVar()
    ip_link_atual = tk.StringVar()

    tk.Label(frame_dados, text="Descrição:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tk.Label(frame_dados, textvariable=descricao_atual).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_dados, text="Usuário:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    tk.Label(frame_dados, textvariable=usuario_atual).grid(row=1, column=1, padx=5, pady=5, sticky="w")
    tk.Button(frame_dados, text="Copiar", command=lambda: copiar_dado(usuario_atual, "Usuário")).grid(row=1, column=2, padx=5)

    tk.Label(frame_dados, text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    tk.Label(frame_dados, textvariable=senha_atual).grid(row=2, column=1, padx=5, pady=5, sticky="w")
    tk.Button(frame_dados, text="Copiar", command=lambda: copiar_dado(senha_atual, "Senha")).grid(row=2, column=2, padx=5)

    tk.Label(frame_dados, text="IP/Link:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    tk.Label(frame_dados, textvariable=ip_link_atual).grid(row=3, column=1, padx=5, pady=5, sticky="w")
    tk.Button(frame_dados, text="Copiar", command=lambda: copiar_dado(ip_link_atual, "IP/Link")).grid(row=3, column=2, padx=5)

    btn_limpar = tk.Button(frame_dados, text="Limpar Dados", command=lambda: limpar_dados(descricao_atual, usuario_atual, senha_atual, ip_link_atual, lista_senhas))
    btn_limpar.grid(row=4, column=0, columnspan=3, pady=10)

    # Frame para adicionar novos dados (inferior)
    frame_entrada = tk.Frame(janela)
    frame_entrada.pack(fill=tk.X, pady=10)

    tk.Label(frame_entrada, text="Adicionar novos dados:").grid(row=0, column=0, columnspan=6, pady=5)

    tk.Label(frame_entrada, text="Descrição:").grid(row=1, column=0, padx=5, sticky="w")
    entrada_descricao = tk.Entry(frame_entrada)
    entrada_descricao.grid(row=1, column=1, padx=5)

    tk.Label(frame_entrada, text="Usuário:").grid(row=1, column=2, padx=5, sticky="w")
    entrada_usuario = tk.Entry(frame_entrada)
    entrada_usuario.grid(row=1, column=3, padx=5)

    tk.Label(frame_entrada, text="Senha:").grid(row=2, column=0, padx=5, sticky="w")
    entrada_senha = tk.Entry(frame_entrada)
    entrada_senha.grid(row=2, column=1, padx=5)

    tk.Label(frame_entrada, text="IP/Link:").grid(row=2, column=2, padx=5, sticky="w")
    entrada_ip_link = tk.Entry(frame_entrada)
    entrada_ip_link.grid(row=2, column=3, padx=5)

    # Botão "Salvar Novos Dados" na coluna 0 a 3
    tk.Button(frame_entrada, text="Salvar Novos Dados", command=lambda: adicionar_novos_dados(janela, entrada_descricao, entrada_usuario, entrada_senha, entrada_ip_link, entrada_pesquisa)).grid(row=3, column=0, columnspan=4, pady=10)

    # Botão "Encerrar" no canto direito, mesma linha do "Salvar Novos Dados"
    btn_encerrar = tk.Button(frame_entrada, text="Encerrar", command=lambda: [logging.info("Botão Encerrar clicado."), encerrar_app(janela)], bg="red", fg="white")
    btn_encerrar.grid(row=3, column=5, padx=(20, 5), pady=10, sticky="e")

    # Funções auxiliares
    def mostrar_dados(event):
        selecao = lista_senhas.curselection()
        if selecao:
            from banco import carregar_dados
            descricao = lista_senhas.get(selecao[0])
            dados = carregar_dados(janela.fernet)
            info = dados[descricao]
            descricao_atual.set(descricao)
            usuario_atual.set(info["usuario"])
            senha_atual.set(info["senha"])
            ip_link_atual.set(info["ip_link"])
            logging.info(f"Dados exibidos para a descrição: {descricao}")
        else:
            limpar_dados(descricao_atual, usuario_atual, senha_atual, ip_link_atual, lista_senhas)

    lista_senhas.bind("<<ListboxSelect>>", mostrar_dados)

    atualizar_lista(lista_senhas, "", janela.fernet)

def atualizar_lista(lista_senhas, filtro, fernet):
    lista_senhas.delete(0, tk.END)
    from banco import carregar_dados
    dados = carregar_dados(fernet)
    for descricao, info in dados.items():
        if filtro.lower() in descricao.lower() or filtro.lower() in info["ip_link"].lower():
            lista_senhas.insert(tk.END, descricao)
    logging.info(f"Lista atualizada com filtro: {filtro}")

def filtrar_lista(entrada_pesquisa):
    filtro = entrada_pesquisa.get()
    atualizar_lista(entrada_pesquisa.master.master.lista_senhas, filtro, entrada_pesquisa.master.master.fernet)

def copiar_dado(dado_atual, tipo):
    dado = dado_atual.get()
    if dado:
        pyperclip.copy(dado)
        messagebox.showinfo("Sucesso", f"{tipo} copiado!")
        logging.info(f"{tipo} copiado: {dado}")
    else:
        messagebox.showwarning("Erro", f"Nenhum {tipo.lower()} selecionado!")
        logging.warning(f"Tentativa de copiar {tipo.lower()} sem seleção.")

def limpar_dados(descricao_atual, usuario_atual, senha_atual, ip_link_atual, lista_senhas):
    descricao_atual.set("")
    usuario_atual.set("")
    senha_atual.set("")
    ip_link_atual.set("")
    lista_senhas.selection_clear(0, tk.END)
    logging.info("Dados exibidos limpos.")

def adicionar_novos_dados(janela, entrada_descricao, entrada_usuario, entrada_senha, entrada_ip_link, entrada_pesquisa):
    descricao = entrada_descricao.get()
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    ip_link = entrada_ip_link.get()
    if descricao:
        from banco import carregar_dados, salvar_dados_todos
        dados = carregar_dados(janela.fernet)
        dados[descricao] = {"usuario": usuario, "senha": senha, "ip_link": ip_link}
        salvar_dados_todos(dados, janela.fernet)
        entrada_descricao.delete(0, tk.END)
        entrada_usuario.delete(0, tk.END)
        entrada_senha.delete(0, tk.END)
        entrada_ip_link.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Dados adicionados com sucesso!")
        filtrar_lista(entrada_pesquisa)
        logging.info(f"Novos dados adicionados: {descricao}")
    else:
        messagebox.showwarning("Erro", "A descrição é obrigatória!")
        logging.warning("Tentativa de adicionar dados sem descrição.")

def eliminar_dado(janela, lista_senhas, filtrar_lista):
    selecao = lista_senhas.curselection()
    if not selecao:
        messagebox.showwarning("Erro", "Selecione uma descrição para eliminar!")
        logging.warning("Tentativa de eliminar sem seleção.")
        return

    from banco import carregar_dados, salvar_dados_todos
    for indice in selecao:
        descricao = lista_senhas.get(indice)
        resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja eliminar a entrada '{descricao}'?")
        if resposta:
            try:
                dados = carregar_dados(janela.fernet)
                if descricao in dados:
                    del dados[descricao]
                    salvar_dados_todos(dados, janela.fernet)
                    limpar_dados(janela.descricao_atual, janela.usuario_atual, janela.senha_atual, janela.ip_link_atual, lista_senhas)
                    filtrar_lista()
                    messagebox.showinfo("Sucesso", f"Entrada '{descricao}' eliminada com sucesso!")
                    logging.info(f"Entrada eliminada: {descricao}")
                else:
                    messagebox.showwarning("Erro", "Entrada não encontrada!")
                    logging.warning(f"Entrada não encontrada para eliminação: {descricao}")
            except Exception as e:
                logging.error(f"Falha ao eliminar a entrada: {str(e)}")
                messagebox.showerror("Erro", f"Falha ao eliminar a entrada: {str(e)}")

def editar_dados(janela, lista_senhas, filtrar_lista):
    selecao = lista_senhas.curselection()
    if not selecao:
        messagebox.showwarning("Erro", "Selecione uma descrição para editar!")
        logging.warning("Tentativa de editar sem seleção.")
        return

    from banco import carregar_dados, salvar_dados_todos
    descricao_antiga = lista_senhas.get(selecao[0])
    dados = carregar_dados(janela.fernet)
    info = dados[descricao_antiga]

    janela_editar = tk.Toplevel(janela)
    janela_editar.title("Editar Dados")
    janela_editar.geometry("400x300")

    tk.Label(janela_editar, text="Descrição:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entrada_descricao_editar = tk.Entry(janela_editar)
    entrada_descricao_editar.grid(row=0, column=1, padx=5, pady=5)
    entrada_descricao_editar.insert(0, descricao_antiga)

    tk.Label(janela_editar, text="Usuário:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entrada_usuario_editar = tk.Entry(janela_editar)
    entrada_usuario_editar.grid(row=1, column=1, padx=5, pady=5)
    entrada_usuario_editar.insert(0, info["usuario"])

    tk.Label(janela_editar, text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entrada_senha_editar = tk.Entry(janela_editar)
    entrada_senha_editar.grid(row=2, column=1, padx=5, pady=5)
    entrada_senha_editar.insert(0, info["senha"])

    tk.Label(janela_editar, text="IP/Link:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entrada_ip_link_editar = tk.Entry(janela_editar)
    entrada_ip_link_editar.grid(row=3, column=1, padx=5, pady=5)
    entrada_ip_link_editar.insert(0, info["ip_link"])

    def salvar_alteracoes():
        nova_descricao = entrada_descricao_editar.get()
        if not nova_descricao:
            messagebox.showwarning("Erro", "A descrição é obrigatória!")
            logging.warning("Tentativa de salvar edição sem descrição.")
            return

        dados = carregar_dados(janela.fernet)
        if nova_descricao != descricao_antiga:
            del dados[descricao_antiga]
        dados[nova_descricao] = {
            "usuario": entrada_usuario_editar.get(),
            "senha": entrada_senha_editar.get(),
            "ip_link": entrada_ip_link_editar.get()
        }
        salvar_dados_todos(dados, janela.fernet)
        messagebox.showinfo("Sucesso", "Dados editados com sucesso!")
        filtrar_lista()
        limpar_dados(janela.descricao_atual, janela.usuario_atual, janela.senha_atual, janela.ip_link_atual, lista_senhas)
        janela_editar.destroy()
        logging.info(f"Dados editados: {nova_descricao}")

    tk.Button(janela_editar, text="Salvar Alterações", command=salvar_alteracoes).grid(row=4, column=0, columnspan=2, pady=10)

def encerrar_app(janela):
    try:
        logging.info("Tentando encerrar a aplicação.")
        janela.destroy()
        logging.info("Aplicação encerrada com sucesso.")
    except Exception as e:
        logging.error(f"Falha ao encerrar a aplicação: {str(e)}")
        messagebox.showerror("Erro", f"Falha ao encerrar a aplicação: {str(e)}")
