import socket
HOST = '140.112.30.40'
PORT = 13751

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)

while True:
    conn, addr = server.accept()
    file = open('order.json')
    serverMessage = file.readline()
    file.close()
    conn.sendall(serverMessage.encode())
    conn.close()
