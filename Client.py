""" Script for Tkinter GUI chat client. """

import tkinter
from tkinter.filedialog import askopenfilename
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def receive():
    """ Handles receiving of messages. """
    while True:
        try:
            msg = sock.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break

def send(event=None):
    """ Handles sending of messages. """
    msg = var.get()
    var.set("")  # Clears input field.
    sock.send(bytes(msg, "utf8"))
    if msg == "#quit":
        sock.close()
        top.quit()

def on_closing(event=None):
    """ This function is to be called when the window is closed. """
    var.set("#quit")
    send()

def smiley_button_tieup(event=None):
    """ Function for smiley button action """
    var.set(":)")
    msg = var.get()  # A common smiley character
    sock.send(bytes(msg, "utf8"))
    var.set("")

def sad_button_tieup(event=None):
    """ Function for smiley button action """
    var.set(":(")    # A common smiley character
    msg = var.get()
    sock.send(bytes(msg, "utf8"))
    var.set("")

def on_enter(e):
    quit_button['background'] = 'red'

def on_leave(e):
    quit_button['background'] = 'white'

def send_file(event=None):
    filename = askopenfilename()
    file = open(filename, "rb")
    SendData = file.read(1024)
    sock.send(SendData)


top = tkinter.Tk()
top.title("Instant Messenger v1.0.0")
messages_frame = tkinter.Frame(top)

var = tkinter.StringVar()
var.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set, bg="darkgray")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack()

messages_frame.pack()

button_label = tkinter.Label(top, text="Enter Message:", background="white")
button_label.pack()
entry_field = tkinter.Entry(top, textvariable=var, foreground="Black")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send, background="white")
send_button.pack(side='left', ipadx=100)
smiley_button = tkinter.Button(top, text=":)", command=smiley_button_tieup)
smiley_button.pack(side='left')
sad_button = tkinter.Button(top, text=":(", command=sad_button_tieup)
sad_button.pack(side='left')

quit_button = tkinter.Button(top, text="Quit", command=on_closing)
quit_button.bind("<Enter>", on_enter)
quit_button.bind("<Leave>", on_leave)
quit_button.pack(side='left', ipadx=100)

sendFile_button = tkinter.Button(top, text="Send File", command=send_file)
sendFile_button.pack(side='left')

top.protocol("WM_DELETE_WINDOW", on_closing)

BUFSIZ = 1024
ADDR = ('localhost', 5000)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.