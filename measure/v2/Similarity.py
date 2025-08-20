from measure.v2.mean import Mean
from measure.v2.prediction import Prediction
import numpy as np
from sklearn.manifold import MDS


from abc import abstractmethod

class Similarity(Prediction) :
    '''
    Property of Distance based when calculation similarity

    Methods:
    --------
        numerator(vector1,vector2)
            Measurement the value of numerator by threating matrix as a vector
        
        denominator(vector1,vector2)
            Measurement the value of denominator by threating matrix as a vector

        similarity_calculation(u, v, matrix)
            Provide the result similarity of the user-item matrix rating as a vector

        main_calculation(u, v, matrix)
            Provide measurement similarity of the user-item matrix rating as a matrix
    '''
    
    def __init__(self, data, *, toyData : bool|None = True, opsional="user-based",k=2) :
        
        Mean.__init__(self,data,opsional=opsional,toyData=toyData)
        self.adapted_mean_centered = self.result_mean_centered if opsional == "user-based" else np.transpose(self.result_mean_centered)
        
        self.result_similarity = self.main_calculation()
        
        Prediction.__init__(self,data,self.result_similarity,opsional=opsional,k=k,toyData=toyData)

    # @property
    @abstractmethod
    def numerator(self, A:list, B:list) -> int: ...

    # @property
    @abstractmethod
    def denominator(self, A:list, B:list) -> int: ...

    # @property
    @abstractmethod
    def similarity_calculation(self,A:list,B:list) -> float: ...

    @property
    @abstractmethod
    def main_calculation(self) -> list[list[float]]: ...

    def show_similarity(self) -> object:
        return self.result_similarity
    
    def get_reduced_data(self) :
        data = 1-np.real(self.result_similarity)

        # Memastikan matriks simetris
        dissimilarity = (data + data.T) / 2

        # Menerapkan MDS1
        mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42, normalized_stress='auto')
        return mds.fit_transform(dissimilarity).tolist()
