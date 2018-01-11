import os
import matplotlib as plt
import numpy as np

import face_transform
import face
import constants
import util

DIR_1 = constants.DEFAULT_TESTING_FACE_DIR_1
DIR_2 = constants.DEFAULT_TESTING_FACE_DIR_2
DIR_3 = constants.DEFAULT_TESTING_FACE_DIR_3

def get_faces(dirname):
    f_t = face_transform.FaceTransformation()
    face_list = []
    for face_filename in os.listdir(dirname):
        # find readable image
        impath = dirname + "/" + face_filename
        print(impath)
        if not util.readable_image(impath):
            continue

        # create face and add to database
        curr_face = face.Face(impath)
        if curr_face.set_features(f_t) != -1:
            face_list.append(curr_face)

    return face_list


def main():
    faces = [get_faces(DIR_1), get_faces(DIR_2), get_faces(DIR_3)]

    points = []
    for class_index, curr_class in enumerate(faces):
        curr_test = []
        for test_group in faces:
            curr_samples = []
            for face in test_group:
                curr_samples.append(curr_class[0].distance(face))
            curr_test.append(curr_samples)
        points.append(curr_test)

    util.plot_classes(points)





if __name__ == "__main__":
    main()
