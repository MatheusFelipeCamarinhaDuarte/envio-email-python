import tkinter as tk
from tkinter import messagebox
import schedule
import time
import threading

class Teste():
    
    def __init__(self):
        self.parar = False
        self.root = tk.Tk()
        self.root.title("Aplicação Tkinter")
        # self.esconder()
        # Mantém a janela aberta
        # Botão para iniciar o agendador
        start_button = tk.Button(self.root, text="Iniciar Agendador", command=self.start_schedule)
        start_button.pack(pady=10)

        # Botão para parar o agendador
        stop_button = tk.Button(self.root, text="Parar Agendador", command=self.stop_schedule)
        stop_button.pack(pady=10)
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

        self.root.mainloop()        

    def run_schedule(self):
        while not self.parar:
            schedule.run_pending()
            time.sleep(1)

    def start_schedule(self):
        schedule_thread = threading.Thread(target=self.run_schedule)
        schedule_thread.daemon = True
        schedule_thread.start()

    def stop_schedule(self):
        self.parar = True

    def show_message(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta a janela principal
        messagebox.showinfo("Bom dia", "Bom dia!")
        self.root.destroy()  # Destroi a janela principal depois de exibir a mensagem

    def job(self):
        self.show_message()    

    def esconder(self):
        self.root.withdraw()

if __name__ == "__main__":
    Teste()