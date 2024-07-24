class Utilitarios():
    """Classe com funções utilitárias"""
    def get_caminho_atual(self):
        import os
        import sys
        
        if getattr(sys, 'frozen', False):  # Quando rodando como um executável
            print("executavel")
            caminho_app = os.path.dirname(sys.executable)
        else:  # Quando rodando como um script
            print("vscode")
            caminho_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return caminho_app

    def verifica_email(self, email: str) -> bool:
        import re
        """
        Verifica se o e-mail fornecido é válido.

        Parâmetros:
            email (str): O e-mail a ser verificado.

        Retorna:
            bool: True se o e-mail for válido, False caso contrário.
        """
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None