""" Script for TCP chat server - relays messages to all clients """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

BUFSIZ = 1024
ADDR = ('localhost', 5000)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        connection, client_address = SOCK.accept()
        print("%s:%s has connected." % client_address)
        connection.send("Greetings from the ChatRoom! ".encode("utf8"))
        connection.send("Now type your name and press enter!".encode("utf8"))
        addresses[connection] = client_address
        Thread(target=handle_client, args=(connection, client_address)).start()


def handle_client(conn, addr):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = conn.recv(BUFSIZ).decode('utf8')
    welcome = 'Welcome %s! If you ever want to quit, type #quit to exit.' % name
    conn.send(bytes(welcome, "utf8"))
    msg = "%s from [%s] has joined the chat!" % (name, addr[0])
    broadcast(bytes(msg, "utf8"))
    clients[conn] = name
    while True:
        msg = conn.recv(BUFSIZ)
        if msg != bytes("#quit", "utf8"):
            broadcast(msg, name + ": ")
        else:
            conn.send(bytes("#quit", "utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""
    for conn in clients:
        conn.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SOCK.listen(5)
    print("Server has started !!")
    print("Allowing for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SOCK.close()
