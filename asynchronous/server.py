import random
import json
import socket
import numpy as np

serv_ip = "127.0.0.1"
serv_port = 9090
sync = 0
req_ack = 1
resp_res = 2
req_inv = 1
req_res = 2

res = dict()
def send_error(conc, msg):
    reply = json.dumps({"error": msg})
    conc.send(reply.encode())

def add(x, y):
    return x + y
def sort(array):
    return sorted(array)

def prot(conc, request):
    request = json.loads(request)
    if "rpc_type" not in request:
        send_error(conc, "no rpc type sent in last message")
    if request["rpc_type"] == 1:
        async_proc(conc, request)
    elif request["rpc_type"] == 2:
        def_proc(conc, request)


def async_proc(conc, request):
    if request["request_type"] == req_inv:
        token = random.randint(1, 10000)
        f = globals().get(request["function"])
        if not f:
            send_error(conc, "invalid function")
            return
        reply = json.dumps({"response_type": 1, "token": token})
        conc.send(reply.encode())
        try:
            result = f(*request["args"])
            res[token] = result
        except Exception:
            send_error(conc, "error while executing function")
    elif request["request_type"] == req_res:
        token = int(request["token"])
        result = res[token]
        reply = json.dumps({"result": result, "response_type": resp_res})
        conc.send(reply.encode())
    else:
        send_error(conc, "invalid request type")


def def_proc(conc, request):
    f = globals().get(request["function"])
    if not f:
        send_error(conc, "invalid function")
        return
    try:
        result = f(*request["args"])
        reply = json.dumps({"result": result, "response_type": resp_res})
        conc.send(reply.encode())
    except Exception:
        send_error(conc, "error while executing function")

def main():
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.bind((serv_ip, serv_port))
    skt.listen(10)
    while True:
        conc, _sender_address = skt.accept()
        request = conc.recv(65536).decode()
        prot(conc, request)
        conc.close()

if __name__ == "__main__":
    main()