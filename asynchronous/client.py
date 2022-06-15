
import json
import socket
import sys
import threading
serv_ip = "127.0.0.1"
serv_port = 9090
sync = 0
asynch = 1
defer = 2
req_ack = 1
resp_res = 2
req_inv = 1
req_res = 2


class asynprot:
    def __init__(self, function, args):
        self.function = function
        self.args = args
        self.rpc_type = asynch
        self.computation_id = None
        self.result = None

    def invoke(self):
        request = {
            "function": self.function,
            "args": self.args,
            "rpc_type": self.rpc_type,
            "request_type": req_inv,
        }

        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect((serv_ip, serv_port))
        skt.send(json.dumps(request).encode())
        response = skt.recv(65536).decode()
        response = json.loads(response)
        skt.close()
        if "error" in response:
            raise RuntimeError(response["error"])
        if "response_type" not in response:
            raise RuntimeError("No response type received from server")
        self.computation_id = response["token"]

    def get_result(self):
        request = {
            "rpc_type": self.rpc_type,
            "token": self.computation_id,
            "request_type": req_res,
        }

        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect((serv_ip, serv_port))
        skt.send(json.dumps(request).encode())
        response = skt.recv(65536).decode()
        response = json.loads(response)
        skt.close()
        if "error" in response:
            raise RuntimeError(response["error"])
        if "response_type" not in response:
            raise ValueError("No response type received from server")

        self.result = response["result"]
        return self.result

class defprot:
    def __init__(self, function, args):
        # Assign the argument to the instance's name attribute
        self.function = function
        self.args = args
        self.rpc_type = defer
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.connect((serv_ip, serv_port))
    def get_result(self):
        response = self.skt.recv(65536).decode()
        response = json.loads(response)
        if "error" in response:
            raise RuntimeError(response["error"])
        if "response_type" not in response:
            raise RuntimeError("no response type received from server")
        result = response.get("result")
        if result is None:
            raise RuntimeError("error parsing result")
        return response["result"]
    def __del__(self):
        self.skt.close()
    def invoke(self, par_fn=None, args=[]):
        # pack the parameters
        request = {
            "function": self.function,
            "args": self.args,
            "rpc_type": self.rpc_type,
            "request_type": req_inv,
        }
        self.skt.send(json.dumps(request).encode())
        if par_fn is not None:
            thread = threading.Thread(target=par_fn, args=args)
            thread.start()
        result = self.get_result()
        print(f"The result received from the server: {result}")
        thread.join()
        return result