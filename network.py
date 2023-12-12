import socket
import pickle



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.16.163"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.load(self.client.recv(2048))
        except (socket.error, pickle.UnpicklingError) as e:
            print(f"Connection error: {e}")
            return None

    def send(self, data):
        try: 
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
n = Network()
print(n.send("Hello"))
print(n.send("working"))