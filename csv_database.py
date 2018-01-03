import os

import constants
import face
import face_csv_parser
import face_transform

class CSVDatabase(object):
    DISPLAY_ITEMS = 10

    def __init__(
        self, 
        face_dir=constants.DEFAULT_FACE_DIR,
        csv_filename=constants.DEFAULT_FACES_CSV_NAME, 
    ):
        # set filenames
        self._csv_filename = csv_filename
        self._face_dir = face_dir
    
        # create csv parser
        self._parser = face_csv_parser.FaceCSVParser(csv_filename)
        self.create_database()
                
        # create a face transform object
        self._analyzer = face_transform.FaceTransform(self.get_face_mat())
        self.project_faces()
    
    def __getitem__(self, key):
        return self._data[key]
        
    def __setitem__(self, key, val):
        self._data[key] = val
        self._parser.write_csv(self._data) 
        
    def append_item(self, val):
        self._data.append(val)
        self._parser.write_csv(self._data) 
        
    def __repr__(self):
        return '\n'.join(list(self._data[:CSVDatabase.DISPLAY_ITEMS]))
      
    def get_face_mat(self):
        return np.mat([face.features for face in self._data])

    def project_faces(self):        
        # project all data onto new basis
        proj_faces = self._analyzer.project_faces(self.get_face_mat())

        # update all the faces matrix
        for i in range(self._data_len):
            faces[i].features = proj_faces[i]
        
    def create_database(self):
        # create all of the faces
        for face_filename in os.listdir(self._face_dir):
            self._data.append(face.Face(face_filename))

        # number of faces in database
        self._data_len = len(self._data)
        
        # write into the csv file
        self._parser.write_csv(self._data)
        
    def check_for_matches(self, generated_face):
        matches = []
        for face in self._data:
            # check for match
            if face == generated_face:
                matches.append(face)
        return matches
        
    def generate_face(self):
        # generated a face using inverse sample
        return face.Face(features=self._analyzer.sample_face())
   
   