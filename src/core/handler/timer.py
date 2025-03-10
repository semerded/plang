import time

class Timer:
    def __init__(self, delay):
        self.delay = delay
        
        self.previous_time = time.perf_counter()
        
    def is_ringing(self):
        return time.perf_counter() - self.previous_time >= self.delay
    
    def reset(self):
        self.previous_time = time.perf_counter()
        
    def stop(self):
        pass
    