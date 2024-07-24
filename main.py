from app.keys.conexao_versao import conexao
from tkinter import messagebox
from app.telas.tela_inicial import Tela_inicial
from app.classes.conexao import Server



# 8 da manhã e 8 da noite







def main():
    import os
    # app = Tela_1()
    # janela = app.carregar_pagina()
    # janela.mainloop()
    
    banco = 'email'
    versao = 'v1.0.1'
    admin = False
    
    conectado = conexao(banco,versao, admin)
    if conectado == True:
        print("verificado")
        app = Tela_inicial()
        janela = app.carregar_pagina()

        conexao_existente = Server(janela).verificar_conexao()
        if conexao_existente:
            os._exit(0)

        janela.mainloop()
    elif conectado == False:
        pass
    elif conectado == "certificado_invalido":
        messagebox.showerror("Erro", "Você não possui o certificado para esta aplicação dentro desta máquina.")
    else:
        # Mensagem para caso o certificado não seja válido
        messagebox.showerror("Erro", "Erro desocnhecido, entre em contato com o administrador.")

    
if __name__ == "__main__":
    main()