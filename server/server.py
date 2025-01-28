import socket


def start_connection():
    host = '0.0.0.0'
    port = 18000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um socket TCP/IP
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Esperando por conexão...")
    conn, addr = server_socket.accept()  
    print(f"Conexão estabelecida com {addr}")

    data = conn.recv(1024)
    print(f"Mensagem recebida: {data.decode()}")

    # Envia uma resposta
    conn.send("Mensagem recebida com sucesso!".encode())

    conn.close()

if __name__ == '__main__':
    start_connection()