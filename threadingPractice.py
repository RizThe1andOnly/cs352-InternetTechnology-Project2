import threading
import time
import os


class StrStore:
    def __init__(self,strToBeModded):
        self.val = strToBeModded
    
    def modVal(self,inp):
        self.val = inp
    
    def getVal(self):
        return self.val



def threadFunc(inp,req,sharedVar,lock,stopper):
    r"""
        Will change the value of the sharedVar based on inp.

        -----------
        @param:
            - inp :
                - if 0 then sharedVar will be set to 0
                - if 1 then shardVar will be set to 1
            - req :
                the variable that defines which value the particular thread is looking for
                ; that thread will only do variable change if it receives the variable it is
                looking for.
    """
    
    print(f"inp:{inp} req:{req}")

    with lock:
        if inp == req:
            sharedVar.modVal(str(inp))
    
    print(f"sharedVar: {sharedVar.getVal()} from Thread {req}")
    
    while (True):
        if stopper():
            break
    
    print(f"Thread {req} Interrupted")
    
    exit()



if __name__ == "__main__":

    print(os.getpid())
    
    sharedVar = StrStore(None)
    stopperVar = False

    tl = threading.Lock()

    t1 = threading.Thread(name='thread1',target=threadFunc,args=[1,0,sharedVar,tl,lambda:stopperVar])
    t2 = threading.Thread(name='thread2',target=threadFunc,args=[1,1,sharedVar,tl,lambda:stopperVar])

    t1.start()
    t2.start()

    time.sleep(5)

    #shut down threads:
    stopperVar = True
    print(sharedVar.getVal())
