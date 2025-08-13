import pandas as pd
from numpy import transpose
from measure.v2.MatrixRating import MatrixRating

class Mean(MatrixRating) :

    def __init__(self, data,*,opsional="user-based", toyData : bool = True) :
        super().__init__(data,toyData=toyData)
        
        self.opsional = opsional
        
        self.result_mean = self.__mean_calculation()
        self.result_mean_centered = self.__mean_centered_calculation()
    
    def __numerator(self, u : int) -> int:
        return sum(self.getItemWithValue(u) if self.opsional == "user-based" else self.getUserWithValue(u))

    def __denominator(self, u : int) -> int:
        return len(self.getItem(u) if self.opsional == "user-based" else self.getUser(u))

    def __mean_calculation(self) -> list[float]:
        return [ (self.__numerator(u)/self.__denominator(u)) if self.__denominator(u) != 0 else 0 for u in range(len(self.matrixRating if self.opsional == "user-based" else self.reverseMatrixRating))]
    
    def __mean_centered_calculation(self) -> list[float]:
        return [[ ((self.matrixRating[u][i] - self.result_mean[u]) if self.opsional == "user-based" else (self.matrixRating[u][i] - self.result_mean[i])) if self.matrixRating[u][i] != 0 else 0 for i in range(len(self.matrixRating[u]))] for u in range(len(self.matrixRating))]

    def show_mean_centered(self) :
        return self.result_mean_centered
    
    def show_mean(self) :
        return self.result_mean