from multiprocessing import Process, Queue, Pipe, Lock

class JobRunner:

    jobs:list
    q:Queue
    threads:int = 8

    def __init__(self, threads):
        self.jobs = []
        self.threads = threads
        self.lock = Lock()
        self.q = Queue()

    def AddToQueue( self, myProgram, arg:list ):
        arg.insert(0, self.q)
        arg.insert(1, self.lock)
        thread = Process(target=myProgram,args=arg)
        self.jobs.append(thread)

    def RunQueue(self):
        for job in self.jobs:
            job.start()
        for job in self.jobs:
            job.join()

    def GetValue(self):
        if not self.q.empty():
            return self.q.get()
        return None
