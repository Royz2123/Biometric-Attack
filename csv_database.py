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
        create_database=False
    ):
        # set filenames
        self._csv_filename = csv_filename
        self._face_dir = face_dir

        # create a face transform object
        self._analyzer = face_transform.FaceTransformation()

        # create csv parser and data
        self._parser = face_csv_parser.FaceCSVParser(csv_filename)
        self._data = []

        if create_database:
            self.create_database()
        else:
            self._data = self._parser.read_csv()

        # number of faces in database
        self._data_len = len(self._data)

        # set the transform PCA and such
        self._analyzer.set_transform(self.get_face_mat())
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
            self._data[i].features = proj_faces[i]

    def create_database(self):
        # create all of the faces
        for i, face_filename in enumerate(os.listdir(self._face_dir)):
            # print progress
            print("%s:\t\t%d/%d" % (face_filename, i + 1, len(os.listdir(self._face_dir))))

            # find readable image
            found, im_path = self.find_face_filename(face_filename)
            if not found:
                print("NOT FOUND")
                continue

            # create face and add to database
            curr_face = face.Face(self._face_dir + im_path)
            if curr_face.set_features(self._analyzer) != -1:
                self._data.append(curr_face)

            # write into the csv file
            self._parser.del_csv()
            self._parser.write_csv(self._data)


    def find_face_filename(self, curr_dir):
        for filename in os.listdir(self._face_dir + curr_dir):
            if filename == "img_scl":
                new_dir = curr_dir + "/img_scl/" + curr_dir
                return self.find_face_filename(new_dir)

            elif util.readable_image(filename):
                return True, curr_dir + "/" + filename
        return False, ""

    def check_for_match(self, generated_face):
        return [face for face in self._data if face == generated_face]

    def check_for_matches(self, faces):
        return [len(self.check_for_match(face)) for face in faces]

    def generate_faces(self, batch_size=constants.DEFAULT_ATTACK_SIZE):
        return self._analyzer.generate_faces(batch_size)
