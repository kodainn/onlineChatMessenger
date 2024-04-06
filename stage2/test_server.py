import socket

def server():
    # サーバーソケットの作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # ホストとポートの指定
    host = '127.0.0.1'
    port = 12345
    
    # サーバーソケットを指定のホストとポートにバインド
    server_socket.bind((host, port))
    
    # サーバーの待ち受けを開始
    server_socket.listen()
    

    
    # クライアントからの接続を待ち受け
    client_socket, client_address = server_socket.accept()
    print(client_address)
    print(f"{client_address} が接続しました。")
    
    # クライアントからのデータを受信
    data, address = client_socket.recvfrom(1024)
    
    # クライアントにメッセージを送信
    client_socket.sendall(b"aaaaaaaa")
    
    # ソケットのクローズ
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    server()
