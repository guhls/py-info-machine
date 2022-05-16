import os, platform, psutil, socket
import re
import pandas as pd

from demo_minio import push_to_minio

def main():
    os.system("cls")

    my_system = platform.uname()

    print(my_system.node)

    memory = list(psutil.virtual_memory())

    df = pd.DataFrame([[os.getlogin(), f"{my_system.system} {my_system.release}", str(memory[0])[:2]]], columns=["User", "Sys", "RAM"])
    print(df)

    # with open("gustavopc-infosys.csv", 'r') as file:
    #     print(pd.read_csv(file))

    #push_to_minio(df)

    #df.to_csv(f"archive\{my_system.node}-infosys.csv", index=False)

    return df


def send_df_to_server():
    df = main()

    HOST = '127.0.0.1'
    PORT = 50000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(df.to_csv(index=False).encode())
    data = s.recv(1024)

    print("Msg ecoada", data.decode())


if __name__ == "__main__":
    send_df_to_server()