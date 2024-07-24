from abc import ABC, abstractmethod
from tkinter import messagebox
import tkinter as tk

try:
    from app.classes.janela import Janela
except:
    from janela import Janela
    
class Telas(ABC):
    """Classe para importação de arquivo"""
    from app.classes.banco_de_dados import Banco_de_dados
    from app.classes.janela import Janela
    def __init__(self,janela:Janela = None, banco:Banco_de_dados = Banco_de_dados()):
        """Método de criação das telas de importacao"""
        super().__init__()
        # tkinter
        self.tk = tk
        self.banco = banco
        self.email = ''
        self.senha = ''
        # Janela
        if janela:
            self.janela = janela
            self.carregar_pagina()
        else:
            self.janela = Janela()
    @abstractmethod
    def carregar_pagina():
        raise NotImplementedError("Subclasses devem implementar este método.")



                
                
                
                
                
                
                