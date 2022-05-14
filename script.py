import os
import platform
import psutil
import pandas as pd
import awscli

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

    push_to_minio(df)

    #df.to_parquet(f"D:\{my_system.node}-infosys.csv", index=False)

if __name__ == "__main__":
    main()