import socket

def protocol_header(type, username_length):
    return type.to_bytes(1, "big") + username_length.to_bytes(1, "big")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001

client_address = '0.0.0.0'
client_port = int(input("please input server port: "))

#すでにほかのクライアントにポートが使われていた時
try:
    client_socket.bind((client_address, client_port))
except OSError as e:
    print(f"Error: {e}. Please choose a different port.")
    exit()


username = input("please username(max:255): ")
#ユーザー名の長さがオーバーしたとき
if len(username) > 255:
    print("username exceeds the maximum value.")
    exit()
    
regist = "regist"
header = protocol_header(len(regist), len(username))

#ヘッダーを送信
client_socket.sendto(header, (server_address, server_port))

#ユーザー名を送信
client_socket.sendto(username.encode('utf-8'), (server_address, server_port))


while True:
    message = input('send message: ')
    client_socket.sendto(message.encode('utf-8'), (server_address, server_port))
    responseData = client_socket.recv(4096).decode('utf-8')
    print(responseData)