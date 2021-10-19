import socket
from _thread import *
import sys

server = "192.168.178.30"  # local address for now
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


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


pos = [(0,0), (100,100)]


def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("disconnected")
                break
            else:
                if player == 1:  # TODO: extend to 4 players
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("received: ", data)
                print("sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))

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
