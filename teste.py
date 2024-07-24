import tkinter as tk
import socket
import threading
import os

def start_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 65432))
    server.listen(1)

    while True:
        conn, addr = server.accept()
        data = conn.recv(1024)
        if data == b'show':
            root.deiconify()
            root.lift()
        conn.close()

def check_if_running():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 65432))
        client.sendall(b'show')
        client.close()
        print('conectado')
        return True
    except ConnectionRefusedError:
        print('não')
        return False

if check_if_running():
    os._exit(0)
else:
    root = tk.Tk()
    # root.withdraw()

    # Iniciar o servidor de socket em uma thread separada
    threading.Thread(target=start_socket_server, daemon=True).start()
    root.mainloop()
    # Resto do código da sua aplicação
