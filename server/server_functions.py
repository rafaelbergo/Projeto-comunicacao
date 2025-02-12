import socket
import os
import base64
from dotenv import load_dotenv, dotenv_values 
from cryptography.fernet import Fernet

#from server import atualizaCampo

load_dotenv() 

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip_local = s.getsockname()[0]
    s.close()
    return ip_local

def abrir_conexao():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria a conexão TCP/IP
    server_address = ('0.0.0.0', 18000)  # 0.0.0.0 aceita conexao de qualquer IP 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    
    server_socket.listen(1) # Espera ate o cliente conectar
    server_socket.settimeout(30)

    print('Aguardando conexão...')
    
    try:
        connection, client_address = server_socket.accept()
        print(f'Conexão estabelecida com {client_address}')
        print(connection)
        return server_socket, connection, client_address
    except socket.timeout:
        print('Tempo limite de conexão atingido')
        return None, None, None
    
def fechar_conexao(server_socket):
    server_socket.close()
    print('Conexão fechada')

def escolhe_envio(connection, mensagens, flags):
    #if flags['chk_msg'] and not flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and not flags['chk_msg_alg']:
    if flags['chk_msg']:
        mensagem = mensagens['msg']
        if flags['chk_msg_cripto']:
            mensagem2 = criptografaFernet(mensagem) 
            atualizaCampo('MSG_CRIPTO', mensagem2)


    if flags['chk_msg_cripto']:
        mensagem = mensagens['msg_cripto']



        enviar_mensagem(connection, mensagens['msg'])


# Usa o algoritmo de Fernet para criptografar
def criptografaFernet(mensagem): 
    keyENV = os.getenv('KEY')
    key = base64.b64decode(keyENV)
    cipher = Fernet(key)

    print(f"Mensagem original: {mensagem}")

    # Criptografar a mensagem
    mensagem_criptografada = cipher.encrypt(mensagem.encode())
    print(f"Mensagem criptografada: {mensagem_criptografada}")

    #print("Mensagem criptografada em formato binário (bits):")
    #for byte in mensagem_criptografada:
    #    print(f'{byte:08b}', end=' ')

    #mensagem_descriptografada = cipher.decrypt(mensagem_criptografada).decode()
    #print(f"Mensagem descriptografada: {mensagem_descriptografada}")

    return mensagem_criptografada


def enviar_mensagem(client_socket, mensagem):
    if client_socket:
        try:
            client_socket.sendall(mensagem.encode())
            print('Mensagem enviada')
        except socket.error as e:
            print(f'Erro ao enviar mensagem: {e}')
    else:
        if not client_socket:
            print('Conexão fechada')
