import subprocess, time, os

# Connect to OpenVPN
def main():
    subprocess.call(['connect.bat'])
    time.sleep(15) # adjust your connection time
    print("Connect OpenVPN")


def create_file():
    with open("connect.bat", 'w+') as file:
        file.write(r'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --command connect client.ovpn')


# # Disconnect from OpenVPN
# subprocess.call([r'filepath\ovpn_disconnect.bat'])
# print("Disconnect OpenVPN")

if __name__ == "__main__":
    main()