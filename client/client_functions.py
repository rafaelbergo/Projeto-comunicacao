import base64
import json
import os
import socket
from dotenv import load_dotenv 
from cryptography.fernet import Fernet
import pandas as pd

load_dotenv() 

def conectar(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server_address = (server_ip, 18000)
    
    try:
        client_socket.connect(server_address)  
        return client_socket
    except socket.error as e:
        print(f'Erro ao conectar ao servidor: {e}')
        return None
    
def desconectar(client_socket):
    client_socket.close()
    print('Desconectado do servidor')

def receber_mensagem(client_socket):
    try:
        dados_json = client_socket.recv(8096).decode()
        if dados_json:
            dados = json.loads(dados_json)

            opcao = dados.get('opcao')  
            mensagem = dados.get('mensagem')

            if opcao is not None and mensagem is not None:
                return opcao, mensagem
            else:
                return None, None
        else:
            return None, None

    except Exception as e:
        return None, None


def escolhe_opcao(opcao, mensagem, atualizaCampo, criaGrafico):
    
    if opcao == 1:  # Caso para mensagem, mensagem criptografada, mensagem em binário e mensagem com algoritmo
        atualizaCampo('REC_MSG_ALG', mensagem)
        criaGrafico(mensagem)
        mensagem2 = removeAlgoritmo_8b6T(mensagem)
        atualizaCampo('REC_MSG_BIN', mensagem2)
        mensagem3 = desconverteBinario(mensagem2) 
        atualizaCampo('REC_MSG_CRIPTO', mensagem3) 
        mensagem4 = descriptografaFernet(mensagem3)  
        atualizaCampo('REC_MSG', mensagem4)
        return
    
    elif opcao == 2:  # Caso para mensagem criptografada, mensagem em binário e mensagem com algoritmo
        atualizaCampo('REC_MSG_ALG', mensagem)
        criaGrafico(mensagem)
        mensagem2 = removeAlgoritmo_8b6T(mensagem)
        atualizaCampo('REC_MSG_BIN', mensagem2)
        mensagem3 = desconverteBinario(mensagem2)
        atualizaCampo('REC_MSG_CRIPTO', mensagem3)
        mensagem4 = descriptografaFernet(mensagem3)  
        atualizaCampo('REC_MSG', mensagem4)  
        return
    
    elif opcao == 3:  # Caso para mensagem em binário e mensagem com algoritmo
        atualizaCampo('REC_MSG_ALG', mensagem)
        criaGrafico(mensagem)
        mensagem2 = removeAlgoritmo_8b6T(mensagem)
        atualizaCampo('REC_MSG_BIN', mensagem2)
        mensagem3 = desconverteBinario(mensagem2)
        atualizaCampo('REC_MSG', mensagem3)
        return  
    
    elif opcao == 4:  # Caso para mensagem com algoritmo somente
        atualizaCampo('REC_MSG_ALG', mensagem)
        criaGrafico(mensagem)
        mensagem2 = removeAlgoritmo_8b6T(mensagem)
        atualizaCampo('REC_MSG_BIN', mensagem2)
        mensagem3 = desconverteBinario(mensagem2)
        atualizaCampo('REC_MSG', mensagem3)
        return
    
    elif opcao == 5:  # Caso para mensagem somente
        atualizaCampo('REC_MSG', mensagem)  
        return
    
    elif opcao == 6:  # Caso para mensagem criptografada somente
        atualizaCampo('REC_MSG_CRIPTO', mensagem)
        mensagem2 = descriptografaFernet(mensagem)
        atualizaCampo('REC_MSG', mensagem2) 
        return
    
    elif opcao == 7:  # Caso para mensagem em binário somente
        atualizaCampo('REC_MSG_BIN', mensagem)
        mensagem = desconverteBinario(mensagem)
        atualizaCampo('REC_MSG', mensagem) 
        return 
    
    elif opcao == 8:  # Caso vazio
        return
    
    elif opcao == 9:  # Caso para mensagem e mensagem criptografada
        atualizaCampo('REC_MSG_CRIPTO', mensagem)  
        mensagem2 = descriptografaFernet(mensagem) 
        atualizaCampo('REC_MSG', mensagem2) 
        return
    
    elif opcao == 10:  # Caso para mensagem e mensagem em binário
        atualizaCampo('REC_MSG_BIN', mensagem)  
        mensagem = desconverteBinario(mensagem) 
        atualizaCampo('REC_MSG', mensagem) 
        return
    
    elif opcao == 11:  # Caso para mensagem, mensagem em binario e mensagem com algoritmo
        atualizaCampo('REC_MSG_ALG', mensagem)
        criaGrafico(mensagem)
        mensagem2 = removeAlgoritmo_8b6T(mensagem)
        atualizaCampo('REC_MSG_BIN', mensagem2)
        mensagem3 = desconverteBinario(mensagem2)
        atualizaCampo('REC_MSG', mensagem3)
        return
    
    elif opcao == 12:  # Caso para mensagem, mensagem criptografada e mensagem em binário
        atualizaCampo('REC_MSG_BIN', mensagem)
        mensagem2 = desconverteBinario(mensagem)  
        atualizaCampo('REC_MSG_CRIPTO', mensagem2)  
        mensagem3= descriptografaFernet(mensagem2)  
        atualizaCampo('REC_MSG', mensagem3)
        return
    
    elif opcao == 13:  # Caso para mensagem criptografada e mensagem em binário
        atualizaCampo('REC_MSG_BIN', mensagem)  
        mensagem2 = desconverteBinario(mensagem)  
        atualizaCampo('REC_MSG_CRIPTO', mensagem2) 
        mensagem3 = descriptografaFernet(mensagem2)
        atualizaCampo('REC_MSG', mensagem3)
        return
    
    if opcao == 14:  # Caso para mensagem em binario e mensagem com algoritmo
        atualizaCampo('REC_MSG_ALG', mensagem)
        criaGrafico(mensagem)
        mensagem2 = removeAlgoritmo_8b6T(mensagem)
        atualizaCampo('REC_MSG_BIN', mensagem2)
        return
    
    if opcao == 15:  # Caso para mensagem e mensagem com algoritmo
        atualizaCampo('REC_MSG_ALG', mensagem)
        criaGrafico(mensagem)
        mensagem2 = removeAlgoritmo_8b6T(mensagem)
        mensagem3 = desconverteBinario(mensagem2)
        atualizaCampo('REC_MSG', mensagem3)
        return
    
    else:
        return

def descriptografaFernet(mensagem_criptografada):
    keyENV = os.getenv('KEY')
    key = base64.b64decode(keyENV)
    cipher = Fernet(key)
    mensagem = cipher.decrypt(mensagem_criptografada.encode()).decode()
    return mensagem

def desconverteBinario(mensagem_binaria):
    mensagem = ''.join(chr(int(b, 2)) for b in mensagem_binaria.split(' '))
    return mensagem

def removeAlgoritmo_8b6T(mensagem):
    decoded_binary = '' 
    
    table = pd.read_csv('8B6T.csv')
    
    table['Binary'] = table['Binary'].apply(lambda x: str(x).strip().zfill(8))
    groups = mensagem.split(' ')
    
    for group in groups:
        matching_row = table[table['Value'] == group]
        
        if not matching_row.empty:
            binary_value = matching_row['Binary'].iloc[0]
            decoded_binary += binary_value

    spaced_binary = ' '.join([decoded_binary[i:i+8] for i in range(0, len(decoded_binary), 8)])
    
    return spaced_binary