import pandas as pd

class DataReader:
    def __init__(self, data_file):
        self.data_file_path = data_file
        self.data = self.read_data()
        pass
    
    # 读取数据，每个场景都需要改
    def read_data(self):
        return pd.read_excel(self.data_file_path, sheet_name=0)

    def read(self, row, col):
        return self.data.iloc[row, col]