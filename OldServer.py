# # This is a sample Python script.
# import socket
# import time
# from _thread import *
# import threading
#
# from threading import Thread
#
# # połączyć z c&c
# # do każdego ataku inne ip
# # wysłać komunikat o rozpoczęciu ataku
#
#
# print_lock = threading.Lock()
#
#
# # lauch when botmaster is connected
# def thread_for_botmaster(c, addr):
#     print('Botmaster Connected')
#     ip = str(c.recv(16).decode())
#     print('received target ip=' + ip)
#
#
#
# # thread function
# def threaded(c, addr):
#     while True:
#         # data received from client
#         try:
#             c.send('1'.encode())
#             time.sleep(0.5)
#             c.send('192.168.100.8'.encode())
#         except:
#             print("Bot is disconnected")
#             c.close()
#
#         # connection closed
#         if not data:
#             print('Bye')
#
#             # lock released on exit
#             print_lock.release()
#             break
#     c.close()
#
#
# if __name__ == '__main__':
#
#     host = "127.0.0.1"
#     port = 65432
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((host, port))
#     print("socket binded to port", port)
#
#     # put the socket into listening mode
#     s.listen(5)
#     print("socket is listening")
#     f=0
#     # a forever loop until client wants to exit
#     while True:
#         # establish connection with client
#         c, addr = s.accept()
#         data = c.recv(1).decode()
#         print('otrzymano:'+data)
#         if int(data) == 1:
#             print('normal bot connected')
#             f = 1
#         if int(data) == 2:
#             print('botmaster connected')
#             f = 2
#
#         # else:
#         #     f = 0
#         #     print("error")
#         #     continue
#
#         # lock acquired by client
#         print_lock.acquire()
#         print('Connected to :', addr[0], ':', addr[1])
#
#         # Start a new thread and return its identifier
#         if f == 1:
#             th = start_new_thread(threaded, (c, addr))
#         elif f == 2:
#             start_new_thread(thread_for_botmaster, (c, addr))
#
#     s.close()
