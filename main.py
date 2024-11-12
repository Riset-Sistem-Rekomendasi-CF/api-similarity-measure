
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.v1.route import similarity_routers
from config.config import cors_options

app = FastAPI()

app.add_middleware(CORSMiddleware,**cors_options)

app.include_router(similarity_routers)

