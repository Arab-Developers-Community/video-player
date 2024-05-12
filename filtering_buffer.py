# class that will create x number of buffers and will have gettter and setter for each buffer with locks so a single buffer can be accessed by a single thread at a time\

from filtering_manager import filtering_manager
import threading
import time

class filtering_buffer:

    def __init__(self, buffers_num, fm: filtering_manager):
        self.buffers = [None] * buffers_num
        self.locks = [threading.Lock() for i in range(buffers_num)]
        self.fm = fm

    def get_buffer(self, index):
        self.locks[index].acquire()
        buffer = self.buffers[index]
        self.locks[index].release()
        return buffer

    def set_buffer(self, index, buffer):
        self.locks[index].acquire()
        self.buffers[index] = buffer
        self.locks[index].release()
    
    def startSyncThread(self):
        thread = threading.Thread(target=self.sync)
        thread.start()

    def sync(self):
        while True:
            for i in range(len(self.buffers)):
                    self.set_buffer(i, self.fm.read_state())
            time.sleep(10)   
    

    