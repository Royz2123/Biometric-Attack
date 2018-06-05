import dlib
import matplotlib.pyplot as plt
import numpy as np
import numpy.matlib
import scipy.interpolate as interpolate
import time

import constants
import face
import util

class FaceTransformation(object):
    HISTOGRAM_BINS = 40

    def __init__(self):
        # set dlib analyzers
        self._detector = dlib.get_frontal_face_detector()
        self._sp = dlib.shape_predictor(constants.SHAPE_PREDICTOR_PATH)
        self._facerec = dlib.face_recognition_model_v1(constants.FACE_REC_MODEL_PATH)

    def set_transform(self, face_mat):
        # face_mat = face_mat.transpose()

        """
        #Plots the first feature:
        data = face_mat.transpose()[0]
        print(data.shape)
        hist, bin_edges = np.histogram(data, bins=FaceTransformation.HISTOGRAM_BINS, density=True)
        self.plot_hist(hist, bin_edges)
        """

        # se face mat size
        face_mat_size = (np.size(face_mat, 0), np.size(face_mat, 1))
        self._dimension = face_mat_size[1]

        # calculate the mean and subtract from matrix
        self._mean = np.matrix.mean(face_mat, 0)
        repped = numpy.matlib.repmat(self._mean, np.size(face_mat, 0), 1)
        face_mat = np.subtract(face_mat, repped)

        # calculate covariance matrix
        self._cov = np.cov(face_mat.transpose())

        # calculate and sort eigenvalues and eigenvectors
        eig_values, eig_vectors = np.linalg.eig(self._cov)
        eig_pairs = [
            (np.abs(eig_values[i]), eig_vectors[:,i])
            for i in range(len(eig_values))
        ]
        eig_pairs.sort(key=lambda x: x[0], reverse=True)     # sort based on values (second in pair)

        # find projectionn matrix (no need for dimensionality decrease for now)
        self._matrix_w = np.hstack(
            tuple([
                eig_pairs[i][1].reshape(self._dimension, 1)
                for i in range(self._dimension)
            ])
        )
        self._inv_matrix_w = np.linalg.inv(self._matrix_w)

        # calculate this face_mat by projecting
        self._face_mat = self.project_faces(face_mat)

        # now for each feature find inv function
        self._features = [self.create_inv(f_d) for f_d in self._face_mat.transpose()]

        """
        Small code sample for checking the sampling quality

        data = self._face_mat.transpose()[0]
        hist, bin_edges = np.histogram(data, bins=FaceTransformation.HISTOGRAM_BINS, density=True)
        self.plot_hist(hist, bin_edges)

        data = self.gen_feature(0, 10000)
        hist, bin_edges = np.histogram(data, bins=FaceTransformation.HISTOGRAM_BINS, density=True)
        self.plot_hist(hist, bin_edges)


        # Plots the generated_faces:

        data = self.generate_faces(10000)
        data = [face.features[0] for face in data]
        hist, bin_edges = np.histogram(data, bins=FaceTransformation.HISTOGRAM_BINS, density=True)
        self.plot_hist(hist, bin_edges)
        plt.show()
        """


    def unproject_faces(self, data):
        # First mulriply by inverse of projection matrix
        data = np.mat(data) * np.mat(self._inv_matrix_w)

        # Then add the original mean
        repped = numpy.matlib.repmat(self._mean, np.size(data, 0), 1)
        data = np.add(data, repped)
        return data


    def project_faces(self, face_mat):
        return np.mat(face_mat) * np.mat(self._matrix_w)

    def generate_faces(self, batch_size=constants.DEFAULT_ATTACK_SIZE * 100):
        features = [self.gen_feature(f_index, batch_size) for f_index in range(len(self._features))]
        features = self.unproject_faces(np.array(features).transpose())
        faces = [face.Face(features=arr) for arr in np.array(features)]
        return faces

    def gen_feature(self, f_index, batch_size):
        return self._features[f_index](np.random.rand(batch_size))

    def create_inv(self, data, n_bins=HISTOGRAM_BINS, debug=False):
        hist, bin_edges = np.histogram(data, bins=n_bins, density=True)
        if debug:
            util.plot_hist(hist, bin_edges)
        cum_values = np.zeros(bin_edges.shape)
        cum_values[1:] = np.cumsum(hist*np.diff(bin_edges))
        cdf = interpolate.interp1d(cum_values, bin_edges)
        return cdf

    def plot_hist(self, hist, bin_edges):
        width = 0.7 * (bin_edges[1] - bin_edges[0])
        center = (bin_edges[:-1] + bin_edges[1:]) / 2
        plt.bar(center, hist, align='center', width=width)
        plt.show()


    """
    Compute the 128D vector that describes the face in img identified by
    shape.  In general, if two face descriptor vectors have a Euclidean
    distance between them less than 0.6 then they are from the same
    person, otherwise they are from different people. Here we just print
    the vector to the screen.

    It should also be noted that you can also call this function like this:
    face_descriptor = facerec.compute_face_descriptor(img, shape, 100)
    The version of the call without the 100 gets 99.13% accuracy on LFW
    while the version with 100 gets 99.38%.  However, the 100 makes the
    call 100x slower to execute, so choose whatever version you like.  To
    explain a little, the 3rd argument tells the code how many times to
    jitter/resample the image.  When you set it to 100 it executes the
    face descriptor extraction 100 times on slightly modified versions of
    the face and returns the average result.  You could also pick a more
    middle value, such as 10, which is only 10x slower but still gets an
    LFW accuracy of 99.3%.
    """
    def find_features(self, img, debug=False):
        # find the bounding boxes of each face (if exists)
        bounding_boxes = self._detector(img, 1)
        if not len(bounding_boxes):
            return None

        # Process the first face
        shape = self._sp(img, bounding_boxes[0])

        # Compute the 128D vector
        face_descriptor = self._facerec.compute_face_descriptor(img, shape)

        # debug the picture
        if debug:
            print(face_descriptor)

        return np.array(face_descriptor)
