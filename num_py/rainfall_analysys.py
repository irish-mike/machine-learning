import numpy as np

class RainfallAnalysis:
    def __init__(self):
        pass

    def run_all(self):
        print('Running rainfall analysis')
        path = 'data/CorkRainfall.txt'
        self.__read_file(path)
        pass

    def __read_file(self, path):
        data = np.genfromtxt(path)
        print(data.shape)
        print(f"Reading rainfall data from {path}")
        pass


    def max_rainfall(self):
        pass

    def unique_years(self):
        pass

