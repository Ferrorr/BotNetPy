# This is a sample Python script.
import socket

from threading import Thread
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# połączyć z c&c
# do każdego połączenia inne ip
# wysłać komunikat o rozpoczęciu ataku

def new_client(s,addr):
    while True:
        msg = s.recv(1024)
        msg=raw_input('Server>> ')
        s.send(msg)
    s.close()


# import socket programming library
import socket

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()


# thread function
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

        # connection closed
    c.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    host = "127.0.0.1"

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,addr))
    s.close()

