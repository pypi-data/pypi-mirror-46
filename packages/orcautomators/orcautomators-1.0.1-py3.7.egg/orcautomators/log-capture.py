import logging
import threading
import time
from collections import deque

class LoggerEnv():

    def __init__(self,name,level=logging.INFO,file_name='log/thread-{thread}-{name}-{day}-{month}-{year}.log',format='%(asctime)s %(threadName)s :%(levelname)s:    %(message)s',datefmt='%d-%m-%y %H:%M:%S'):
        line=time.localtime()
        line=list(line)
        lis=deque()
        for h in line:
            lis.appendleft(int(h))
            if(line.index(h) == 2):
                break
        day=lis[0]
        month=lis[1]
        year=lis[2]
        self.name=name
        self.thread=threading.currentThread().getName()
        filename=file_name.format(thread=self.thread,name=self.name,day=day,month=month,year=year)
        logging.basicConfig(level=level,filename=filename,format=format,datefmt=datefmt)

    def capture_stage(self,function,breaks=True):
        
        def capture(*args, **kwargs):
            try:
                function(*args, **kwargs)
                logging.info("...Stage {func}:Sucess!".format(func=function.__name__))
            except Exception as e :
                logging.error("...Stage {func}:{msg}".format(func=function.__name__,msg=e.args))
                if breaks:
                    Error="\n"+str(e.args)
                    raise Exception(Error)
        return capture