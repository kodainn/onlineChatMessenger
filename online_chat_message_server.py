import socket

#クライアントのソケットと名前を紐づけるためのハッシュマップ
clients = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001

server_socket.bind((server_address, server_port))

print('starting socket server')


#ヘッダーを取得して名前のサイズを取得
header, _ = server_socket.recvfrom(1)
username_length = int.from_bytes(header[:1], "big")

#エンコードしてハッシュマップに格納
usernameBytes, client_address = server_socket.recvfrom(username_length)
username = usernameBytes.decode('utf-8')
clients[client_address] = username

try:
    while True:
        client_message_bytes, client_address = server_socket.recvfrom(4096)
        client_message = client_message_bytes.decode('utf-8')
        response_message = clients[client_address] + ": " + client_message
        for client_address, _ in clients.items():
            server_socket.sendto(response_message.encode('utf-8'), client_address)
except Exception as e:
    print('error: ', e)
finally:
    server_socket.close()