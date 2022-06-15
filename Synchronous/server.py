
#Synchronous RPC server supporting UPLOAD, DOWNLOAD, RENAME and DELETE
#Done by Shruthi Sree Thirunavukkarasu (1001933428) and Vandhana Manivannan (1001876764)

import numpy as np
import sys
import socket
import json

SERVER_IP = "0.0.0.0"
SERVER_PORT = 9090

def protocol(link, request):
    request = json.loads(request)
    f = globals().get(request["func"])
    if not f:
        send_error(link, "invalid function")
        return
    try:
        result = f(*request["args"])
        # send the result back
        reply = json.dumps({"result": result})
        link.send(reply.encode())
    except Exception:
        send_error(link, "Error while executing function")

def send_error(link, msg):
    reply = json.dumps({"error": msg})
    link.send(reply.encode())

def sort(array):
    return sorted(array)

def add(x, y):
    return x + y

def main():
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.bind((SERVER_IP, SERVER_PORT))
    skt.listen(5)
    while True:
        link, _sender_address = skt.accept()
        request = link.recv(65536).decode()
        protocol(link, request)
        link.close()


if __name__ == "__main__":
    main()