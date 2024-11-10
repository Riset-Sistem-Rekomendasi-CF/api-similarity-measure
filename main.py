import similarity as sm

from fastapi import FastAPI , HTTPException , APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataPassed(BaseModel):
    data : list 
    k : int
    opsional : str

@app.post("/pearson")
async def pearson(data : DataPassed):
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    pearson = sm.Pearson(data.data,opsional=data.opsional,k=data.k)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : pearson.getMeanListArray(),
            "mean-centered" : pearson.getMeanCenteredArray(),
            "similarity" : pearson.getSimilarityArray(),
            "prediction" : pearson.getPredictionArray(),
            "reduced-data" : pearson.getReducedDataArray(),
        } 
    }


@app.post("/cosine")
async def cosine(data : DataPassed):
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    cosine = sm.Cosine(data.data,opsional=data.opsional,k=data.k)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : cosine.getMeanListArray(),
            "mean-centered" : cosine.getMeanCenteredArray(),
            "similarity" : cosine.getSimilarityArray(),
            "prediction" : cosine.getPredictionArray(),
            "top-n" : cosine.getTopNArray(),
            "reduced-data" : cosine.getReducedDataArray(),
        } 
    }

@app.post("/acosine")
async def acosine(data : DataPassed):
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    acosine = sm.ACosine(data.data,opsional=data.opsional,k=data.k)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : acosine.getMeanListArray(),
            "mean-list-brother" : acosine.getMeanBrotherArray(),
            "mean-centered" : acosine.getMeanCenteredArray(),
            "mean-centered-brother" : acosine.getMeanCenteredBrotherArray(),
            "similarity" : acosine.getSimilarityArray(),
            "prediction" : acosine.getPredictionArray(),
            "top-n" : acosine.getTopNArray(),
            "reduced-data" : acosine.getReducedDataArray(),
        } 
    }

@app.post("/bc")
async def bc(data : DataPassed):
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    bc = sm.BC(data.data,opsional=data.opsional,k=data.k)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : bc.getMeanListArray(),
            "mean-centered" : bc.getMeanCenteredArray(),
            "similarity" : bc.getSimilarityArray(),
            "probability" : bc.getProbabilityArray(),
            "prediction" : bc.getPredictionArray(),
            "top-n" : bc.getTopNArray(),
            "reduced-data" : bc.getReducedDataArray(),
        } 
    }



