import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12342)
client_socket.connect(server_address)
while True:
    message = input("Введіть текст для сервера: ")
    client_socket.send(message.encode('utf-8'))
    client_socket.send(str(len(message)).encode('utf-8'))
    data = client_socket.recv(1024).decode('utf-8')
    print('you - {}'.format(data))
    if message == 'exit':
        break

client_socket.close()
