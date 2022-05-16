import socket
import pandas as pd

HOST = 'localhost'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print("Aguardando ...")
conn, ender = s.accept()

print("conectado em", ender)
while True:
    data = conn.recv(1024)

    from io import BytesIO

    pd.read_csv(BytesIO(data)).to_csv("archive/" ,index=False)

    if not data:
        print("Closing conn")
        conn.close()
        break
    conn.sendall(data)