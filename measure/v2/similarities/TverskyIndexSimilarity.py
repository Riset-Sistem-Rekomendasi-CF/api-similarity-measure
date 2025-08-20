from measure.v2 import Similarity

from typing_extensions import override
from sklearn.manifold import MDS

import numpy as np

class TverskyIndexSimilarity(Similarity) :
    
    def __init__(self, data, *, toyData : bool|None = True, opsional="user-based",k=2,alpha_1=0.7,alpha_2=0.2) -> None :
        
        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2

        super().__init__(data,toyData=toyData,opsional=opsional,k=k)

    def __checkSymmetric(self) -> bool :
        return self.alpha_1 == self.alpha_2
    
    @override
    def numerator(self, A:list, B:list) -> float:
        return len( set(A) & set(B) )

    @override
    def denominator(self, A:list, B:list) -> float:
        return len( set(A) & set(B) ) + (self.alpha_1 * len( set(A) - set(B) )) + self.alpha_2 * len( set(B) - set(A) )
    
    @override
    def similarity_calculation(self,A, B) -> float :
        setA = set(self.getItem(A) if self.opsional == "user-based" else self.getUser(A))
        setB = set(self.getItem(B) if self.opsional == "user-based" else self.getUser(B))

        denom = self.denominator(setA,setB).real
        
        return (self.numerator(setA,setB).real / denom) if denom != 0 else 0

    @override
    def main_calculation(self) -> list[list[float]]:
        matrix = self.matrixRating if self.opsional == "user-based" else self.reverseMatrixRating
        result = [[] for _ in range(len(matrix))]
        
        if self.__checkSymmetric() :
            for i in range(len(matrix)):
                for j in range(i,len(matrix)):
                    if i == j:
                        result[i].append(1)
                        continue
                    similarity_result = self.similarity_calculation(int(i), int(j))
                    result[i].append(similarity_result)
                    result[j].append(similarity_result)
            return result
        
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if i == j:
                    result[i].append(1)
                    continue
                similarity_result = self.similarity_calculation(int(i), int(j))
                result[i].append(similarity_result)
        return result