import numpy as np
import os

import constants
import face
import face_csv_parser
import face_transform
import util

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

        # create csv parser and data
        self._parser = face_csv_parser.FaceCSVParser(csv_filename)
        self._data = []
        self.create_database()

        # create a face transform object
        self._analyzer = face_transform.FaceTransformation(self.get_face_mat())
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
            new_path = self._face_dir + face_filename
            self._data.append(
                face.Face(new_path + "/" + os.listdir(new_path)[0])
            )

        # number of faces in database
        self._data_len = len(self._data)

        # write into the csv file
        self._parser.write_csv(self._data)

    def check_for_match(self, generated_face):
        return [face for face in self._data if face == generated_face]

    def check_for_matches(self, faces):
        return [len(self.check_for_match(face)) for face in faces]

    def generate_faces(self, batch_size=constants.DEFAULT_ATTACK_SIZE):
        return self._analyzer.generate_faces(batch_size)