import os, platform, psutil, socket, subprocess
from re import sub

import tqdm
import pandas as pd
from cpuinfo import get_cpu_info
import wmi

from conn_opnvpn import connect_openvpn, disconnect_openvpn


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_programs_installed():
    data = subprocess.check_output(["wmic", "product", "get", "name"])
    a = str(data)

    programs_in_machine = []

    # try block
    try:

        # arrange the string
        for i in range(len(a)):
            programs_in_machine.append(a.split("\\r\\r\\n")[6:][i])

    except IndexError as e:
        return ",".join([programs.strip() for programs in programs_in_machine])


def main():
    uname = platform.uname()

    c = wmi.WMI()
    my_system = c.Win32_ComputerSystem()[0]

    svmem = psutil.virtual_memory()

    hd_info = (
        subprocess.check_output(["wmic", "diskdrive", "get", "model"])
        .decode("utf-8")
        .split("\n")
    )

    programs = get_programs_installed()

    df = pd.DataFrame(
        [
            [
                uname.node,
                os.getlogin(),
                my_system.Manufacturer,
                my_system.Model,
                get_cpu_info()["brand_raw"],
                get_size(svmem.total),
                hd_info[1].split("\r")[:-2][0].strip(),
                f"{uname.system} {uname.release}",
                programs,
            ]
        ],
        columns=[
            "machine_name",
            "last_user",
            "manufacturer",
            "model",
            "cpu",
            "memory",
            "disk_drive",
            "so",
            "programs_installed",
        ],
    )

    filename = f"archive\{uname.node}-infosys.csv"

    df.to_csv(f"{filename}", index=False)

    return filename


def send_csv_to_server():
    connect_openvpn()

    SEPARATOR = ","
    BUFFER_SIZE = 4096

    filename = main()
    filesize = os.path.getsize(filename)

    HOST = "DESKTOP-QPNNSCN"
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
    disconnect_openvpn()


if __name__ == "__main__":
    send_csv_to_server()
