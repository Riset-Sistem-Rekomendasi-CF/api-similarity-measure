import cmath

from measure.v2.mean import Mean
from measure.v2.prediction import Prediction
from measure.v2 import Similarity
from measure.v2.MatrixRating import MatrixRating

from typing_extensions import override
from operator import mul,itemgetter


class CosineSimilarity (Similarity) :

    def __init__(self, data, *, toyData : bool|None = True, opsional="user-based",k=2) :
        # Mean.__init__(self,data,opsional=opsional,toyData=toyData)

        # self.result_similarity = self.main_calculation()

        # Prediction.__init__(self,data,self.result_similarity,opsional=opsional,k=k,toyData=toyData)
        super().__init__(data,toyData=toyData,opsional=opsional,k=k)

    @override
    def numerator(self,u:int,v:int, commonlyRated : list[int], matrix : list|None = None) -> float:
        if len(commonlyRated) == 0 :
            return 0
        if not self.toyData :
            return sum(map(mul, list(itemgetter(*commonlyRated)(matrix[u])) , list(itemgetter(*commonlyRated)(matrix[v])) )) if len(commonlyRated) > 1 else matrix[u][commonlyRated[0]] * matrix[v][commonlyRated[0]]
        return sum(map(mul, list(itemgetter(*commonlyRated)(self.__data[u])) , list(itemgetter(*commonlyRated)(self.__data[v])) )) if len(commonlyRated) > 1 else self.__data[u][commonlyRated[0]] * self.__data[v][commonlyRated[0]]

    @override
    def denominator(self,u : int,v : int, set1 : list[int] ,set2 : list[int], matrix : list|None = None) -> float:
        if len(set1) == 0 or len(set2) == 0 :
            return 0
        if not self.toyData :
            return cmath.sqrt( sum(list(map(lambda x : x**2, itemgetter(*set1)(matrix[u]) ))) if len(set1) > 1 else matrix[u][set1[0]]**2 ) * cmath.sqrt(sum(list(map(lambda x : x**2,itemgetter(*set2)(matrix[v])) )) if len(set2) > 1 else matrix[v][set2[0]]**2)
        return cmath.sqrt( sum(list(map(lambda x : x**2, itemgetter(*set1)(self.__data[u]) ))) if len(set1) > 1 else self.__data[u][set1[0]]**2 ) * cmath.sqrt(sum(list(map(lambda x : x**2,itemgetter(*set2)(self.__data[v])) )) if len(set2) > 1 else self.__data[v][set2[0]]**2)

    @override
    def similarity_calculation(self, u : int, v : int):

        set1, set2 = self.getItem(u) if self.opsional == "user-based" else self.getUser(u) , self.getItem(v) if self.opsional == "user-based" else self.getUser(v)
        commonlyRated = list( set(set1) & set(set2) )
        numerator , denominator = self.numerator(u,v, commonlyRated).real, self.denominator(u,v, set1, set2).real
        return (numerator / denominator) if denominator != 0 and numerator != 0 else 0

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
    
    def similarity_result(self) :
        return self.result_similarity
        
    def show_similarity(self) :
        return self.result_similarity
