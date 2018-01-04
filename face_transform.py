import numpy as np
import scipy.interpolate as interpolate

import constants

class FaceTransformation(object):
    HISTOGRAM_BINS = 40

    def __init__(self, face_mat):    
        # calculate the mean and subtract from matrix
        self._mean = np.matrix.mean(face_mat)
        face_mat -= self._mean
        
        # calculate covariance matrix
        self._cov = np.cov(face_mat)
        
        # calculate and sort eigenvalues and eigenvectors
        eigen = zip(*np.lianlg.eig(face_mat))
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
    
        
    @staticmethod
    def find_features(face_im):
        # dlib features, call function
        pass
        




