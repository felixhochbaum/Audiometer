import time
import numpy as np

class Familiarization():
    def __init__(self):
        self.level = 10

    def familiarize(self):
        print("Dummy Familiarization started")
        time.sleep(2)
        print("Dummy Familiarization done")
        return self.level

class StandardProcedure():
    def __init__(self):
        # 125, 250, 500, 1000, 2000, 4000, 8000 #Hz
        left = np.array([5, 10, 5, 10, 20, 25, 40]) #dBHL
        right = np.array([10, 10, 10, 15, 20, 25, 50])
        self.level = {"right": right, 
                      "left": left}

    def standard_test(self):
        print("Dummy HearingTest started")
        time.sleep(2)
        print("Dummy HearingTest done")
        return self.level
    

