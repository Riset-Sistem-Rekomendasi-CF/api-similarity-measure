from pydantic import BaseModel


class DataPassed(BaseModel):
    data : list 
    k : int
    opsional : str