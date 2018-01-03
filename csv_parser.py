import numpy as np

class CSVParser(object):
    def __init__(self, filename):
        self._filename = filename
        
    def read_file():
        ret = ""
        with open(self._filename, "r") as f:
            buf = f.read()
            if buf is None:
                break
            ret += buf
        return ret
        
    def write_file(content):
        with open(self._filename, "w") as f:
            f.write(content)
    
    def read_csv(self):
        file_content = self.read_file()
        rows = []
        for row in file_content.split('\n'):
            rows.append(row.split(','))
        return np.array(rows)
     
    def write_csv(self, arr):
        for row in arr:
            self.write_file(','.join(list(row)) + '\n')
            