import cmath

from measure.v2.mean import Mean
from measure.v2.prediction import Prediction
from measure.v2 import Similarity
from measure.v2.MatrixRating import MatrixRating

import numpy as np
from typing_extensions import override
from operator import mul,itemgetter


class BhattacaryyaCoefficientSimilarity(Similarity) :

    def __init__(self, data, *, toyData : bool|None = True, opsional="user-based",k=2) :
        super().__init__(data,toyData=toyData,opsional=opsional,k=k)

    def probability(self,column : int, target : int) -> float :
        return len( list(filter(lambda x : x == target,self.getItemWithValue(column) if self.opsional == "user-based" else self.getUserWithValue(column))) ) / len(self.getItem(column) if self.opsional == "user-based" else self.getUser(column))

    def probabilities(self,column : int):
        return [self.probability(column, target) for target in range(self.lowest_rating, self.highest_rating+1)]

    @override
    def similarity_calculation(self, u, j):
        column_1 = self.probabilities(u)
        column_2 = self.probabilities(j)
        result = sum(np.sqrt( np.array(list(map(mul,column_1,column_2))) )).real
        return result

    @override
    def main_calculation(self):
        matrix = self.matrixRating if self.opsional == "user-based" else self.reverseMatrixRating
        
        result = [[] for _ in range(len(matrix))]
        
        for i in range(len(matrix)):
            for j in range(i, len(matrix)):
                if i == j:
                    result[i].append(1)
                    continue
                similarity_result = self.similarity_calculation(int(i), int(j))
                result[i].append(similarity_result)
                result[j].append(similarity_result)
        return result
    
    def show_probabilities(self) :
        return [self.probabilities(column) for column in range(len(self.matrixRating if self.opsional == "user-based" else self.reverseMatrixRating))]