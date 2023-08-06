import socket,time
from multiprocessing import Pool
from threading import Thread

from queue import Queue



class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()


class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
    
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list,target,open_ports):
        for args in args_list:
            self.add_task(func, args,target,open_ports)
    def wait_completion(self):
        self.tasks.join()



from random import randrange
from time import sleep
target_ip=[]
open_ports=[]
ports=[]

def pscan(port,target,open_ports):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((target,port))
        s.close()
        # print(port)
        open_ports.append(port)
        return port
    except :
        # print(e)
        pass

    


def func(ip,port_range):
    results=[]
    target_ip=str(ip).split(",")
    ports=range(int(str(port_range).split("-")[0]),int(str(port_range).split("-")[1]))
    for target in target_ip:
        open_ports=[]
        start = time.time()
        pool = ThreadPool(100)
        pool.map(pscan, ports,target,open_ports)
        pool.wait_completion()
        print("Time = ", time.time() - start)
        results.append({"Target=":target,"Open_Ports":open_ports,"Time Taken":time.time()-start})
    return results
# print(func("192.168.1.127","0-65000"))


