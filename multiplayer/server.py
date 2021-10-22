import socket
from _thread import *
import pickle
from game import Game

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



connected = set()
games = {}
idCount = 0




def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))  # tell client which player number they are

    reply = ""
    while True:

        try:
            data = conn.recv(4096).decode()  # increase bits in case of pickle error

            if gameId in games:  # games still running or some client disconnected?
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(p, data)  # send move

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print("lost connection")

    try:
        del games[gameId]
        print("closing game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2  # TODO: increase to 4 players for allowing more then one game serverside - might wanna go back to hardcode 4 players for ease
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))

