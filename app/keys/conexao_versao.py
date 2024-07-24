import firebase_admin
import os
import google.auth.exceptions
import requests
from firebase_admin import credentials, db
from tkinter import messagebox
import psutil

def conexao(banco:str,versao:str, admin:bool):
    try:
        # Verificar se o aplicativo Firebase já foi inicializado
        if not firebase_admin._apps:
            # Caminho para o arquivo de configuração baixado do Firebase
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            # Caminho absoluto para o arquivo de credenciais
            caminho_absoluto = os.path.join(diretorio_atual, 'cred', 'matheus-solutions-firebase-adminsdk-1wjyx-583b5a3a87.json')
            cred = credentials.Certificate(caminho_absoluto)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://matheus-solutions-default-rtdb.firebaseio.com/'
            })
        if admin:
            mac_address = 'admin'
        else:
            mac_address = get_mac_address()
        
        # Referência para o nó (ou caminho) no banco de dados
        ref = db.reference(f'{banco}/versoes')
        ref_certificado = db.reference(f'{banco}/certificados')
        certificados = ref_certificado.get()
        dicio = ref.get()
        
        if mac_address not in certificados:
            messagebox.showerror("Dispositivo inválido", f"Você não possui licença para este dispositivo, entre em contato com o administrador para adiquirir a licença\n\nSeu código: {mac_address}")
            return False
        else:
            if dicio["atual"] == versao:
                print("Permitido")
                return True
            else:
                antigos = dicio["antigas"]
                if versao in antigos:
                    print("Permitido, mas antigo")
                    messagebox.showwarning("Versão desatualizada", f"Você está utilizando uma versão antiga, entre em contato com o administrador antes que sua versão expire.\nSua versão: {versao}\nversão atual: {dicio["atual"]}")
                    return True
                else:
                    messagebox.showerror("Versão descontinuada", f"Você está utilizando uma versão descontinuada, entre em contato com o administrador para adiquirir a nova versão\nSua versão: {versao}\nversão atual: {dicio["atual"]}")
                    print("Não permitido")
                    return False

    except requests.exceptions.ConnectionError as e:
        print("Erro de conexão: ", e)
        return messagebox.showerror("Erro", "Você precisa estar conectado a internet!")
    except google.auth.exceptions.TransportError as e:
        print("Erro de transporte: ", e)
        return messagebox.showerror("Erro", "Você precisa estar conectado a internet!")
    except Exception as e:
        print("Ocorreu um erro: ", e)
        return messagebox.showerror("Erro", "Você precisa estar conectado a internet!")


def get_mac_address():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK and interface != 'lo':
                return addr.address
    return None

# teste = conexao()
# print(teste)

# Escrever dados no Firebase
# ref.set({
#     'name': 'John Doe',
#     'age': 30,
#     'email': 'john.doe@example.com'
# })

# Ler dados do Firebase
# data = ref.get()
# print(data)
