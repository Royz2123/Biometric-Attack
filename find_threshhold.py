import os
import matplotlib as plt
import math
import numpy as np

import face_transform
import face
import constants
import util
import csv_database


DIR_1 = constants.DEFAULT_TESTING_FACE_DIR_1
DIR_2 = constants.DEFAULT_TESTING_FACE_DIR_2
DIR_3 = constants.DEFAULT_TESTING_FACE_DIR_3
DATA_DIR = "faces/all_faces/all_labeld_faces_corrected/"

def get_face_dir(dirname):
    face_filenames = os.listdir(dirname)

    # messy database, handle bad driectories recursively
    if "img_scl" in face_filenames:
        impath = dirname + "/img_scl/"
        return get_face_dir(impath + os.listdir(impath)[0] + "/")

    else:
        # add full path to names
        # also check that it is a readable file
        fixed_names = []
        for face_filename in os.listdir(dirname):
            if util.readable_image(dirname + "/" + face_filename):
                fixed_names.append((dirname + "/" + face_filename))
            if len(fixed_names) >= 2:
                break
        return fixed_names


def get_faces(dirname):
    f_t = face_transform.FaceTransformation()
    face_list = []

    print(get_face_dir(dirname))

    for impath in get_face_dir(dirname):
        # create face and add to database
        curr_face = face.Face(impath)
        if curr_face.set_features(f_t) != -1:
            face_list.append(curr_face)

        # check if we already have enough faces
        if len(face_list) == 2:
            break

    return face_list


# simple main for comparing a few faces
def main1():
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


# main that plots the real face diffrences
def main2():
    # frequency counts between self and itself
    self_freq = {}
    other_freq = {}

    # face data
    face_database = csv_database.CSVDatabase()

    for face in face_database._data:
        pass

"""
def add_element(d, key):
    if key not in d.keys():
        d[key] = 0
    d[key] += 1
    return d

def round_dist(dist):
    return math.ceil(dist * 10) / 10
"""

def main():
    # frequency counts between self and itself
    self_freq = []
    other_freq = []

    # first get all the faes
    faces = []
    for index, curr_dir in enumerate(os.listdir(DATA_DIR)):
        faces.append(get_faces(DATA_DIR + curr_dir))
        print("%d/%d" % (index, len(os.listdir(DATA_DIR))))

    for subject_index in range(len(faces) - 1):
        try:
            first, second = faces[subject_index], faces[subject_index + 1]

            # find distances
            self_dist = first[0].distance(first[1])
            other_dist = first[0].distance(second[0])

            # add to frequencies
            #self_freq = add_element(self_freq, self_dist)
            #other_freq = add_element(other_freq, other_dist)
            self_freq.append(self_dist)
            other_freq.append(other_dist)
        except:
            pass

    util.plot_freqs(self_freq, other_freq)







if __name__ == "__main__":
    main()
