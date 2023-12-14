import socket
from _thread import start_new_thread
import sys
from network import Network
from player import Player
import pickle


server = "192.168.16.163"
port = 5555

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for Connection, Server Started")

players = [Player]

def threaded_client(conn, player):
    global players
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data
            reply = pickle.dumps(players[player])

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer+= 1