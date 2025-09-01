from fastapi import APIRouter, HTTPException, Depends, Request
import measure.v2.similarities as sm
from dto.v1.dtoSimilarity import DataPassed

from middleware import SlidingWindowLog

limiter = SlidingWindowLog(rate_limit=50, per_seconds=10)

similarity_routers = APIRouter(redirect_slashes=False,prefix="/api/v2",dependencies=[Depends(limiter)])

@similarity_routers.post("/tversky")
async def tversky(data : DataPassed) :
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    tversky = sm.TI(data.data,opsional=data.opsional,k=data.k)

        
    return {
        "error" : False,
        "data" : {
            "mean-list" : tversky.show_mean(data.opsional),
            "mean-centered" : tversky.show_mean_centered(data.opsional),
            "similarity" : tversky.show_similarity(),
            "prediction" : tversky.get_a_bunch_of_prediction(20),
            "top-n" : tversky.get_top_n_array(),
            "reduced-data" : tversky.get_reduced_data(),
        } 
    }

@similarity_routers.post("/pearson")
async def pearson(data : DataPassed) :
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    pearson = sm.Pearson(data.data,opsional=data.opsional,k=data.k)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : pearson.show_mean(data.opsional),
            "mean-centered" : pearson.show_mean_centered(data.opsional),
            "similarity" : pearson.show_similarity(),
            "prediction" : pearson.get_a_bunch_of_prediction(20),
            "top-n" : pearson.get_top_n_array(),
            "reduced-data" : pearson.get_reduced_data(),
        } 
    }

@similarity_routers.post("/cosine")
async def cosine(data : DataPassed) :
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    cosine = sm.Cosine(data.data,opsional=data.opsional,k=data.k)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : cosine.show_mean(data.opsional),
            "mean-centered" : cosine.show_mean_centered(data.opsional),
            "similarity" : cosine.show_similarity(),
            "prediction" : cosine.get_a_bunch_of_prediction(20),
            "top-n" : cosine.get_top_n_array(),
            "reduced-data" : cosine.get_reduced_data(),
        } 
    }

@similarity_routers.post("/acosine")
async def acosine(data : DataPassed) :
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    acosine = sm.ACosine(data.data,opsional=data.opsional,k=data.k)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : acosine.show_mean("user-based" if data.opsional == "item-based" else "item-based"),
            "mean-centered" : acosine.show_mean_centered("user-based" if data.opsional == "item-based" else "item-based"),
            "similarity" : acosine.show_similarity(),
            "prediction" : acosine.get_a_bunch_of_prediction(20),
            "top-n" : acosine.get_top_n_array(),
            "reduced-data" : acosine.get_reduced_data(),
        } 
    }

@similarity_routers.post("/bc")
async def bc(data : DataPassed):
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    bc = sm.BC(data.data,opsional=data.opsional,k=data.k)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : bc.show_mean(data.opsional),
            "mean-centered" : bc.show_mean_centered(data.opsional),
            "similarity" : bc.show_similarity(),
            "probability" : bc.show_probabilities(),
            "prediction" : bc.get_a_bunch_of_prediction(20),
            "top-n" : bc.get_top_n_array(),
            "reduced-data" : bc.get_reduced_data(),
        } 
    }