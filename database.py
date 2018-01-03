import csv_parser

class CSVDatabase(object):
    def __init__(self, filename):
        self._parser = csv_parser.CSVParser(filename)
        self._data = self._parser.read_csv()
    
    def __getitem__(self, key):
        return self._data[key]
        
    def __setitem__(self, key, val):
        self._data[key] = val
