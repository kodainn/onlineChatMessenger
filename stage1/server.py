import socket
from datetime import datetime

#クライアントのソケットと名前を紐づけるためのハッシュマップ
clients = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001

server_socket.bind((server_address, server_port))

print('starting socket server')

try:
    while True:
        client_message_bytes, client_address = server_socket.recvfrom(4096)
        client_message = client_message_bytes.decode('utf-8')

        #新規のクライアントに対する処理
        if client_address not in clients:
            clients[client_address] = {
                'username': client_message,
                'last_visited_time':  datetime.now()
            }
            print('session in user: ' + clients[client_address]['username'])
            continue
            
        if client_message:
            #メッセージを送信したユーザーの最終更新日時を更新
            clients[client_address]['last_visited_time'] = datetime.now()

            response_message = clients[client_address]['username'] + ": " + client_message
            for client_address, client_info in clients.items():
                #しばらく更新が無かったユーザーを削除
                time_difference = datetime.now() - client_info['last_visited_time']
                if time_difference.seconds > 60:
                    clients.pop(client_address)
                    print('session out user: ' + client_info['username'])
                    continue

                server_socket.sendto(response_message.encode('utf-8'), client_address)
except Exception as e:
    print('error: ', e)
finally:
    server_socket.close()