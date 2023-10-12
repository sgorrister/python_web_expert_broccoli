import socket
import time
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12342)
server_socket.bind(server_address)
server_socket.listen(1)  

print("Сервер слухає на {}:{}".format(*server_address))
while True:
    client_socket, client_address = server_socket.accept()
    print("З'єднано з клієнтом {}:{}".format(*client_address))
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        rozmir = client_socket.recv(1024).decode('utf-8')
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if int(rozmir) == len(data):
            print("Отримано від клієнта: ", data)
            print('when:' + current_time)
            client_socket.send(("Ви надіслали: "+data).encode('utf-8'))
        else:
            print("broken data")
            client_socket.send(("Брокен дата "+data).encode('utf-8'))
        if data == 'exit':
            break
    client_socket.close()
server_socket.close()
