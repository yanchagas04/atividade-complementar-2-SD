import socket
import threading
from client.handle_client import handle_client

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()
    print("Servidor de Quiz iniciado. Aguardando conexões...")
    
    try:
        while True:
            conn, addr = server_socket.accept()
            # Cria uma nova thread para cada cliente
            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, addr)
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("Desligando servidor...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()