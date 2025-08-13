from numpy import transpose
from measure.v2.mean import Mean
from operator import itemgetter,mul
import copy

class Prediction(Mean):

    def __init__(
                self,
                data,
                similarity : None| list[list[float]] = None,
                *, 
                opsional : str|None = None,
                k : int|None = None, 
                toyData : bool = True,
            ) -> None :

        super().__init__(data,opsional=opsional,toyData=toyData)

        self.similarity = similarity if opsional == "user-based" else transpose(similarity)
        self.data_for_prediction = copy.deepcopy(data)
        self.matrixRating = data
        self.reverseMatrixRating = transpose(self.matrixRating).tolist()
        self.result_mean_centered_for_prediction = transpose(self.result_mean_centered).tolist() if opsional == "user-based" else self.result_mean_centered
        self.k = k
        self.prediction = self.main_prediction_calculation()      

        self.topN = self.get_top_n()

    def __numerator(self,u,i,nearestNeighborhood) -> float :
        return sum( list( 
            map(mul,itemgetter(*nearestNeighborhood)(self.similarity[ u  if self.opsional == "user-based" else i ]),
            itemgetter(*nearestNeighborhood)(self.result_mean_centered_for_prediction[ u  if self.opsional == "item-based" else i ])) 
            )) if len(nearestNeighborhood) > 1 else (self.similarity[ u  if self.opsional == "user-based" else i ][nearestNeighborhood[0]]*self.result_mean_centered_for_prediction[ u  if self.opsional == "item-based" else i ][nearestNeighborhood[0]])

    def __denominator(self,u,i,nearestNeighborhood) -> float :
        return sum( list(map(lambda x : abs(x),itemgetter(*nearestNeighborhood)(self.similarity[u if self.opsional == "user-based" else i])))) if len(nearestNeighborhood) > 1 else abs(self.similarity[u if self.opsional == "user-based" else i][nearestNeighborhood[0]])

    def selected_neighborhood(self,u,i) -> list[float]:

        indices = list(set(self.getUser(i))) if self.opsional == "user-based" else list(set(self.getItem(u)))
        similarity_selected = self.similarity[u if self.opsional == "user-based" else i]

        if len(indices) > 1 :
            indices = sorted(indices,key=lambda x : similarity_selected[x],reverse=True)
        else :
            return indices if len(indices) >= 1 else []

        return indices[:self.k]
        

    def prediction_calculation(self, u, i) -> float :
        
        nearestNeighborhood = self.selected_neighborhood(u,i)
        average = self.result_mean[u if self.opsional == "user-based" else i]

        if len(nearestNeighborhood) != 0 :
            numerator = self.__numerator(u,i,nearestNeighborhood)
            denom = self.__denominator(u,i,nearestNeighborhood)
        else :
            return 0

        return (average + (numerator / denom)) if denom != 0 else 0

    def main_prediction_calculation(self) -> None :
        result = copy.deepcopy(self.data_for_prediction)
        for u in range(len(self.matrixRating)) :
            for i in range(len(self.matrixRating[0])) :
                result[u][i] = self.prediction_calculation(u,i) if self.matrixRating[u][i] == 0 else self.matrixRating[u][i]
        return result
    
    def get_top_n(self) :
        result = []
        for i in range(len(self.data_for_prediction) ) :
            unratedItem = self.getItem(i,interacted=False)
            if len(unratedItem) > 1 :

                if len(unratedItem) == 0 :
                    result.append([])
                    continue
                
                sorted_array = sorted(unratedItem,key=lambda x: self.prediction[i][x],reverse=True) if len(unratedItem) > 1 else self.prediction[i][unratedItem[0]]

                result.append(sorted_array)
            else :
                result.append(unratedItem)
        
        return result

    def get_top_n_specific_user(self, u) :
        return self.topN[u]
    
    def show_prediction(self):
        return self.prediction

    def get_top_n_array(self) :
        return self.topN

