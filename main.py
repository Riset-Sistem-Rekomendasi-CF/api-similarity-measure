import similarity as sm

from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app = FastAPI()

class DataPassed(BaseModel):
    data : list 
    k : int
    opsional : int

@app.post("/pearson")
async def pearson(data : DataPassed):
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    pearson = sm.Pearson(data.data,opsional=1,k=3)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : pearson.getMeanListArray(),
            "mean-centered" : pearson.getMeanCenteredArray(),
            "similarity" : pearson.getSimilarityArray(),
            "prediction" : pearson.getPredictionArray(),
        } 
    }


@app.post("/cosine")
async def cosine(data : DataPassed):
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    cosine = sm.Cosine(data.data,opsional=1,k=3)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : cosine.getMeanListArray(),
            "mean-centered" : cosine.getMeanCenteredArray(),
            "similarity" : cosine.getSimilarityArray(),
            "prediction" : cosine.getPredictionArray(),
        } 
    }

@app.post("/acosine")
async def acosine(data : DataPassed):
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    acosine = sm.ACosine(data.data,opsional=1,k=3)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : acosine.getMeanListArray(),
            "mean-centered" : acosine.getMeanCenteredArray(),
            "similarity" : acosine.getSimilarityArray(),
            "prediction" : acosine.getPredictionArray(),
        } 
    }

@app.post("/bc")
async def bc(data : DataPassed):
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    bc = sm.BC(data.data,opsional=1,k=3)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : bc.getMeanListArray(),
            "mean-centered" : bc.getMeanCenteredArray(),
            "similarity" : bc.getSimilarityArray(),
            "prediction" : bc.getPredictionArray(),
        } 
    }



