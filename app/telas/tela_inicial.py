from app.classes.janela import Janela
from app.classes.telas import Telas
from app.classes.utilitarios import Utilitarios

class Tela_inicial(Telas):
    def carregar_pagina(self) -> Janela:
        """Janela Principal da aplicação, com o intuito de inciar aplicação e não retornar a está tela novamente.

        Returns:
            tk.Tk: Retorna uma tela Tk.
        """
        
        # Importações
        import tkinter as tk

        # Criação da janela principal
        janela_principal = self.janela
        janela_principal.limpar()        

        # Cria um widget Label para exibir a imagem
        apresentacao = tk.Label(janela_principal, text="Envio de emails automático")
        apresentacao.pack(anchor=tk.CENTER, expand=True)
        
        # Colocando a linha de inícia do código em si. Uma vez colocado, ele não volta para cá
        email = lambda: self.tela_email()
        button = tk.Button(janela_principal, text="Cadastro para envio", width=20,height=1, command=email)
        button.pack(anchor=tk.CENTER, expand=True)

        config = lambda: self.tela_config()
        button = tk.Button(janela_principal, text="Configuração de envios", width=20,height=1, command=config)
        button.pack(anchor=tk.CENTER, expand=True)
        
        iniciar = lambda: self.iniciar()
        button = tk.Button(janela_principal, text="Iniciar automação", width=20,height=1, command=iniciar)
        button.pack(anchor=tk.CENTER, expand=True)
        
        
        janela_principal.rodape(janela_principal)
        
        # Retornando a primeira tela criada
        return janela_principal


    def tela_email(self):
        from app.telas.tela_email import Tela_de_email
        Tela_de_email(self.janela)

    def tela_config(self):
        from app.telas.tela_configuracao import Tela_de_configuracao
        Tela_de_configuracao(self.janela)

    def iniciar(self):
        from app.classes.enviador import Email
        from app.classes.banco_de_dados import Banco_de_dados
        import json
        import os
        
        pasta_atual = Utilitarios().get_caminho_atual()
        print(pasta_atual)
        pasta_pai = os.path.dirname(pasta_atual)
        nome_arquivo = os.path.join(pasta_pai,'data','email.json')
        
        with open(nome_arquivo, mode="r", newline="") as arquivo_json:
            dados_email = json.load(arquivo_json)
        
        if dados_email["email"]:
            nome = dados_email["nome_banco"]
            usuario = dados_email["usuario_banco"]
            senha = dados_email["senha_banco"]
            email = dados_email["email"]
            senha_email = dados_email["senha"]
            banco = Banco_de_dados()
            banco.iniciar(usuario,senha,nome)

            self.janela.enviador = Email(email, senha_email, banco, self.janela)