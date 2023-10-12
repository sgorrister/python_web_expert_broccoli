import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)
message = input("Введіть текст для сервера: ")
client_socket.sendall(message.encode('utf-8'))
client_socket.close()
