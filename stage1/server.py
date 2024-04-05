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
        client_message_bytes, send_client_address = server_socket.recvfrom(4096)
        client_message = client_message_bytes.decode('utf-8')

        #新規のクライアントに対する処理
        if send_client_address not in clients:
            clients[send_client_address] = {
                'username': client_message,
                'last_visited_time':  datetime.now(),
                'exists': True
            }
            print('session in user: ' + clients[send_client_address]['username'])
            continue

        #セッションが切れてしまったユーザー
        if not(clients[send_client_address]['exists']):
            continue

        #送信者の最終更新時間からセッションを維持するか判定
        time_difference = datetime.now() - clients[send_client_address]['last_visited_time']
        if time_difference.seconds > 60:
            clients[send_client_address]['exists'] = False
            print('session out user: ' + client_info['username'])
            continue
            
        if client_message:
            #メッセージを送信したユーザーの最終更新日時を更新
            clients[send_client_address]['last_visited_time'] = datetime.now()

            response_message = clients[send_client_address]['username'] + ": " + client_message
            for receive_client_address, client_info in clients.items():
                #しばらく更新が無かったユーザーを削除
                time_difference = datetime.now() - client_info['last_visited_time']
                if time_difference.seconds > 60:
                    clients[send_client_address]['exists'] = False
                    print('session out user: ' + client_info['username'])
                    continue
                #送信者にはリレーしない
                if send_client_address == receive_client_address:
                    continue
                server_socket.sendto(response_message.encode('utf-8'), receive_client_address)
except Exception as e:
    print('error: ', e)
finally:
    server_socket.close()