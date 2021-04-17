# Chat-Application-using-TCP-Socket-and-Threads

This chat application makes use of tcp-sockets for client-server communication as well as threads for running an instance for every client.
This application consists of 2 files, **Server.py** and **Client.py**.

### Server.py

For the server file, we'll be using TCP sockets instead of UDP sockets. There is no particular reason as the same thing can be done through UDP sockets as well, but for a messenger application, there is usually a server that decides whether or not to approve or reject the incoming connection. In the current scenario, we're accepting any incoming connection but we have the capability to implement a monitoring feature that decides what to do with the incoming connection.

### Code Description

```python
clients = {}
addresses = {}

BUFSIZ = 1024
ADDR = ('localhost', 5000)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind(ADDR)
```

From the above, people can determine that we're using TCP Sockets because of <code>SOCK_STREAM</code>. Also the socket address, <code>ADDR</code> is a combination of the IP address and the port number. Once we have the address, we bind that address to the socket. That means that when client need to connect to server, they need to refer to the same address

```python
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        connection, client_address = SOCK.accept()
        print("%s:%s has connected." % client_address)
        connection.send("Greetings from the ChatRoom! ".encode("utf8"))
        connection.send("Now type your name and press enter!".encode("utf8"))
        addresses[connection] = client_address
        Thread(target=handle_client, args=(connection, client_address)).start()
```

This is an infinite loop that waits for incoming connection from the clients. As soon as it gets one, it will accept the connection and log some details about the connection. We then store the client address (connection) in the <code>addresses</code> dictionary. Then we allocate and start a thread for that client.

```python
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
```

Once we've welcomed and registered the client, we need to handle its actions. We'll first register his/her name and send a welcome message to that person. In the While loop we'll handle all messages sent by the user. We're using <code>recv()</code> to receive any input from the user. Moreover since the return value of <code>recv()</code> is in bytes, we need to make sure to compare bytes-strings with it, hence the use of <code>bytes()</code>
If the client sends <code>#quit</code>, that means he want to quit. We'll close the connection to the server and delete the instance of that client from out clients dictionary.

```python
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for conn in clients:
        conn.send(bytes(prefix, "utf8") + msg)
```

This function is pretty direct. This will basically circulate any messages sent to all clients. For example, if Client A sends a message and there are 3 clients in total, Client A, B and C. All clients should be able to see what message was sent. The <code>prefix</code> is the just the name of the sender.

```python
if __name__ == "__main__":
    SOCK.listen(5)  # Listens for 5 connections at max.
    print("Chat Server has Started !!")
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SOCK.close()
```

This is the satrting code for out server. It will listen for 5 clients at max but that can be changed if needed. We then start the thread that handles <code>accept_incoming_connections()</code>. In order to prevent the server from closing, we use the <code>join()</code> function. This will act as a hold on any starting thread and they will run infintely unless forced to close.
