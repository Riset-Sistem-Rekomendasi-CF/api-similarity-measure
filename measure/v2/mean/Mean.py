import pandas as pd
from numpy import transpose
from measure.v2.MatrixRating import MatrixRating

class Mean(MatrixRating) :

    def __init__(self, data,*,opsional="user-based", toyData : bool = True) :
        super().__init__(data,toyData=toyData)
        
        self.opsional = opsional
        self.result_overall_mean = self.__dozen_mean()
        self.result_overall_mean_and_mean_centered = self.__dozen_mean_and_mean_centered()
        
        self.result_mean = self.result_overall_mean_and_mean_centered["mean"][opsional]
        self.result_mean_centered = self.result_overall_mean_and_mean_centered["mean-centered"][opsional]

    
    def __numerator(self, u : int, opsional) -> int:
        return sum(self.getItemWithValue(u) if opsional == "user-based" else self.getUserWithValue(u))

    def __denominator(self, u : int, opsional) -> int:
        return len(self.getItem(u) if opsional == "user-based" else self.getUser(u))

    def __mean_calculation(self,opsional) -> list[float]:
        return [ (self.__numerator(u,opsional)/self.__denominator(u,opsional)) if self.__denominator(u,opsional) != 0 else 0 for u in range(len(self.matrixRating if opsional == "user-based" else self.reverseMatrixRating))]
    
    def __mean_centered_calculation(self,opsional) -> list[float]:
        return [[ ((self.matrixRating[u][i] - self.result_overall_mean[opsional][u]) if opsional == "user-based" else (self.matrixRating[u][i] - self.result_overall_mean[opsional][i])) if self.matrixRating[u][i] != 0 else 0 for i in range(len(self.matrixRating[u]))] for u in range(len(self.matrixRating))]

    def __dozen_mean(self) :
        return {
                "user-based" : self.__mean_calculation("user-based"),
                "item-based" : self.__mean_calculation("item-based"),
            }

    def __dozen_mean_and_mean_centered(self) :
        return {
            "mean" : {
                "user-based" : self.result_overall_mean["user-based"],
                "item-based" : self.result_overall_mean["item-based"],
            },
            "mean-centered" : {
                "user-based" : self.__mean_centered_calculation("user-based"),
                "item-based" : self.__mean_centered_calculation("item-based"),
            }
        }

    def show_mean_centered(self,opsional) :
        return self.result_overall_mean_and_mean_centered["mean-centered"][opsional]
    
    def show_mean(self,opsional) :
        return self.result_overall_mean_and_mean_centered["mean"][opsional]