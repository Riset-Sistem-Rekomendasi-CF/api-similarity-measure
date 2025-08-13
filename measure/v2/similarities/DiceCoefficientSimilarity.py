from measure.v2.mean import Mean
from measure.v2.prediction import Prediction
from measure.v2 import Similarity
from measure.v2.MatrixRating import MatrixRating

from typing_extensions import override

class DiceCoefficientSimilarity(Similarity, Prediction, Mean, MatrixRating) :

    def __init__(self, data, * ,toyData : bool|None = True, opsional="user-based",k=2):
        Mean.__init__(self,data,opsional=opsional,toyData=toyData)

        self.result_similarity = self.main_calculation()
        Prediction.__init__(self,data,self.result_similarity,opsional=opsional,k=k,toyData=toyData)

    @override
    def numerator(self, A:list, B:list) -> list[float]:
        return 2 * len( set(A) & set(B) )

    @override
    def denominator(self, A:list, B:list) -> list[float]:
        return len( A ) + len( B )

    @override
    def similarity_calculation(self,A, B) -> float :
        setA = set(self.getItem(A) if self.opsional == "user-based" else self.getUser(A))
        setB = set(self.getItem(B) if self.opsional == "user-based" else self.getUser(B))

        denom = self.denominator(setA,setB).real

        return (self.numerator(setA,setB).real / denom) if denom != 0 else 0

    @override
    def main_calculation(self):
        matrix = self.matrixRating if self.opsional == "user-based" else self.reverseMatrixRating
        result = [[] for _ in range(len(matrix))]

        for i in range(len(matrix)) :
            for j in range(i,len(matrix)):
                if i == j :
                    result[i].append(1)
                    continue
                similarity_result = self.similarity_calculation(int(i), int(j))
                result[i].append(similarity_result)
                result[j].append(similarity_result)
        return result

    def show_similarity(self) :
        return self.result_similarity