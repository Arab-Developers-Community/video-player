import threading

class filter_state:
    def __init__(self, video):
        self.blockedSections = []
    
    def add_blocked_section(self, start, end):
        self.lock = threading.Lock()
        with self.lock:
            self.blockedSections.append((start, end))

    def is_blocked(self, second):
        if self.lock:
            self.lock.acquire()
            
        for start, end in self.blockedSections:
            if start <= second <= end:
                return True
        return False


    

