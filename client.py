import socket
import json
import threading

class TcpClient:
    def __init__(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #クライアントと宛先サーバーのソケット情報
        self.server_address:  str   = 'localhost'
        self.server_port:     int   = 9001
        self.client_address:  tuple = None

        #ボディ情報
        self.room_name:       str = ''
        self.operation:       int = 1
        self.user_name:       str = ''
        self.password:        str = ''
        self.host_room_token: str = ''
        
        #ヘッダー情報
        self.room_name_size:  int = 0
        self.operation_size:  int = 1
        self.user_name_size:  int = 0
        self.password_size:   int = 0
        
        
    
    def set_input(self):
        #ルーム名
        self.room_name       = input('roomname (max_name_len 10): ')
        self.room_name_size  = len(self.room_name)
        if self.room_name_size > 10:
            print('upper limit exceeded.')
            exit()
         
        #操作コード   
        self.operation       = int(input('create room 1, join room 2: '))
        if self.operation != 1 and self.operation != 2:
            print('the choices are 1 or 2.')
            exit()

        #ユーザー名
        self.user_name       = input('username max_name_len 10: ')
        self.user_name_size  = len(self.user_name)
        if self.user_name_size > 10:
            print('upper limit exceeded.')
            exit()
        
        #パスワード 
        self.password        = input('password(max: 20): ')
        self.password_size   = len(self.password)
        if self.password_size > 20:
            print('upper limit exceeded.')
            exit()
        
    def request_message(self) -> str:
        return str(self.room_name_size) + str(self.operation_size) + str(self.user_name_size) + str(self.password_size) + \
                self.room_name + str(self.operation) + self.user_name + self.password
    
    def start(self) -> None:
        try:
            self.socket.connect((self.server_address, self.server_port))
        except socket.socket as err:
            print(err)
            exit()
        
        request_message_bytes: bytes = self.request_message().encode('utf-8')
        self.socket.send(request_message_bytes)
        
        #ルーム作成
        if self.operation == 1:
            
            host_token: str        = self.socket.recv(36).decode('utf-8')
            self.host_room_token   = host_token
            self.client_address    = tuple(json.loads(self.socket.recv(4096).decode('utf-8')))
            
            print('create room success!!!')
            print('host_room_token: ', self.host_room_token)
            
            
        #ルーム参加
        if self.operation == 2:
            self.host_room_token = input('host_token: ')
            self.socket.send(self.host_room_token.encode('utf-8'))
            
            response = self.socket.recv(4096)
            is_room_participation = response[:1].decode('utf-8')
            if is_room_participation == '1':
                client_ddress = response[1:].decode('utf-8')
                self.client_address = tuple(json.loads(client_ddress))
                print("join room ", self.room_name)
            else:
                print('join room fail...')
                self.socket.close()
                exit()
            

class UdpClient:
    def __init__(self, client_address: tuple, room_token: str) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address:            str   = 'localhost'
        self.server_port:               int   = 9001
        self.client_address:            tuple = client_address
        self.room_token:                str   = room_token
        
    def receive_message(self) -> None:
        while True:
            message: str = self.socket.recv(4096).decode('utf-8')
            if message == 'exit':
                print('chatmur closed as the host has left the building.')
            print(message)
        
    def send_message(self) -> None:
        print('please enter your message.\nIf you want to leave, please enter "exit"\n')
        while True:
            input_message: str = input()
            send_message:  str = str(len(input_message)) + input_message + self.room_token
            self.socket.sendto(send_message.encode('utf-8'), (self.server_address, self.server_port))
            
            if input == 'exit':
                print('exited chatmur.')
            
    def start(self) -> None:
        self.socket.bind(self.client_address)
        
        print('------------chat start------------')
        try:
            self.exit_event = threading.Event()
            
            thead_receive_message = threading.Thread(target=self.receive_message)
            thead_send_message    = threading.Thread(target=self.send_message)
            
            thead_receive_message.start()
            thead_send_message.start()
            
            thead_receive_message.join()
            thead_send_message.join()
            
        except Exception as e:
            print('error: ', e)
        finally:
            self.socket.close() 

def main():
    tcp_client = TcpClient()
    tcp_client.set_input()
    tcp_client.start()
    
    udp_client = UdpClient(tcp_client.client_address, tcp_client.host_room_token)
    udp_client.start()
        
  
main()