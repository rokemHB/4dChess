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

def threaded_client(conn):
    conn.send(str.encode("connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)  # amount of information to retrieve
            reply = data.decode("utf-8")

            if not data:
                print("disconnected")
                break
            else:
                print("received: ", reply)
                print("sending: ", reply)

            conn.sendall(str.encode(reply))

        except:
            break

    print("lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("connected to: ", addr)

    start_new_thread(threaded_client, (conn,))

#34