from fastapi import APIRouter, HTTPException
import measure.v2.similarities as sm

from dto.v1.dtoSimilarity import DataPassed

similarity_routers = APIRouter(prefix="/api/v2")

@similarity_routers.post("/tversky")
async def tversky(data : DataPassed) :
    if data.data == [] and data.k == 0 and data.opsional:
        raise HTTPException(status_code=404,detail="Data yang kamu kirimkan kosong")

    tversky = sm.TI(data.data,opsional=data.opsional,k=data.k)
    
    return {
        "error" : False,
        "data" : {
            "mean-list" : tversky.show_mean(),
            "mean-centered" : tversky.show_mean_centered(),
            "similarity" : tversky.show_similarity(),
            "prediction" : tversky.show_prediction(),
            "top-n" : tversky.get_top_n_array(),
            "reduced-data" : tversky.get_reduced_data(),
        } 
    }