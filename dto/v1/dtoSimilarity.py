from pydantic import BaseModel


class DataPassed(BaseModel):
    data : list[list] 
    k : int
    opsional : str