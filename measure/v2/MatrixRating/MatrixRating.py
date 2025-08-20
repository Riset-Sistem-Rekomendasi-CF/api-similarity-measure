import numpy as np 
import pandas as pd

Vector = list[float|int]
Matrix = list[list[float|int]]

class MatrixRating():

    def __init__(self, data : Matrix | str ,*, toyData : bool = True):
        """
        Parameters :
            matrix : str | list[list[float]]
                The path of folder movielens or matrix rating

            data : str | list[list[float]]
                The path of data or Data matrix

            reverseMatrixRating : list[list[float]]
                Reverse of matrix rating
        """
        self.data = data
        self.toyData = toyData

        if type(data) is str :
            raise ValueError(f"{self} data should be type list")

        self.matrixRating = data
        self.reverseMatrixRating = np.transpose(self.matrixRating).tolist()
        
        self.highest_rating = int(max([max(column) for column in self.matrixRating]))
        self.lowest_rating = int( min([ min(list(filter(lambda x : x!=0 , column))) for column in self.matrixRating]))

        self.__matrix_component_of_item = self.__dozenOfItem()
        self.__matrix_component_of_user = self.__dozenOfUser()

    def __dozenOfItem(self) -> dict :
        return {
            "unrated" : [[j for j in range(len(self.matrixRating[0])) if self.matrixRating[i][j] == 0 ] for i in range(len(self.matrixRating))],
            "rated" : [[j for j in range(len(self.matrixRating[0])) if self.matrixRating[i][j] != 0 ] for i in range(len(self.matrixRating))]
        }

    def __dozenOfUser(self) -> dict[str : Matrix ] :
        return {
            "unrated" : [[j for j in range(len(self.reverseMatrixRating[0])) if self.reverseMatrixRating[i][j] == 0 ] for i in range(len(self.reverseMatrixRating))],
            "rated" : [[j for j in range(len(self.reverseMatrixRating[0])) if self.reverseMatrixRating[i][j] != 0 ] for i in range(len(self.reverseMatrixRating))]
        }

    def getItem(self, user : int,*, interacted : bool = True) -> Vector :
        label = "rated" if interacted else "unrated"

        if user > len(self.__matrix_component_of_item[label]) :
            raise ValueError("Data akses melebihi matriks")

        return self.__matrix_component_of_item[label][user]

    def getUser(self ,item : int,*,interacted: bool|None = True) -> Vector :
        label = "rated" if interacted else "unrated"

        if item > len(self.__matrix_component_of_user[label]) :
            raise ValueError("Data akses melebihi matriks")

        return self.__matrix_component_of_user[label][item]
    
    def getItemWithValue(self,user : int) -> Vector :
        return self.matrixRating[user]

    def getUserWithValue(self, item : int) -> Vector :
        return self.reverseMatrixRating[item]

    def showMatrix(self,u) -> pd :
        return pd.DataFrame(self.train[u])
