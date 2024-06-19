import time
import numpy as np

class Familiarization():

    def __init__(self):
        """Dummy Familiarization class
        """
        self.level = 10

    def familiarize(self):
        """Dummy Familiarization function

        Returns:
            int: startlevel for the main procedure
        """
        print("Dummy Familiarization started")
        time.sleep(2)
        print("Dummy Familiarization done")
        return self.level

class StandardProcedure():
    
    def __init__(self):
        """Dummy StandardProcedure class
        """
        # Dummy Results
        # 125, 250, 500, 1000, 2000, 4000, 8000 #Hz
        left = np.array([5, 10, 5, 10, 20, 25, 40]) #dBHL
        right = np.array([10, 10, 10, 15, 20, 25, 50])
        self.results = {"right": right, 
                      "left": left}

    def standard_test(self):
        """Dummy StandardProcedure function

        Returns:
            dict: dummy results of the test"""
        print("Dummy Hearing Test started")
        time.sleep(2)
        print("Dummy Hearing Test done")
        return self.results
    

class TestProcedure():
    
    def __init__(self):
        """Dummy StandardProcedure class
        """
        # Dummy Results
        # 125, 250, 500, 1000, 2000, 4000, 8000 #Hz
        left = np.array([5, 10, 5, 10, 20, 25, 40]) #dBHL
        right = np.array([10, 10, 10, 15, 20, 25, 50])
        self.results = {"right": right, 
                    "left": left}

    def test_test(self):
        """Dummy StandardProcedure function

        Returns:
            dict: dummy results of the test"""
        print("Test Hearing Test started")
        time.sleep(2)
        print("Test Hearing Test done")
        return self.results
    

