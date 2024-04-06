import socket

def client():
    # クライアントソケットの作成
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # サーバーのホスト名とポート番号
    server_host = '127.0.0.1'
    server_port = 12345
    
    # サーバーに接続
    client_socket.connect((server_host, server_port))
    
    # サーバーにメッセージを送信
    message = "aaaaaaaaa"
    client_socket.sendall(message.encode())
    
    # サーバーからのレスポンスを受信
    data = client_socket.recv(1024)
    print(f"aaaaaaaaa: {data.decode()}")
    
    # ソケットのクローズ
    client_socket.close()

if __name__ == "__main__":
    client()
