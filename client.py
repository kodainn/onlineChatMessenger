import socket

class room_tcp_client:
    def __init__(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address: str = 'localhost'
        self.server_port: int = 9001
        self.client_address: str = 'localhost'
        self.client_port: int = 0

        self.room_name_size: int = 0
        self.operation: int = 1
        self.state: int = 0
        self.room_name: str = ''
        self.room_password: str = ''
        self.host_room_token: str = ''
        self.user_name: str = ''
    
    def set_input(self):
        