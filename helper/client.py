import xmlrpc.client
import os
import threading
import time

def helper_thread(num):
    print("sync")
    with xmlrpc.client.ServerProxy("http://localhost:9090/") as proxy:
        while(True):
            proxy.file_sync()
            time.sleep(10)
            print("syncing")
def thread_2(num):
    with xmlrpc.client.ServerProxy("http://localhost:9090/") as proxy:
        proxy.rename_file()
        proxy.get_details()
        path_name = 'C:\\Users\\shruthi sree\\Downloads\\Project1_T_V\\HELPER\\client'
        directory_list = os.listdir(path_name)
        print("Files in client",directory_list)
        
if __name__ == "__main__":
    # creating threads
    t1 = threading.Thread(target=helper_thread, args=(1,))
    t2 = threading.Thread(target=thread_2, args=(1,))
  
    # initiating threads
    t1.start()
   