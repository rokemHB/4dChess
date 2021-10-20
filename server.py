import pickle
import socket
from _thread import *
from player import Player
import pickle


server = "192.168.178.30" #"10.51.1.141"  # local address for now
port = 5555

# AF_INET for ipv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# TODO: change to 4 players later
s.listen(2)

print("waiting for connection, server is running")




# TODO: extend to 4 players
players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("disconnected")
                break
            else:
                if player == 1:  # TODO: extend to 4 players
                    reply = players[0]
                else:
                    reply = players[1]

                print("received: ", data)
                print("sending: ", reply)

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("lost connection")
    conn.close()

currentPlayer = 0  # add connecting players
while True:
    conn, addr = s.accept()
    print("connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
