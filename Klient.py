import socket
import time
import xtelnet

from requests import get

if __name__ == '__main__':

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        while True:
            print('_________________________________________')
            print('| Do you want to start the attack? (Y/N)|')
            print('-----------------------------------------')
            attack = str(input())
            if attack == 'Y' or attack == 'y':
                print('Enter the target IP adddress XXX.XXX.XXX.XXX')
                victimIP = str(input())  # Walidować?
                flag = 0

                while flag != 1:
                    time.sleep(0.5)
                    try:
                        s.connect((HOST, PORT))
                        s.sendall('2'.encode())
                        flag = 1
                    except:
                        flag = 0
                        print('Error: ')
                        continue

                s.send(str(victimIP).encode())
            else:
                continue
            # s.send('2'.encode())
            # data = s.recv(1024)
