import json
import socket
import os
import base64
from dotenv import load_dotenv, dotenv_values 
from cryptography.fernet import Fernet
import pandas as pd

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
        return server_socket, connection, client_address
    except socket.timeout:
        print('Tempo limite de conexão atingido')
        return None, None, None
    
def fechar_conexao(server_socket):
    server_socket.close()
    print('Conexão fechada')

def escolhe_envio(connection, mensagens, flags, atualizaCampo, opcao):
    # Caso para mensagem, mensagem criptografada, mensagem em binário e mensagem com algoritmo
    if flags['chk_msg']: 
        mensagem = mensagens['msg']

        if flags['chk_msg_cripto']:
            mensagem2 = criptografaFernet(mensagem) 
            atualizaCampo('MSG_CRIPTO', mensagem2)

            if flags['chk_msg_bin']:
                mensagem3 = converteBinario(mensagem2)
                atualizaCampo('MSG_BIN', mensagem3)

                if flags['chk_msg_alg']:
                    mensagem4 = aplicaAlgoritmo_8b6T(mensagem3)
                    atualizaCampo('MSG_ALG', mensagem4)
                    #criaGrafico(mensagem4)
                    opcao = 1
                    enviar_mensagem(connection, mensagem4, opcao)
                    return

    # Caso para mensagem criptografada, mensagem em binário e mensagem com algoritmo
    if flags['chk_msg_cripto']:
        mensagem = mensagens['msg_cripto']
        atualizaCampo('MSG_CRIPTO', mensagem)

        if flags['chk_msg_bin']:
            mensagem2 = converteBinario(mensagem)
            atualizaCampo('MSG_BIN', mensagem2)

            if flags['chk_msg_alg']:
                mensagem3 = aplicaAlgoritmo_8b6T(mensagem2)
                atualizaCampo('MSG_ALG', mensagem3)
                criaGrafico(mensagem3)
                opcao = 2
                enviar_mensagem(connection, mensagem3, opcao)
                return

    # Caso para mensagem em binário e mensagem com algoritmo
    if flags['chk_msg_bin']:
        mensagem = mensagens['msg_bin']
        #atualizaCampo('MSG_BIN', mensagem)

        if flags['chk_msg_alg']:
            mensagem2 = aplicaAlgoritmo_8b6T(mensagem)
            atualizaCampo('MSG_ALG', mensagem2)
            criaGrafico(mensagem2)
            opcao = 3
            enviar_mensagem(connection, mensagem2, opcao)
            return


    # Caso para mensagem com algoritmo
    if flags['chk_msg_alg']:
        mensagem = mensagens['msg_alg']
        atualizaCampo('MSG_ALG', mensagem)
        opcao = 4
        enviar_mensagem(connection, mensagem, opcao)
        return
    
    # Caso para mensagem somente
    if flags['chk_msg'] and not flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        atualizaCampo('MSG', mensagem)
        opcao = 5
        enviar_mensagem(connection, mensagem, opcao)
        return
    
    # Caso para mensagem criptografada somente
    if not flags['chk_msg'] and flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg_cripto']
        atualizaCampo('MSG_CRIPTO', mensagem)
        opcao = 6
        enviar_mensagem(connection, mensagem, opcao)

        return
    
    # Caso para mensagem em binário somente
    if not flags['chk_msg'] and not flags['chk_msg_cripto'] and flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg_bin']
        atualizaCampo('MSG_BIN', mensagem)
        opcao = 7
        enviar_mensagem(connection, mensagem, opcao)
        return
    
    # Caso para mensagem com algoritmo somente
    if not flags['chk_msg'] and not flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and flags['chk_msg_alg']:
        mensagem = mensagens['msg_alg']
        atualizaCampo('MSG_ALG', mensagem)
        opcao = 8
        enviar_mensagem(connection, mensagem, opcao)
        return
    
    # Caso para mensagem e mensagem criptografada
    if flags['chk_msg'] and flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        mensagem2 = criptografaFernet(mensagem)
        atualizaCampo('MSG_CRIPTO', mensagem2)
        opcao = 9
        enviar_mensagem(connection, mensagem2, opcao)
        return

    # Caso para mensagem e mensagem em binário
    if flags['chk_msg'] and not flags['chk_msg_cripto'] and flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        mensagem2 = converteBinario(mensagem)
        atualizaCampo('MSG_BIN', mensagem2)
        opcao = 10
        enviar_mensagem(connection, mensagem2, opcao)
        return
    
    # Caso para mensagem, mensagem em binario e mensagem com algoritmo
    if flags['chk_msg'] and not flags['chk_msg_cripto'] and flags['chk_msg_bin'] and flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        print('mensagem', mensagem)
        mensagem2 = converteBinario(mensagem)
        print('bin', mensagem2)
        atualizaCampo('MSG_BIN', mensagem2)
        mensagem3 = aplicaAlgoritmo_8b6T(mensagem2)
        atualizaCampo('MSG_ALG', mensagem3)
        opcao = 11
        print(mensagem2)
        enviar_mensagem(connection, mensagem3, opcao)
        return
    
    # Caso para mensagem, mensagem criptografada e mensagem em binário
    if flags['chk_msg'] and flags['chk_msg_cripto'] and flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        mensagem2 = criptografaFernet(mensagem)
        atualizaCampo('MSG_CRIPTO', mensagem2)
        mensagem3 = converteBinario(mensagem2)
        atualizaCampo('MSG_BIN', mensagem3)
        opcao = 12
        enviar_mensagem(connection, mensagem3, opcao)
        return
    
    # Caso para mensagem criptografada e mensagem em binário
    if not flags['chk_msg'] and flags['chk_msg_cripto'] and flags['chk_msg_bin'] and not flags['chk_msg_alg']:
        mensagem = mensagens['msg_cripto']
        atualizaCampo('MSG_CRIPTO', mensagem)
        mensagem2 = converteBinario(mensagem)
        atualizaCampo('MSG_BIN', mensagem2)
        opcao = 13
        enviar_mensagem(connection, mensagem2, opcao)
        return
    
    # Caso para mensagem em binario e mensagem com algoritmo
    if not flags['chk_msg'] and not flags['chk_msg_cripto'] and flags['chk_msg_bin'] and flags['chk_msg_alg']:
        mensagem = mensagens['msg_bin']
        print("bin: ", mensagem)
        atualizaCampo('MSG_BIN', mensagem)
        mensagem2 = aplicaAlgoritmo_8b6T(mensagem)
        print("alg: ", mensagem2)
        atualizaCampo('MSG_ALG', mensagem2)
        opcao = 14
        enviar_mensagem(connection, mensagem2, opcao)
        return
    
    # Caso para mensagem e mensagem com algoritmo
    if flags['chk_msg'] and not flags['chk_msg_cripto'] and not flags['chk_msg_bin'] and flags['chk_msg_alg']:
        mensagem = mensagens['msg']
        print("msg: ", mensagem)
        mensagem2 = converteBinario(mensagem)
        print("bin: ", mensagem2)
        mensagem3 = aplicaAlgoritmo_8b6T(mensagem2)
        print("alg: ", mensagem3)
        atualizaCampo('MSG_ALG', mensagem3)
        opcao = 15
        enviar_mensagem(connection, mensagem3, opcao)
        return
    
    else:
        return



# Usa o algoritmo de Fernet para criptografar
def criptografaFernet(mensagem): 
    keyENV = os.getenv('KEY')
    key = base64.b64decode(keyENV)
    cipher = Fernet(key)

    mensagem_criptografada = cipher.encrypt(mensagem.encode())

    return mensagem_criptografada.decode()

def converteBinario(mensagem):
    if isinstance(mensagem, bytes):
        mensagem = mensagem.decode('utf-8')

    binario = ' '.join(f'{ord(char):08b}' for char in mensagem)
    return binario

def aplicaAlgoritmo_8b6T(mensagem):
    encoded = ''
    mensagem = mensagem.replace(" ", "") 
    table = pd.read_csv('8B6T.csv')

    table['Binary'] = table['Binary'].apply(lambda x: str(x).strip().zfill(8)) 
    
    for i in range(0, len(mensagem), 8):
        byte = mensagem[i:i+8]
        
        matching_row = table[table['Binary'] == byte]
        if not matching_row.empty:
            encoded += matching_row['Value'].iloc[0] + ' '

    return encoded

def criaGrafico(mensagem):
    pass

def enviar_mensagem(client_socket, mensagem, opcao):
    if client_socket:
        try:
            # Salva os dados no formato de dicionario
            dados = {
                'opcao': opcao,
                'mensagem': mensagem
            }
            dados_json = json.dumps(dados).encode()
            client_socket.sendall(dados_json)

        except socket.error as e:
            print(f'Erro ao enviar mensagem: {e}')
    else:
        if not client_socket:
            print('Conexão fechada')
