
import CSVParser
import face

class FaceCSVParser(CSVParser):
    def __init__(self, filename):
        super(FaceCSVParser, self).__init__(self, filename)
        
    def read_csv(self):
        arr = super(FaceCSVParser, self).read_csv(self)
        return [face.Face(filename=face[0], features=face[1:]) for face in arr]
        
    def write_csv(self, arr):
        csv_format = [np.array([face.filename] + face.features) for face in arr]
        super(FaceCSVParser, self).write_csv(self, csv_format)