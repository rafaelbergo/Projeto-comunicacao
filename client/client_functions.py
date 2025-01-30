import socket

def conectar(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server_address = (server_ip, 18000)
    
    try:
        client_socket.connect(server_address)  
        print(f'Conectado ao servidor {server_ip}')
        return client_socket
    except socket.error as e:
        print(f'Erro ao conectar ao servidor: {e}')
        return None
    
def desconectar(client_socket):
    client_socket.close()
    print('Desconectado do servidor')

def receber_mensagem(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        if data:
            print('Mensagem recebida')
            print(f'Mensagem: {data}')
            return data
        return None
    except:
        return None
