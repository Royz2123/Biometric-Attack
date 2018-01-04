import os

import numpy as np

class CSVParser(object):
    def __init__(self, filename):
        self._filename = filename

    def read_file(self):
        ret = ""
        with open(self._filename, "r") as f:
            while True:
                buf = f.read()
                if len(buf) == 0:
                    break
                ret += buf
        return ret

    def write_file(self, content, mode="a"):
        with open(self._filename, mode) as f:
            f.write(content)

    def read_csv(self):
        file_content = self.read_file()
        rows = []
        for row in file_content.split('\n')[:-1]:
            rows.append(row.split(','))
        return np.array(rows)

    def write_csv(self, arr):
        for row in arr:
            self.write_file(','.join(list(row)) + '\n')

    def del_csv(self):
        os.remove(self._filename)
