import socket

HOST = '192.168.0.127'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(str.encode("Hello World"))
data = s.recv(1024)

print("Msg ecoada", data.decode())