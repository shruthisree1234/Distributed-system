
#Multi-threaded file server supporting UPLOAD, DOWNLOAD, RENAME and DELETE
#Done by Shruthi Sree Thirunavukkarasu (1001933428) and Vandhana Manivannan (1001876764)

import sys
import base64
import socket
from threading import Thread
from pathlib import Path

buff_size = 65536
con_limit = 1024
serv_ip = "0.0.0.0"
serv_port = 9090

class wt(Thread):
    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.client_ip = ip
        self.client_port = port
        self.conn = conn
        
    def run(self):
        msg = self.conn.recv(buff_size)
        tokens = msg.split(b"\n", maxsplit=2)
        instruc = tokens[0].decode().strip().lower()

        if instruc == "upload":
            fname = tokens[1].decode().strip()
            file_data = tokens[2]
            Path("Files_uploaded/").mkdir(parents=True, exist_ok=True)
            Path("Files_uploaded/{}".format(fname)).write_bytes(file_data)
            print(f"{self.client_ip}:{self.client_port} - '{fname}' is Uploaded")

        elif instruc == "delete":
            fname = tokens[1].decode().strip()
            file = Path("Files_uploaded/{}".format(fname))
            if file.is_file():
                file.unlink()
                print(f"{self.client_ip}:{self.client_port} - '{fname}' is Deleted")
                
        elif instruc == "download":
            fname = tokens[1].decode().strip()
            file = Path("Files_uploaded/{}".format(fname))
            if file.is_file():
                self.conn.send(file.read_bytes())
                print(f"{self.client_ip}:{self.client_port} - '{fname}' is Downloaded")

        elif instruc == "rename":
            fname = tokens[1].decode().strip()
            newname = tokens[2].decode().strip()
            file = Path("Files_uploaded/{}".format(fname))
            new_file = Path("Files_uploaded/{}".format(newname))
            if file.is_file():
                file.rename(new_file)
                print(f"{self.client_ip}:{self.client_port} - '{fname}' is renamed to '{newname}'")


def main():
    tsk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tsk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tsk.bind((serv_ip, serv_port))
    tsk.listen(con_limit)
    print(f"Server running at {serv_ip}:{serv_port}")
    while True:
        (conn, (client_ip, client_port)) = tsk.accept()
        wkr = wt(client_ip, client_port, conn)
        wkr.start()

if __name__ == "__main__":
    main()