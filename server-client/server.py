import socket, tqdm, os


HOST = "localhost"
PORT = 50000

BUFFER_SIZE = 1024
SEPARATOR = ","

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print("Aguardando ...")
conn, address = s.accept()

# receive the file infos
# receive using client socket, not server socket
received = conn.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

print("conectado em", address)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(
    range(filesize),
    f"Receiving {filename}",
    unit="B",
    unit_scale=True,
    unit_divisor=1024,
)
with open(f"archive\{filename}", "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = conn.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
conn.close()
# close the server socket
s.close()
