import numpy as np
import scipy.interpolate as interpolate

class FaceTransformation(object):
    def __init__(self, face_mat):    
        # calculate the mean and subtract from matrix
        self._mean = np.matrix.mean(face_mat)
        face_mat -= self._mean
        
        # calculate covariance matrix
        self._cov = np.cov(face_mat)
        
        # calculate and sort eigenvalues and eigenvectors
        eigen = zip(*np.lianlg.eig(face_mat))
        self._eig_vectors, self._eig_values = zip(*sorted(eigen, lambda x: x[1]))
        
        # caluclate this face_mat by projecting
        self._face_mat = self.project_faces(face_mat)
        
    def project_faces(self, face_mat):
        return np.mat(face_mat) * np.mat(self._eig_vectors)
        
    def sample_faces(self, batch_size=constants.DEFAULT_ATTACK_SIZE):
        return inverse_transform_sampling
        
    def inverse_transform_sampling(data, n_bins=40, n_samples=1000):
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
        




