import cmath

from measure.v2 import Similarity

from typing_extensions import override
from operator import mul,itemgetter

class PearsonSimilarity(Similarity) :

    def __init__(self, data, *, toyData : bool|None = True, opsional="user-based",k=2):

        super().__init__(data,toyData=toyData,opsional=opsional,k=k)
        

    @override
    def numerator(self,u : int, v : int, setOfRated : list) -> float:
        if len(setOfRated) == 0 :
            return 0
            
        return sum(map(mul, (itemgetter(*setOfRated)(self.adapted_mean_centered[u])) , (itemgetter(*setOfRated)(self.adapted_mean_centered[v])) )) if len(setOfRated) > 1 else (self.adapted_mean_centered[u][setOfRated[0]] * self.adapted_mean_centered[u][setOfRated[0]])
        
    @override
    def denominator(self, u : int, v : int, setOfRated : list) -> float:
        if len(setOfRated) == 0 :
            return 0
        return cmath.sqrt(sum( list(map(lambda x : x**2,itemgetter(*setOfRated)(self.adapted_mean_centered[u] ))) ) if len(setOfRated) > 1 else self.adapted_mean_centered[u][setOfRated[0]]**2) * (cmath.sqrt( sum(list(map(lambda x:x**2,itemgetter(*setOfRated)(self.adapted_mean_centered[v])))) if len(setOfRated) > 1 else self.adapted_mean_centered[v][setOfRated[0]]**2))

    @override
    def similarity_calculation(self, u : int, v : int) -> float:
        
        set1 = self.getItem(u) if self.opsional == "user-based" else self.getUser(u)
        set2 = self.getItem(v) if self.opsional == "user-based" else self.getUser(v)
        commonlyRated = list(set(set1) & set(set2))

        denominator = self.denominator(u,v,commonlyRated).real

        numerator = self.numerator(u,v,commonlyRated).real

        return (numerator / denominator) if denominator != 0 and numerator != 0 else 0

    @override
    def main_calculation(self) -> list[list[float]]:
        matrix = self.matrixRating if self.opsional == "user-based" else self.reverseMatrixRating
        result = [[] for _ in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(i, len(matrix)):
                if i == j:
                    result[i].append(1)
                    continue
                similarity_result = self.similarity_calculation(i, j)
                result[i].append(similarity_result)
                result[j].append(similarity_result)
        return result
