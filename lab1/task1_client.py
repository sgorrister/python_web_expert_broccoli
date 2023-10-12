import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12342)
client_socket.connect(server_address)
message = input("Введіть текст для сервера: ")
client_socket.send(message.encode('utf-8'))
data = client_socket.recv(1024).decode('utf-8')
print('you - {}'.format(data))
client_socket.close()
