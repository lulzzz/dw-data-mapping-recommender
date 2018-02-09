import pandas as pd


class SamplePairsParser(object):
    def parse(self, path):
        dataframe = pd.read_excel(path)
        return dataframe
