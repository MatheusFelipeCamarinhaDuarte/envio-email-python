import tkinter as tk
from tkinter import Tk
from tkinter import messagebox

class Janela(Tk):
    """Janela principal da nossa aplicação que herda tk.Tk do Tkinter,
    com o objetivo de ser uma single-page aplication e adiciona funções
    extras como o Limpar
    
    A janela principal já inicia com nome fixo e icone de nossa aplicação,
    além de fixar a largura e altura, e realizar um protocolo correto de quit()
    caso alguém delete a janela pelo botao.
    """
    from typing import Callable, Optional, Tuple, List
    from app.classes.banco_de_dados import Banco_de_dados
    from app.classes.enviador import Email
    
    def __init__(self, enviador:Email = None):
        """Método de criação de tela personalizada"""
        import os
        super().__init__()
        # Titulo inicial
        self.title("Matheus Solutions")
        # Icone
        diretorio_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_icone = os.path.join(diretorio_app, "icons", "selltech.ico")
        self.iconbitmap(caminho_icone)
        altura = 400
        largura = 550
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        # Travando as dimensões da janela
        self.resizable(False, False)
        # Protocolo de encerramento correto
        self.protocol("WM_DELETE_WINDOW", lambda: [self.quit(),self.destroy()])
        self.enviador = enviador

    def limpar(self) -> None:
        """Método para limpar todos os widgets

        Returns:
            Janela: retorna a janela limpa
        """
        for widget in self.winfo_children():
            widget.destroy()
        return self

    def duplo_frame(self,frame_pai:tk.Frame, orientacao: str = 'Y') -> Tuple[tk.Frame, tk.Frame]:
        """Cria um frame duplo na orientação especificada.
        X para Frame esqueda e direita, Y para frames superiores e inferiores

        Args:
            orientacao (str): Deve ser 'X' ou 'Y'. Defalts to 'Y'.

        Raises:
            ValueError: Se a orientação não for 'X' ou 'Y'.
    
        Returns:
            Tuple[tk.Frame, tk.Frame]: Retorna uma tupla contendo os dois frames criados.
        """
        if orientacao not in ("X", "Y"):
            raise ValueError("A orientação deve ser 'X' ou 'Y'.")
        # Fazendo a verificação da orientação da tela.
        if orientacao == "X":
            # Implementação para orientação X
            frame_esquerdo = tk.Frame(frame_pai)
            frame_esquerdo.pack(side=tk.LEFT)
            frame_direito = tk.Frame(frame_pai)
            frame_direito.pack(side=tk.RIGHT)          
            return frame_esquerdo, frame_direito
        else:
            # Implementação para orientação Y (superior e inferior)
            frame_superior = tk.Frame(frame_pai)
            frame_superior.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
            frame_inferior = tk.Frame(frame_pai)
            frame_inferior.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
            return frame_superior, frame_inferior

    def rodape(self, frame_inferior:tk.Frame, func_tela_anterior:Optional[Callable[[], None]] = None) -> tk.Frame:
        """Método que chame e adiciona um frame de rodapé com funções voltar e sair.

        Args:
            frame_inferior (tk.Frame): Frame em que se localiza a parte de baixo da janela.
            func_tela_anterior (function, optional): Aqui fica a função da geração da tela 
            anterior, sem ela, o código não adiciona o botão voltar. Defaults to False.

        Returns:
            tk.Frame: Frame equivalente ao rodape da janela.
        """        
        
        # A partir do frame inferior, cria um outro frame destinado ao rodapé
        frame_rodape = tk.Frame(frame_inferior)
        frame_rodape.pack(anchor=tk.S,expand=True, fill=tk.X)
        # Caso tenha a função da tela anterior, adiciona a tela voltar
        if func_tela_anterior:
            voltar = tk.Button(frame_rodape, text="Voltar", command=lambda: [func_tela_anterior()])
            voltar.pack(side=tk.LEFT, pady=10, padx=10)
        
        # Adiciona o botão de sair da aplicação com o devido
        sair = tk.Button(frame_rodape, text="Sair", command=lambda: self.quit())
        sair.pack(side=tk.RIGHT, pady=10, padx=10)
        
        # Retorna o frame do rodape (Já ligado ao frame inferior)
        return frame_rodape

    def multi_botoes(self, dicionario_botoes:dict, frame_pertencente:tk.Frame, largura_botao:int = 20, altura_botao:int = 1, espacamento:int=5, orientacao=tk.CENTER) -> list[tk.Button]:
        """Método para criar multiplos botões em sequência um do outro.

        Args:
            dicionario_botoes (dict): um dicionario onde a chave é o text do
            botao e o valor é a função passada por meio de lambda.
            frame_pertencente (tk.Frame): Frame onde o botão será colocado
            largura_botao (int, optional): largura padrão do botão. Defaults to 20.
            orientacao (optional): Orientação do botão (padrão é centro). Defaults to tk.CENTER.

        Returns:
            list[tk.Button]: Retorna uma lista de botões para caso queria modificar algo nele
        """
        # Gera uma lista vazia
        todos = []
        # Para cada nome gerado, cria um botao com a respectiva funcao dele e adiciona na lista
        for texto, funcao in dicionario_botoes.items():
            button = tk.Button(frame_pertencente, text=texto, width=largura_botao,height=altura_botao, command=funcao)
            button.pack(anchor=orientacao, pady=espacamento, padx=10)
            todos.append(button)
        return todos

    def multi_radios(self,lista_radio:list, frame_pertencente:tk.Frame,lista:bool=False,resposta:bool = True, frame_side:str = None) -> Tuple[tk.StringVar,List[tk.Radiobutton]]:
        """Método para criar multiplos botões radios em sequência um do outro e 
        retorna-los junto com a variável.
        
        O método conta também com um label que exibe em baixo a opção selecionada.

        Args:
            lista_radio (list): Lista dos radios que quer de valores
            frame_pertencente (tk.Frame): Frame em que quer adicionar os radios
            lista (bool, optional): disposição em lista ao invés de coluna. 
            Defaults to False.

        Returns:
            Tuple[tk.StringVar,List[tk.Radiobutton]]: Devolve 2 variáveis, uma é 
            a string var do que está escrito no Radio button, e a outra é uma lista
            de todos os tk.RadioButton 
        """
        # Definição da variável que indica o radio_button
        var_opcao = tk.StringVar(value='Nenhuma opção selecionada')
        
        # Criação do subframe para o radio button
        frame_dos_radio_buttons = tk.Frame(frame_pertencente)
        if frame_side:
            if frame_side not in ['left', 'right', 'top', 'bottom']:
                raise ValueError("A lista deve ser 'left', 'right', 'top' ou 'bottom'.")
            else:
                frame_dos_radio_buttons.pack(side=frame_side)
        else:    
            frame_dos_radio_buttons.pack()
        
        #Definição de 
        lado = tk.TOP
        orientacao=tk.W
        if lista:
            lado = tk.RIGHT
            orientacao=tk.CENTER
        
        
        lista_radio_buttons = []
        # Criação de radio_button versionada de acordo com a lista passada
        for texto in lista_radio:
            radio_button = tk.Radiobutton(frame_dos_radio_buttons, text=texto, variable=var_opcao, value=texto, command=lambda: [opcao.config(text=var_opcao.get())])
            radio_button.pack(anchor=orientacao,side=lado)
            lista_radio_buttons.append(radio_button)
        
        opcao = tk.Label(frame_pertencente, text=var_opcao.get())
        if resposta:
            # Label para mostrar a opção selecionada
            opcao.pack(anchor=orientacao)
        
        # Retorna a variável que mantém o valor selecionado
        return var_opcao, lista_radio_buttons

    def desativar_radio(self,*args: Tuple[tk.Radiobutton]) -> None:
        """Métodos para desativar múltiplos radios para não serems clicáveis
        
        Args:
            *args (Tuple[tk.Radiobutton]): Lista de todos os radios a serem desativados
        """
        for i, arg in enumerate(args):
            arg.config(state=tk.DISABLED)

    def verifica_radio(self,*args: Tuple[str]) -> bool:
        """Método para verificar se algum radio está selecionado
        
        Args:
            funcao_proxima_tela (Callable): funcao para prosseguir para a proxima tela
            *args (Tuple[tk.StringVar]): Lista de todos os radios a serem verificados
        Returns:
            (str | Callable): Devolve uma mensagem de errado ou a função para a próxima tela
        """
        for i, arg in enumerate(args):
            if arg == 'Nenhuma opção selecionada':
                messagebox.showerror("Erro","Você precisa escolher o campo antes de prosseguir!")
                return False 
        return True

    def layout_de_conexao(self,frame_pertencente:tk.Frame,voltar_a_tela_inicial: Callable[[],None],tela, banco:Banco_de_dados, nome_banco:str, usuario_banco:str, senha_banco:str, email:str, senha:str) -> tk.Entry:
        """Método com o intuito de realizar o layout de conexao
        com o banco de dados (Nome do banco,usuário, senha).add()

        Args:
            frame_pertencente (tk.Frame): Frame em que o layot irá ficar.
            banco (Banco_de_dados): Banco de dados criado pela tela
            voltar_a_tela_inicial (Callable[[],None]): funcao_que retorna para a mesma tela ou apra a tela psoterior
        Returns:
            Tuple[tk.Entry]: retorna os 3 inputs
        """
        frame_conjunto = tk.Frame(frame_pertencente)
        frame_conjunto.pack()
        
        frame_email = tk.Frame(frame_conjunto)
        frame_email.pack(expand=True, fill=tk.X)
        
        frame_senha_email = tk.Frame(frame_conjunto)
        frame_senha_email.pack(expand=True, fill=tk.X)
        
        apresentacao = tk.Label(frame_conjunto, text="Insira as informações do banco")
        apresentacao.pack()

        frame_nome_banco = tk.Frame(frame_conjunto)
        frame_nome_banco.pack(expand=True, fill=tk.X)

        frame_usuario = tk.Frame(frame_conjunto)
        frame_usuario.pack(expand=True, fill=tk.X)

        frame_senha = tk.Frame(frame_conjunto)
        frame_senha.pack(expand=True, fill=tk.X)
        
        # Input de email
        label_email = tk.Label(frame_email, text="Email")
        label_email.pack(side=tk.LEFT, pady=5, padx=10)
        input_email = tk.Entry(frame_email, width=20)
        input_email.pack(side=tk.RIGHT, pady=5, padx=10)
        input_email.insert(0, email)
        
        # Input de senha
        label_senha = tk.Label(frame_senha_email, text="senha do email")
        label_senha.pack(side=tk.LEFT, pady=5, padx=10)
        input_senha_email = tk.Entry(frame_senha_email, width=20)
        input_senha_email.pack(side=tk.RIGHT, pady=5, padx=10)
        input_senha_email.insert(0, senha)
        
        # Input de nome do banco
        label_nome_banco = tk.Label(frame_nome_banco, text="Nome do Banco")
        label_nome_banco.pack(side=tk.LEFT, pady=5, padx=10)
        input_nome_banco = tk.Entry(frame_nome_banco, width=20)
        input_nome_banco.pack(side=tk.RIGHT, pady=5, padx=10)
        input_nome_banco.insert(0, nome_banco)
        # Input de usuário do banco
        label_usuario = tk.Label(frame_usuario, text="Usuario do banco")
        label_usuario.pack(side=tk.LEFT, pady=5, padx=10)
        input_usuario = tk.Entry(frame_usuario, width=20)
        input_usuario.pack(side=tk.RIGHT, pady=5, padx=10)
        input_usuario.insert(0, usuario_banco)
        # Input de senha do bancos
        label_senha = tk.Label(frame_senha, text="Senha do banco")
        label_senha.pack(side=tk.LEFT, pady=5, padx=10)
        input_senha = tk.Entry(frame_senha, width=20)
        input_senha.pack(side=tk.RIGHT, pady=5, padx=10)
        input_senha.insert(0, senha_banco)
        # Botão para conectar com o banco de dados
        
        conectar_ao_banco = lambda:[banco.iniciar(input_usuario.get(),input_senha.get(),input_nome_banco.get()),setattr(tela, "email", input_email.get()),setattr(tela, "senha", input_senha_email.get()), voltar_a_tela_inicial()]
        botao_conexao = tk.Button(frame_conjunto,text="SALVAR", command=conectar_ao_banco)
        botao_conexao.pack(pady=(10,0))
        return input_nome_banco, input_usuario, input_senha
    def configuracoes(self,frame_pertencente:tk.Frame,voltar_a_tela_inicial: Callable[[],None]) -> tk.Entry:
        """Método com o intuito de realizar o layout de conexao
        com o banco de dados (Nome do banco,usuário, senha).add()

        Args:
            frame_pertencente (tk.Frame): Frame em que o layot irá ficar.
            banco (Banco_de_dados): Banco de dados criado pela tela
            voltar_a_tela_inicial (Callable[[],None]): funcao_que retorna para a mesma tela ou apra a tela psoterior
        Returns:
            Tuple[tk.Entry]: retorna os 3 inputs
        """
        frame_conjunto = tk.Frame(frame_pertencente)
        frame_conjunto.pack()
        
        frame_email = tk.Frame(frame_conjunto)
        frame_email.pack(expand=True, fill=tk.X)
        
        frame_senha_email = tk.Frame(frame_conjunto)
        frame_senha_email.pack(expand=True, fill=tk.X)
        
        apresentacao = tk.Label(frame_conjunto, text="Insira as informações do banco")
        apresentacao.pack()

        frame_nome_banco = tk.Frame(frame_conjunto)
        frame_nome_banco.pack(expand=True, fill=tk.X)

        frame_usuario = tk.Frame(frame_conjunto)
        frame_usuario.pack(expand=True, fill=tk.X)

        frame_senha = tk.Frame(frame_conjunto)
        frame_senha.pack(expand=True, fill=tk.X)
        
        # Input de email
        label_email = tk.Label(frame_email, text="Email")
        label_email.pack(side=tk.LEFT, pady=5, padx=10)
        input_email = tk.Entry(frame_email, width=20)
        input_email.pack(side=tk.RIGHT, pady=5, padx=10)
        input_email.insert(0, '')
        
        # Input de senha
        label_senha = tk.Label(frame_senha_email, text="senha do email")
        label_senha.pack(side=tk.LEFT, pady=5, padx=10)
        input_senha_email = tk.Entry(frame_senha_email, width=20)
        input_senha_email.pack(side=tk.RIGHT, pady=5, padx=10)
        input_senha_email.insert(0, '')
        
        # Input de nome do banco
        label_nome_banco = tk.Label(frame_nome_banco, text="Nome do Banco")
        label_nome_banco.pack(side=tk.LEFT, pady=5, padx=10)
        input_nome_banco = tk.Entry(frame_nome_banco, width=20)
        input_nome_banco.pack(side=tk.RIGHT, pady=5, padx=10)
        input_nome_banco.insert(0, '')
        # Input de usuário do banco
        label_usuario = tk.Label(frame_usuario, text="Usuario do banco")
        label_usuario.pack(side=tk.LEFT, pady=5, padx=10)
        input_usuario = tk.Entry(frame_usuario, width=20)
        input_usuario.pack(side=tk.RIGHT, pady=5, padx=10)
        input_usuario.insert(0, '')
        # Input de senha do bancos
        label_senha = tk.Label(frame_senha, text="Senha do banco")
        label_senha.pack(side=tk.LEFT, pady=5, padx=10)
        input_senha = tk.Entry(frame_senha, width=20)
        input_senha.pack(side=tk.RIGHT, pady=5, padx=10)
        input_senha.insert(0, '')
        # Botão para conectar com o banco de dados
        
        conectar_ao_banco = lambda: print('')
        botao_conexao = tk.Button(frame_conjunto,text="SALVAR", command=conectar_ao_banco)
        botao_conexao.pack(pady=(10,0))
        return input_nome_banco, input_usuario, input_senha

    def link(self, texto_link:tk.Label, link):
        """
        Abre um navegador da web para o link fornecido quando o rótulo é clicado.

        Parâmetros:
        texto_link (tk.Label): O widget de rótulo que será clicado para abrir o link.
        link (str): A URL a ser aberta no navegador da web.

        Retorna:
        None
        """
        import webbrowser
        texto_link.config(foreground='blue', underline=True)
        texto_link.bind("<Button-1>", lambda event: webbrowser.open(link))

