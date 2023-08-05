import logging
import threading
import time
from collections import deque
import traceback

class LoggerEnv():

    def __init__(self,name,level=logging.INFO,file_name='log/Test-{name}-{day}-{month}-{year}.log',format='%(asctime)s %(threadName)s :%(levelname)s:    %(message)s',datefmt='%d-%m-%y %H:%M:%S'):
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

    def capture_stage_trace(self,function):
        
        def capture(*args, **kwargs):
            
                        
            try:
                function(*args, **kwargs)
                logging.info("...Stage {func}:Sucess!".format(func=function.__name__))
            except Exception as e :
                trace=traceback.format_exc()
                logging.error("...Stage {func}:\n{trace}".format(trace=trace,func=function.__name__))
                Error="\n"+str(e)
                raise Exception(Error)
            
        return capture

    def capture_stage(self,function):
        
        def capture(*args, **kwargs):           
            try:
                function(*args, **kwargs)
                logging.info("...Stage {func}:Sucess!".format(func=function.__name__))
            except Exception as e :
                logging.error("...Stage {func}:   {msg}".format(msg=str(e.args[0]),func=function.__name__))
                Error="\n"+str(e)
                raise Exception(Error)
            
        return capture

    def capture_step_log(self,step):
        
            
        if 'passed' in str(step.status):
            logging.info("...Step Sucess:{key} {step}".format(key=step.keyword,step=step.name))
        else:
            logging.error("...Step {key} {step}:{status}:   {msg},filename:{path}...{line}".format(key=step.keyword,status=step.status,step=step.name,msg=step.exception,path=str(step.filename),line=str(step.line)))