from measure.v2.mean import Mean
from measure.v2.prediction import Prediction

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
