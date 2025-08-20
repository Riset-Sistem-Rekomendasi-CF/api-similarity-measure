import cmath

from measure.v2.mean import Mean
from measure.v2.prediction import Prediction
from measure.v2 import Similarity
from measure.v2.MatrixRating import MatrixRating

from numpy import transpose
from typing_extensions import override
from operator import mul,itemgetter


class AdjustedCosineSimilarity(Similarity) :

    def __init__(self, data, *, toyData : bool|None = True, opsional="user-based",k=2) :
        super().__init__(data,toyData=toyData,opsional=opsional,k=k)

    @override
    def numerator(self,u:int,v:int, commonlyRated : list[int], mean_centered : list[list[float]]) -> float:
        if len(commonlyRated) == 0 :
            return 0
        
        return sum(map(mul, list(itemgetter(*commonlyRated)(mean_centered[u])) , list(itemgetter(*commonlyRated)(mean_centered[v])) )) if len(commonlyRated) > 1 else (mean_centered[u])[commonlyRated[0]] * (mean_centered[v])[commonlyRated[0]]

    @override
    def denominator(self,u : int,v : int,commonlyRated : list[int], mean_centered : list[list[float]]) -> float:
        if len(commonlyRated) == 0 :
            return 0
        return cmath.sqrt( sum(list(map(lambda x : x**2, itemgetter(*commonlyRated)(mean_centered[u]) ))) if len(commonlyRated) > 1 else mean_centered[u][commonlyRated[0]]**2 ) * cmath.sqrt(sum(list(map(lambda x : x**2,itemgetter(*commonlyRated)(mean_centered[v])) )) if len(commonlyRated) > 1 else mean_centered[v][commonlyRated[0]]**2)

    @override
    def similarity_calculation(self, u : int, v : int, mean_centered : list[list[float]]):

        set1, set2 = self.getItem(u) if self.opsional == "user-based" else self.getUser(u) , self.getItem(v) if self.opsional == "user-based" else self.getUser(v)
        commonlyRated = list( set(set1) & set(set2) )
        numerator , denominator = self.numerator(u,v, commonlyRated,mean_centered).real, self.denominator(u,v, commonlyRated,mean_centered).real
        return (numerator / denominator) if denominator != 0 and numerator != 0 else 0

    @override
    def main_calculation(self):
        matrix = self.matrixRating if self.opsional == "user-based" else self.reverseMatrixRating
        mean_centered = transpose(self.result_overall_mean_and_mean_centered["mean-centered"]["user-based"]) if self.opsional == "item-based" else self.result_overall_mean_and_mean_centered["mean-centered"]["item-based"]
        
        result = [[] for _ in range(len(matrix))]
        
        for i in range(len(matrix)):
            for j in range(i, len(matrix)):
                if i == j:
                    result[i].append(1)
                    continue
                similarity_result = self.similarity_calculation(int(i), int(j),mean_centered)
                result[i].append(similarity_result)
                result[j].append(similarity_result)
        return result
    
    def similarity_result(self) :
        return self.result_similarity
        
    def show_similarity(self) :
        return self.result_similarity
