from app.classes.janela import Janela
from app.classes.telas import Telas

class Tela_de_historico(Telas):
    def carregar_pagina(self) -> Janela:
        """Janela Principal da aplicação, com o intuito de inciar aplicação e não retornar a está tela novamente.

        Returns:
            tk.Tk: Retorna uma tela Tk.
        """
        
        # Importações
        import tkinter as tk
        from app.telas.tela_inicial import Tela_inicial
        # Criação da janela principal
        janela_principal = self.janela
        janela_principal.limpar()
        
        # Colocando a linha de apresentação do projeto
        apresentacao = tk.Label(janela_principal, text="Histórico de emails")
        apresentacao.pack(anchor=tk.CENTER, expand=True)
        
        # Colocando a linha de inícia do código em si. Uma vez colocado, ele não volta para cá
        # email = lambda: self.tela_email()
        # button = tk.Button(janela_principal, text="Trocar email", width=10,height=1, command=email)
        # button.pack(anchor=tk.CENTER, expand=True)

        # config = lambda: self.tela_email()
        # button = tk.Button(janela_principal, text="Configurações", width=10,height=1, command=config)
        # button.pack(anchor=tk.CENTER, expand=True)
        frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
        tela_anterior = lambda: Tela_inicial(self.janela,self.banco)
        janela_principal.rodape(frame_inferior,tela_anterior)
        
