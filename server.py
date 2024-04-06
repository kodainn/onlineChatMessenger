import socket
import uuid
import threading
import json

class HostUser:
    def __init__(self, host_address: tuple, host_name: str, host_token: str) -> None:
        self.address: tuple = host_address
        self.name:    str   = host_name
        self.token:   str   = host_token
        print("create: host " + self.name)


class MemberUser:
    def __init__(self, member_address: tuple, member_name: str, member_token: str) -> None:
        self.address: tuple  = member_address
        self.name:      str  = member_name
        self.token:     str  = member_token
        print("create: member " + self.name)


class Room:
    def __init__(self, room_name: str, host_user: HostUser, password: str, token: str) -> None:
        self.name:      str                     = room_name
        self.host_user: HostUser                = host_user
        self.password:  str                     = password
        self.token:     str                     = token
        self.members:   dict[tuple ,MemberUser] = {}
        print("create: " + self.name + " host " + self.host_user.name)
    
    def append(self, member_user: MemberUser):
        self.members[member_user.address] = member_user
        print('add: ' + self.name + ' join ' + member_user.name)
        

class RoomList:
    def __init__(self) -> None:
        self.roomlist: dict[str, Room] = {}

    def append(self, room: Room):
        self.roomlist[room.token] = room
    

class TcpServer:
    def __init__(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #クライアントと宛先サーバーのソケット情報
        self.server_address:  str = 'localhost'
        self.server_port:     int = 9001
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.server_address, self.server_port))
        self.socket.listen(1)
        
    def request_transform(self, request_message: str) -> tuple[str, int, str, str]:
        room_name_size:  int = int(request_message[0])
        operation_size:  int = int(request_message[1])
        user_name_size:  int = int(request_message[2])
        password_size:   int = int(request_message[3]) 
        
        request_message: str = request_message[4:]       
        
        room_name:       str = request_message[:room_name_size]
        request_message: str = request_message[room_name_size:]
        operation:       int = int(request_message[:operation_size])
        request_message: str = request_message[operation_size:]
        user_name:       str = request_message[:user_name_size]
        request_message: str = request_message[user_name_size:]
        password:        str = request_message[:password_size]
        
        return (room_name, operation, user_name, password)
        
    
    def start(self, roomlist: RoomList) -> None:
            while True:
                try:
                    connection, client_address = self.socket.accept()
                    request_message: str = connection.recv(4096).decode('utf-8')
                    room_name, operation, user_name, password = self.request_transform(request_message)
                    
                    #ルーム作成
                    if operation == 1:
                        token:       str        = str(uuid.uuid4())
                        host_user:   HostUser   = HostUser(client_address, user_name, token)
                        member_user: MemberUser = MemberUser(client_address, user_name, token)
                        room:        Room       = Room(room_name, host_user, password, token)
                        room.append(member_user)
                        roomlist.append(room)
                        connection.sendall(token.encode('utf-8'))
                        connection.sendall(json.dumps(client_address).encode('utf-8'))
                        
                        
                    #ルーム参加
                    if operation == 2:
                        room_token: str = connection.recv(36).decode('utf-8')
                        if room_token in roomlist.roomlist and password == roomlist.roomlist[room_token].password and room_name == roomlist.roomlist[room_token].name:
                            member_token: str        = str(uuid.uuid4())
                            room:         Room       = roomlist.roomlist[room_token]
                            member_user:  MemberUser = MemberUser(client_address, user_name, member_token)
                            room.append(member_user)
                            #成功を通知
                            responseData = '1' + json.dumps(client_address)
                            connection.sendall(responseData.encode('utf-8'))
                        else:
                            #失敗を通知
                            connection.sendall('0'.encode('utf-8'))
                except Exception as e:
                    print('error: ', e)
                finally:
                    connection.close()


class UdpServer:
    def __init__(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address:  str = 'localhost'
        self.server_port:     int = 9001
    
    def start(self, roomlist: RoomList) -> None:
        self.socket.bind((self.server_address, self.server_port))
        try:
            while True:
                #メッセージとルームトークンを取得する
                client_message_bytes, client_address = self.socket.recvfrom(4096)
                client_message: str = client_message_bytes.decode('utf-8')
                message_length: int = int(client_message[0])
                message:        str = client_message[1:message_length + 1]
                room_token:     str = client_message[message_length + 1:]
                
                #ルームが存在するか確認
                if room_token not in roomlist.roomlist: continue
                #送信者がそのルームに存在するか確認
                room: Room = roomlist.roomlist[room_token]
                if client_address not in room.members: continue
                
                #チャット退出者
                if message == 'exit':
                    #ホストがチャットルームを退出する場合はチャットルーム事削除
                    if room.host_user.address == client_address:
                        #メンバー全員にホスト退出を通知
                        room.members.pop(client_address)
                        for member_address, _ in room.members.items():
                            self.socket.sendto(message.encode('utf-8'), member_address)
                        roomlist.roomlist.pop(room_token)
                        continue
                    else:
                        room.members.pop(client_address)
                        continue

                sender:         str = room.members[client_address].name
                sender_message: str = sender + ": " + message
                for member_address, _ in room.members.items():
                    self.socket.sendto(sender_message.encode('utf-8'), member_address)
                    
        except Exception as e:
            print('error: ', e)
        finally:
            self.socket.close()


def main():
    roomlist:   RoomList  = RoomList()
    tcp_server: TcpServer = TcpServer()
    udp_server: UdpServer = UdpServer()
    
    print('start tcp server')
    
    thead_tcp = threading.Thread(target=tcp_server.start, args=(roomlist, ))
    thead_udp = threading.Thread(target=udp_server.start, args=(roomlist, ))
    
    thead_tcp.start()
    thead_udp.start()
    
    thead_tcp.join()
    thead_udp.join()
    
main()