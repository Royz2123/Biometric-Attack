import os
import matplotlib as plt
import numpy as np

import face_transform
import face
import constants
import util

USER_DIR = constants.DEFAULT_TESTING_FACE_DIR
OTHER_DIR = constants.DEFAULT_TESTING_FACE_DIR_2


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
    faces2 = get_faces(OTHER_DIR)

    points1 = []
    for face in get_faces(USER_DIR):
        points1.append(faces2[0].distance(face))

    points2 = []
    for face in faces2[1:]:
        points2.append(faces2[0].distance(face))

    util.plot_classes(points1, points2)





if __name__ == "__main__":
    main()
