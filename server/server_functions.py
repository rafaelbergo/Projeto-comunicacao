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

def escolhe_envio(connection, mensagens, flags, atualizaCampo):
    # Caso para mensagem, mensagem criptografada, mensagem em binário e mensagem com algoritmo
    if flags['chk_msg']: 
        mensagem = mensagens['msg']

        if flags['chk_msg_cripto']:
            mensagem2 = criptografaFernet(mensagem) 
            print(f"Mensagem criptografada: {mensagem2}") ##
            atualizaCampo('MSG_CRIPTO', mensagem2)

            if flags['chk_msg_bin']:
                mensagem3 = converteBinario(mensagem2)
                print(f"Mensagem em binário: {mensagem3}") ##
                atualizaCampo('MSG_BIN', mensagem3)

                if flags['chk_msg_alg']:
                    mensagem4 = aplicaAlgoritmo_8b6T(mensagem2)
                    atualizaCampo('MSG_ALG', mensagem4)
                    criaGrafico(mensagem4)
                    #enviar_mensagem(connection, mensagem4)
                    return

    # Caso para mensagem criptografada, mensagem em binário e mensagem com algoritmo
    if flags['chk_msg_cripto']:
        mensagem = mensagens['msg_cripto']
        atualizaCampo('MSG_CRIPTO', mensagem)

        if flags['chk_msg_bin']:
            mensagem2 = converteBinario(mensagem)
            atualizaCampo('MSG_BIN', mensagem2)

            if flags['chk_msg_alg']:
                mensagem3 = aplicaAlgoritmo_8b6T(mensagem)
                atualizaCampo('MSG_ALG', mensagem3)
                criaGrafico(mensagem3)
                #enviar_mensagem(connection, mensagem3)
                return


    # Caso para mensagem em binário e mensagem com algoritmo
    if flags['chk_msg_bin']:
        mensagem = mensagens['msg_bin']
        atualizaCampo('MSG_BIN', mensagem)

        if flags['chk_msg_alg']:
            mensagem2 = aplicaAlgoritmo_8b6T(mensagem)
            atualizaCampo('MSG_ALG', mensagem2)
            criaGrafico(mensagem2)
            #enviar_mensagem(connection, mensagem2)
            return


    # Caso para mensagem com algoritmo
    if flags['chk_msg_alg']:
        mensagem = mensagens['msg_alg']
        atualizaCampo('MSG_ALG', mensagem)
        #enviar_mensagem(connection, mensagem)
        return
    
    # Caso para mensagem somente
    if flags['chk_msg'] and not flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        atualizaCampo('MSG', mensagem)
        enviar_mensagem(connection, mensagem)
        return
    
    # Caso para mensagem criptografada somente
    if not flags['chk_msg'] and flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg_cripto']
        atualizaCampo('MSG_CRIPTO', mensagem)
        enviar_mensagem(connection, mensagem)
        return
    
    # Caso para mensagem em binário somente
    if not flags['chk_msg'] and not flags['chk_msg_cripto'] and flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg_bin']
        atualizaCampo('MSG_BIN', mensagem)
        enviar_mensagem(connection, mensagem)
        return
    
    # Caso para mensagem com algoritmo somente
    if not flags['chk_msg'] and not flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and flags['chk_msg_alg']:
        mensagem = mensagens['msg_alg']
        atualizaCampo('MSG_ALG', mensagem)
        enviar_mensagem(connection, mensagem)
        return
    
    # Caso para mensagem e mensagem criptografada
    if flags['chk_msg'] and flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        mensagem2 = criptografaFernet(mensagem)
        atualizaCampo('MSG_CRIPTO', mensagem2)
        enviar_mensagem(connection, mensagem2)
        return

    # Caso para mensagem e mensagem em binário
    if flags['chk_msg'] and not flags['chk_msg_cripto'] and flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        mensagem2 = converteBinario(mensagem)
        atualizaCampo('MSG_BIN', mensagem2)
        enviar_mensagem(connection, mensagem2)
        return
    
    # Caso para mensagem e mensagem com algoritmo
    if flags['chk_msg'] and not flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        mensagem2 = aplicaAlgoritmo_8b6T(mensagem)
        atualizaCampo('MSG_ALG', mensagem2)
        enviar_mensagem(connection, mensagem2)
        return
    
    else:
        return



# Usa o algoritmo de Fernet para criptografar
def criptografaFernet(mensagem): 
    keyENV = os.getenv('KEY')
    key = base64.b64decode(keyENV)
    cipher = Fernet(key)

    mensagem_criptografada = cipher.encrypt(mensagem.encode())

    return mensagem_criptografada

def converteBinario(mensagem):
    if isinstance(mensagem, bytes):
        mensagem = mensagem.decode('utf-8')

    binario = ' '.join(f'{ord(char):08b}' for char in mensagem)
    return binario.decode()

def aplicaAlgoritmo_8b6T(mensagem): 
    pass

def criaGrafico(mensagem):
    pass

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
