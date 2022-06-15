#Synchronous RPC client supporting UPLOAD, DOWNLOAD, RENAME and DELETE
#Done by Shruthi Sree Thirunavukkarasu (1001933428) and Vandhana Manivannan (1001876764)
import sys
import json
import socket
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9090
def protocol(func, args):
    request = {"func": func, "args": args}
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.connect((SERVER_IP, SERVER_PORT))
    skt.send(json.dumps(request).encode())
    resp = skt.recv(65536).decode()
    skt.close()
    resp = json.loads(resp)
    if "error" in resp:
        raise RuntimeError(resp["error"])
    return resp["result"]

def main():
    print("\nadd(1,2)")
    print(protocol("add", args=[1,2]))
    print("\nsort([10,8,6,4,2])")
    print(protocol("sort", args=[[10,8,6,4,2]]))
if __name__ == "__main__":
    main()