import numpy as np

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
        
    def project_faces(self, face_mat):
        return np.mat(face_mat) * np.mat(self._eig_vectors)
        
    def sample_face(self):
        pass
        
    @staticmethod
    def find_features(face_im):
        # dlib features, call function
        pass
