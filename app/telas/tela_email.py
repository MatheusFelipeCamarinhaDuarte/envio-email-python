from app.classes.janela import Janela
from app.classes.telas import Telas

class Tela_de_email(Telas):
    def carregar_pagina(self) -> Janela:
        """Janela Principal da aplicação, com o intuito de inciar aplicação e não retornar a está tela novamente.

        Returns:
            tk.Tk: Retorna uma tela Tk.
        """
        
        # Importações
        import tkinter as tk
        import os
        import json
        from app.telas.tela_inicial import Tela_inicial
        from app.classes.utilitarios import Utilitarios
        # Criação da janela principal
        janela_principal = self.janela
        janela_principal.limpar()
        
        # Colocando a linha de apresentação do projeto
        apresentacao = tk.Label(janela_principal, text="Insira seu email")
        apresentacao.pack(anchor=tk.CENTER, expand=True)
        
        # Nome do arquivo CSV
        pasta_atual = Utilitarios().get_caminho_atual()
        pasta_pai = os.path.dirname(pasta_atual)
        
        nome_arquivo = os.path.join(pasta_pai,'data','email.json')

        # Modo de leitura
        with open(nome_arquivo, mode="r", newline="") as arquivo_json:
            dados_email = json.load(arquivo_json)
        
        nome = dados_email["nome_banco"]
        usuario = dados_email["usuario_banco"]
        senha = dados_email["senha_banco"]
        email = dados_email["email"]
        senha_email = dados_email["senha"]
        
        
        tela_anterior = lambda: Tela_inicial(self.janela)
        frame_superior,frame_inferior = janela_principal.duplo_frame(janela_principal)
        proximo = lambda: self.voltar(nome_arquivo,dados_email)
        janela_principal.layout_de_conexao(frame_superior,proximo,self,self.banco,nome,usuario,senha,email,senha_email)
        janela_principal.rodape(frame_inferior,tela_anterior)
        

    def voltar(self,nome_arquivo,arquivo_antigo):
        from app.telas.tela_inicial import Tela_inicial
        from app.classes.utilitarios import Utilitarios
        from tkinter import messagebox
        import json
        
        if self.banco.cursor:
            arquivo_antigo["nome_banco"] = self.banco.banco
            arquivo_antigo["usuario_banco"] = self.banco.usuario
            arquivo_antigo["senha_banco"] = self.banco.senha
            
            if Utilitarios().verifica_email(self.email):
                arquivo_antigo["email"] = self.email
                arquivo_antigo["senha"] = self.senha
                
                
                with open(nome_arquivo, mode="w", newline="") as arquivo_json:
                    json.dump(arquivo_antigo, arquivo_json,indent=4)
                Tela_inicial(self.janela,self.banco)
            else:
                messagebox.showerror('Email inválido', "o endereço de email é inválido")