# App_Senhas

## Pré-requisitos de Python
- Python 3.x
  - Recomendo usar uma versão recente, como Python 3.9, 3.10 ou 3.11, para garantir compatibilidade com as bibliotecas utilizadas.
  - Verifique a versão instalada com: `python --version` ou `python3 --version`.

### Bibliotecas Necessárias
- As bibliotecas abaixo são importadas diretamente no seu código. Instale-as via pip:
  - **tkinter**: Biblioteca padrão para interfaces gráficas.
    - Normalmente já vem com o Python, mas em alguns sistemas (como Linux), pode ser necessário instalar separadamente.
    - No Linux (ex.: Ubuntu): `sudo apt-get install python3-tk`
    - No Windows e macOS, geralmente já está incluído.
  - **cryptography**: Usada para criptografia com Fernet.
    - Instale com: `pip install cryptography`
  - **pyperclip**: Usada para copiar dados para a área de transferência.
    - Instale com: `pip install pyperclip`
  - **pyinstaller**: Ferramenta para criar o executável.
    - Instale com: `pip install pyinstaller`
- **Outras Dependências Implícitas**:
  - `sqlite3`: Biblioteca padrão do Python para manipulação de bancos de dados SQLite. Não precisa instalar separadamente.
  - `logging`, `os`, `json`, `hashlib`: Todas são bibliotecas padrão do Python, então não requerem instalação adicional.

## Passos para Configurar o Ambiente
1. **Instale o Python**
   - Baixe e instale o Python do site oficial (https://www.python.org/) se ainda não estiver instalado.
   - Certifique-se de adicionar o Python ao PATH durante a instalação (opção no instalador do Windows).
2. **Crie um Ambiente Virtual (Opcional, mas Recomendado)**
   - Para evitar conflitos com outros projetos:
     - `python -m venv venv`
   - Ative o ambiente:
     - Windows: `venv\Scripts\activate`
     - Linux/macOS: `source venv/bin/activate`
3. **Instale as Dependências**
   - Com o ambiente ativo, execute:
     - `pip install cryptography pyperclip pyinstaller`
4. **Verifique as Instalações**
   - Confirme que tudo está instalado:
     - `pip list`
   - Você deve ver `cryptography`, `pyperclip` e `pyinstaller` na lista.

## Considerações para o PyInstaller
- Ao usar `pyinstaller --onefile --noconsole main.py`, você está gerando um executável único sem janela de console. Aqui estão algumas observações:
  - **Dependências Ocultas**:
    - O PyInstaller geralmente detecta as dependências automaticamente (como `tkinter`, `cryptography`, etc.), mas pode haver problemas com bibliotecas dinâmicas ou recursos externos (como o `tcl/tk` no Linux).
    - Se o executável falhar ao rodar, você pode precisar especificar manualmente caminhos ou arquivos ocultos no comando do PyInstaller.
  - **Comando Completo (Caso Necessário)**:
    - Se houver erros ao executar o executável (ex.: "módulo não encontrado"), tente:
      - `pyinstaller --onefile --noconsole --hidden-import=tkinter --hidden-import=cryptography --hidden-import=pyperclip main.py`
    - Isso força o PyInstaller a incluir explicitamente os módulos.
  - **Sistema Operacional**:
    - O executável gerado só funciona no sistema operacional onde foi compilado (Windows, Linux ou macOS).
    - Para suportar outros sistemas, você precisa compilar em cada um deles separadamente.
    - No Linux, certifique-se de que o `tcl/tk` esteja instalado no sistema de destino, pois o `tkinter` depende disso.
  - **Tamanho do Executável**:
    - O argumento `--onefile` empacota tudo em um único arquivo, o que pode resultar em um executável grande (provavelmente 20-40 MB, dependendo das bibliotecas). Isso é normal.
  - **Arquivos Gerados**:
    - O PyInstaller criará uma pasta `dist/` com o executável `main.exe` (Windows) ou `main` (Linux/macOS).
    - Os arquivos `senhas.db`, `chave.key`, `senha_mestra.hash`, e logs (`app_senha.log`) serão gerados no mesmo diretório onde o executável é executado, a menos que você ajuste os caminhos no código.

## Testando o Executável
- Após compilar com `pyinstaller --onefile --noconsole main.py`, vá até a pasta `dist/`:
  - Windows: `cd dist` e execute `main.exe`.
  - Linux/macOS: `cd dist` e execute `./main`.
- Verifique se:
  - A tela de login aparece.
  - A interface principal carrega após autenticação.
  - As funcionalidades (salvar, exportar, importar, etc.) funcionam corretamente.
- Se houver erros (ex.: "módulo não encontrado" ou "arquivo não pôde ser aberto"):
  - Revise os logs gerados (`app_senha.log`) ou ajuste o comando do PyInstaller.

## Resumo dos Pré-requisitos
- **Python**: 3.9 ou superior.
- **Pacotes via pip**: `cryptography`, `pyperclip`, `pyinstaller`.
- **Sistema**: `tkinter` (padrão ou via `python3-tk` no Linux).
- **Comando**: `pyinstaller --onefile --noconsole main.py`.
