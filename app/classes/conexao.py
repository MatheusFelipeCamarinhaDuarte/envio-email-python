import socket
import threading
class Server():
    from app.classes.janela import Janela
    def __init__(self,janela:Janela):
        ''' Inicializa guardando a tela principal para ser exibida ou ocultada'''
        self.janela = janela
        self.host = 60909
    def iniciar_socket_server(self):
        ''' inicializa um serviço para rodar num localhost específico e próprio da aplicação, e da um comando para quando receber "show" ele mostre a tela principal.'''
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', self.host))
        server.listen(1)
        # cria uma conexão

        while True: # verifica constantemente a conxão para saber se há ou não o envio da mensagem "show"
            conn, addr = server.accept()
            data = conn.recv(1024)
            if data == b'show':
                print('show')
                self.janela.deiconify()
                self.janela.lift()
                self.janela.attributes('-topmost', 1)
                self.janela.focus_force()
                self.janela.attributes('-topmost', 0)
                self.janela.enviador.stop_schedule()
                self.janela.enviador = None
            conn.close()

    def check_if_running(self):
        ''' Faz a verificação tentando envair a mensagem show para o localhost determinado'''
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(('localhost', self.host))
            client.sendall(b'show')
            client.close()
            print('Já existe uma conexão')
            return True
        except ConnectionRefusedError:
            print('não existe conexao')
            return False
    def verificar_conexao(self): 
        '''verifica se já existe uma conexão feita para mandar uma mensagem, e se não existir, cria a conexão'''
        if self.check_if_running():
            return True
        else:
            threading.Thread(target=self.iniciar_socket_server, daemon=True).start()
            return False