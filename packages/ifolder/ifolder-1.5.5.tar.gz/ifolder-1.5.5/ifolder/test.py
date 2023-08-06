import os, sys
import time

class _Transfer_progress():
    def __init__(self):
        self.pgr = {
            'file_name':'',
            'total_size':0,
            'transferred_size':0,
            'ETA':0,
        }
        self.last_time = 0

    def start_new_file(self, file_name, total_size):
        self.pgr = {
        'file_name':file_name,
        'total_size':total_size,
        'transferred_size':0,
        'speed':0,
        'ETA':0,
        }
        self.last_time = 0

    def set(self,new_transferred_size):
        sample_time = time.time()
        self.pgr['transferred_size'] += new_transferred_size
        speed = (new_transferred_size/(sample_time - self.last_time))
        self.pgr['speed'] = speed
        try:
            self.pgr['ETA'] = (self.pgr['total_size'] - self.pgr['transferred_size'])/speed
        except:
            pass
        self.last_time = sample_time

    def get(self):
        return self.pgr


pro = _Transfer_progress()

def produce():
    pro.start_new_file(file_name='None', total_size=1000000)
    for i in range(100):
        pro.set(10000)
        time.sleep(0.2)

def consu():
    for i in range(100):
        print(pro.get() )
        time.sleep(0.2)
    

from threading import Thread

Thread(target=produce).start()

Thread(target=consu).start()
    

