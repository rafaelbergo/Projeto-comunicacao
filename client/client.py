import socket

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    message = "Olá, servidor!"
    client_socket.send(message.encode())
    print(f"Mensagem enviada: {message}")

    response = client_socket.recv(1024)
    print(f"Resposta do servidor: {response.decode()}")

    client_socket.close()

if __name__ == "__main__":
    server_ip = '127.0.0.1' 
    server_port = 18000
    start_client(server_ip, server_port)