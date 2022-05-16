import os, platform, psutil, socket
import tqdm
import pandas as pd

from demo_minio import push_to_minio


def main():
    os.system("cls")

    my_system = platform.uname()
    memory = list(psutil.virtual_memory())

    df = pd.DataFrame(
        [
            [
                os.getlogin(),
                f"{my_system.system} {my_system.release}",
                str(memory[0])[:2],
            ]
        ],
        columns=["User", "Sys", "RAM"],
    )

    filename = f"archive\{my_system.node}-infosys.csv"

    df.to_csv(f"{filename}", index=False)

    return filename


def send_df_to_server():
    SEPARATOR = ","
    BUFFER_SIZE = 4096

    filename = main()
    filesize = os.path.getsize(filename)

    HOST = "127.0.0.1"
    PORT = 50000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    progress = tqdm.tqdm(
        range(filesize),
        f"Sending {filename}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )

    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the socket
    s.close()


if __name__ == "__main__":
    send_df_to_server()