import urllib.parse
import threading
import socket
import sys

def newclient(client, addr):
    msg = client.recv(4096).decode('utf-8')
    msg = urllib.parse.unquote(msg).split()
    if msg[1] == '/' and msg[0] == 'POST':
        mainpage = "".join(open('p2/main.html').readlines())
        response = "HTTP/1.1 201 Created\nContent-Type: text/html\n\n" + mainpage
        file = open('order.json', 'w')
        file.write(msg[-1])
        file.close()
        client.send(response.encode('utf-8'))
        client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.getfqdn(), int(sys.argv[1])))
server.listen(10)

while True:
    conn, addr = server.accept()
    th = threading.Thread(target=newclient, args=(conn, addr))
    th.start()
