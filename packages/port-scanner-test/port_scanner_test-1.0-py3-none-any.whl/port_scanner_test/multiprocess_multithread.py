import socket,time
from multiprocessing import Pool
from threading import Thread
import logging
from queue import Queue

logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter=logging.Formatter('%(asctime)s:%(message)s')
filehnadler=logging.FileHandler('port.log')
filehnadler.setFormatter(formatter)
logger.addHandler(filehnadler)


# import configparser

# config = configparser.ConfigParser()
# config.read('config.ini')


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
    # print(port)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((target,port))
        s.close()
        logger.debug(f"Target : {target} , Port : {port} is open")
        open_ports.append(port)
        return port
    except :
        # print(e)
        pass



ports1=[]

def func(target):
    
    global ports1
    ports=ports1
    # print(ports)
    open_ports=[]
    start = time.time()
    try:
        pool = ThreadPool(100)
        pool.map(pscan, ports,target,open_ports)
        pool.wait_completion()
    except Exception as e:
        print(e)
    logger.debug({"Target=":target,"Open_Ports":open_ports,"Time Taken":time.time()-start})
    return {"Target=":target,"Open_Ports":open_ports,"Time Taken":time.time()-start}
# print(func("192.168.1.127","0-65000"))





def func1(raw_target,port_range):
    target_ip=str(raw_target).split(",")
    logger.debug(f"Targets : {target_ip} , Port Range : {port_range} \n")
    global ports1
    ports1=[i for i in range(int(str(port_range).split("-")[0]),int(str(port_range).split("-")[1]))]
    # print(ports1)
    # print(type(ports1))
    # target=['192.168.1.127','192.168.1.99','192.99.7.28']
    start=time.time()
    import multiprocessing 
    pool1=multiprocessing.Pool()
    result=pool1.map(func,target_ip)
    logger.debug(("Total time=",time.time()-start))
    logger.debug(f'Result : {result} \n')
    return result

# func1('192.99.7.28','0-5000')


# 192.168.1.127,192.168.1.99,/\