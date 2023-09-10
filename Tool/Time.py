import time

class Timer_Class():
    def __init__(self):
        self.Start = time.time()
        self.End = None
    
    def Stop(self):
        self.End = time.time()
        return self.Get_Time()

    def Get_Time(self, String = True):
        if self.End is None:
            self.Stop()
        if String:
            return str(round(self.End - self.Start, 2)) + " seconds"
        else:
            round(self.End - self.Start, 2)