import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)
server_socket.listen(1)  

print("Сервер слухає на {}:{}".format(*server_address))
client_socket, client_address = server_socket.accept()
print("З'єднано з клієнтом {}:{}".format(*client_address))

data = client_socket.recv(1024).decode('utf-8')
print("Отримано від клієнта: ", data)

client_socket.close()
server_socket.close()
