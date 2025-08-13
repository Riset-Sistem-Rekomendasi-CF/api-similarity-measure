import cmath

from measure.v2.mean import Mean
from measure.v2.prediction import Prediction
from measure.v2 import Similarity
from measure.v2.MatrixRating import MatrixRating

from typing_extensions import override
from operator import mul,itemgetter
class PearsonSimilarity (Similarity) :

    def __init__(self, data, *, toyData : bool|None = True, opsional="user-based",k=2):
        super().__init__(data,toyData=toyData,opsional=opsional,k=k)


    @override
    def numerator(self,u : int, v : int, setOfRated : list) -> float:
        if len(setOfRated) == 0 :
            return 0
            
        return sum(map(mul, (itemgetter(*setOfRated)(self.result_mean_centered[u])) , (itemgetter(*setOfRated)(self.result_mean_centered[v])) )) if len(setOfRated) > 1 else (self.result_mean_centered[u][setOfRated[0]] * self.result_mean_centered[u][setOfRated[0]])
        
    @override
    def denominator(self, u : int, v : int, setOfRated : list) -> float:
        if len(setOfRated) == 0 :
            return 0
        return cmath.sqrt(sum( list(map(lambda x : x**2,itemgetter(*setOfRated)(self.result_mean_centered[u] ))) ) if len(setOfRated) > 1 else self.result_mean_centered[u][setOfRated[0]]**2) * (cmath.sqrt( sum(list(map(lambda x:x**2,itemgetter(*setOfRated)(self.result_mean_centered[v])))) if len(setOfRated) > 1 else self.result_mean_centered[v][setOfRated[0]]**2))

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
        result = [[] for _ in range(len(self.__data))]
        for i in range(len(self.__data)): 
            if i % 10 == 0 :
                print(f"Sim({i})")
            for j in range(i, len(self.__data)):
                if i == j:
                    result[i].append(1)
                    continue
                similarity_result = self.similarity_calculation(i, j)
                result[i].append(similarity_result)
                result[j].append(similarity_result)
        print("Sim : Selesai")
        return result

    def similarity_result(self) -> list[list[float]]:
        return self.result_similarity

    @override
    def show(self) -> object:
        return pd.DataFrame(self.result_similarity)
    
