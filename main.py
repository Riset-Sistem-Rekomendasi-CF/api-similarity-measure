
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller.v2.router import similarity_routers
from config.cors import cors_options
import uvicorn
from config.client_redis import lifespan

app = FastAPI(lifespan=lifespan)

# Cors Middleware
app.add_middleware(CORSMiddleware,**cors_options)

app.include_router(similarity_routers)

if __name__ == "__main__" : 
    uvicorn.run(
        app=app,
        reload=True,
        workers=1,
        port=5002
    )
