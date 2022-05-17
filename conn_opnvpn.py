import subprocess, time, os


# Connect to OpenVPN
def connect_openvpn():
    os.system(r'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --command silent_connection 1')

    os.system(r'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --command connect client.ovpn')
    time.sleep(15)


# Disconnect to OpenVPN
def disconnect_openvpn():
    os.system(r'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --command disconnect client.ovpn')



if __name__ == "__main__":
    connect_openvpn()