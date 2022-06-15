
#Multi-threaded file client supporting UPLOAD, DOWNLOAD, RENAME and DELETE
#Done by Shruthi Sree Thirunavukkarasu (1001933428) and Vandhana Manivannan (1001876764)

import sys
import socket
import base64
import select
from pathlib import Path

serv_ip = "127.0.0.1"
serv_port = 9090


def terminate(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)

def downld(skt, fname):
    msg = "{}\n{}".format("DOWNLOAD", fname)
    skt.sendto(msg.encode(), (serv_ip, serv_port))
    ready = select.select([skt], [], [], 1)[0]
    if ready:
        data = skt.recv(65536)
        Path("Files_downloaded/").mkdir(parents=True, exist_ok=True)
        Path("Files_downloaded/{}".format(fname)).write_bytes(data)
    else:
        terminate("download timeout")
        
def upld(skt, fname):
    file = Path(fname)
    if not file.is_file():
        terminate("Invalid file")
    encoded = base64.b64encode(file.read_bytes()).decode()
    msg = "{}\n{}\n{}".format("UPLOAD", file.name, encoded)
    skt.sendto(msg.encode(), (serv_ip, serv_port))

def ren(skt, fname, newname):
    msg = "{}\n{}\n{}".format("RENAME", fname, newname)
    skt.sendto(msg.encode(), (serv_ip, serv_port))
    
def delt(skt, fname):
    msg = "{}\n{}".format("DELETE", fname)
    skt.sendto(msg.encode(), (serv_ip, serv_port))

def main():
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.connect((serv_ip, serv_port))
    inp = input("Input the action to be performed : upload or download or rename or delete\n")
    fname = input("Input the name of the file to be used for the chosen action\n")
    if inp == "upload":
        upld(skt, fname)
    elif inp == "download":
        downld(skt, fname)
    elif inp == "rename":
        newname= input("Input the new name of the file\n")
        ren(skt, fname, newname)
    elif inp == "delete":
        delt(skt, fname)
    
    skt.close()

if __name__ == "__main__":
    main()