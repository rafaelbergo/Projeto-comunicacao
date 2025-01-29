import socket

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
