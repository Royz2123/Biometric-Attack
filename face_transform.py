import dlib
import numpy as np
import scipy.interpolate as interpolate

import constants

class FaceTransformation(object):
    HISTOGRAM_BINS = 40

    def __init__(self):
        # set dlib analyzers
        self._detector = dlib.get_frontal_face_detector()
        self._sp = dlib.shape_predictor(constants.SHAPE_PREDICTOR_PATH)
        self._facerec = dlib.face_recognition_model_v1(constants.FACE_REC_MODEL_PATH)

    def set_transform(self, face_mat):
        # se face mat size
        face_mat_size = (np.size(face_mat, 0), np.size(face_mat, 1))

        # calculate the mean and subtract from matrix
        self._mean = np.matrix.mean(face_mat)
        np.subtract(face_mat, np.full(face_mat_size, self._mean))

        # calculate covariance matrix
        self._cov = np.cov(face_mat)

        # calculate and sort eigenvalues and eigenvectors
        eigen = zip(*np.linalg.eig(face_mat))
        self._eig_vectors, self._eig_values = zip(*sorted(eigen, lambda x: x[1]))

        # calculate this face_mat by projecting
        self._face_mat = self.project_faces(face_mat)

        # now for each feature find inv function
        self._features = [self.create_inv(f_d) for f_d in self._face_mat.transpose()]


    def project_faces(self, face_mat):
        return np.mat(face_mat) * np.mat(self._eig_vectors)

    def generate_faces(self, batch_size=constants.DEFAULT_ATTACK_SIZE):
        features = [gen_feature(f_index, batch_size) for f_index in range(len(self._features))]
        return [face.Face(features=arr) for arr in np.array(features).transpose()]

    def gen_feature(self, f_index, batch_size):
        return self._features[f_index](np.random.rand(batch_size))

    def create_inv(data, n_bins=40):
        hist, bin_edges = np.histogram(data, bins=n_bins, density=True)
        cum_values = np.zeros(bin_edges.shape)
        cum_values[1:] = np.cumsum(hist*np.diff(bin_edges))
        inv_cdf = interpolate.interp1d(cum_values, bin_edges)
        r = np.random.rand(n_samples)
        return inv_cdf(r)


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
