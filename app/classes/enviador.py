class Email():
    """Classe de enviador do email e suas operações"""
    from typing import Callable, Optional, Tuple, List
    from app.classes.banco_de_dados import Banco_de_dados
    import tkinter as tk
    def __init__(self,email:str,senha:str, banco:Banco_de_dados, aplicacao:tk.Tk):
        ''' inicializa a classe email, fazendo com que 2 vezes ao dia seja feita a verificação de possíveis novos clientes para enviar e-mails'''        
        import schedule
        
        self.email = email
        self.senha = senha
        self.banco = banco
        
        self.parar = False
        self.janela = aplicacao

        # schedule.every().day.at(f"08:00").do(self.job)
        # schedule.every().day.at(f"20:00").do(self.job)
        while True:
            for hora in range(24):
                if hora < 10:
                    hora = f"0{hora}"
                for minuto in range(60):
                    if minuto < 10:
                        minuto = f"0{minuto}"
                    # print(f"{hora}:{minuto}")
                    schedule.every().day.at(f"{hora}:{minuto}").do(self.job)
            break

        self.start_schedule() # Inicializa o conferidor de tempo
        self.esconder() # esconde a tela principal para tudo rodar em segundo plano


    def esconder(self):
        ''' Esconde a tela principal'''
        self.janela.withdraw()


    def run_schedule(self):
        ''' começa a fazer com que o schedule rode constanemente até que a condição parar seja verdadeira'''
        import schedule
        import time
        while not self.parar:
            schedule.run_pending()
            time.sleep(1)


    def start_schedule(self):
        ''' inicializa o schedule para rodar constantemente'''
        import threading
        schedule_thread = threading.Thread(target=self.run_schedule)
        schedule_thread.daemon = True
        schedule_thread.start()


    def stop_schedule(self):
        ''' Faz com que o schedule pare de funcionar'''
        self.parar = True


    def show_message(self):
        ''' Mostra uma mensagem através do tkinter'''
        import tkinter as tk
        from tkinter import messagebox
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta a janela principal
        messagebox.showinfo("Bom dia", "Bom dia!")
        self.root.destroy()  # Destroi a janela principal depois de exibir a mensagem


    def job(self):
        ''' Realiza o trabalho através de busca ons bancos de dados e envio de email'''
        self.show_message()
        for i in range(2):
            self.enviar_email()
        


    def enviar_email(self):
        ''' envia o email com as informações necessárias anexadas a ele'''
        print("email enviado...")