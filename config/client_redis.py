import os
import redis.asyncio as redis

from config.environment import settings as env
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

@asynccontextmanager
async def lifespan(app : FastAPI) :
    # On Startup

    # app.state.redis = redis.Redis(
    #     host=env.DB_HOST,
    #     port=env.DB_PORT,
    #     decode_responses=True,
    # )
    app.state.redis = redis.Redis(
        host=env.DB_HOST,
        port=env.DB_PORT,
        decode_responses=True,
        username=env.DB_USERNAME,
        password=env.DB_PASSWORD
    )

    # app.state.redis = redis.from_url(
    #     f"redis://{env.DB_HOST}:{env.DB_PORT}",
    #     decode_responses=True,
    # )

    try:
        await app.state.redis.ping()
        print("Redis connection successful")
    except Exception as e:
        print(f"Redis connection failed: {e}")
    
    print("Redis Connected created")
    
    yield
    
    # On Shutdown
    await app.state.redis.close()
    print("Redis Connected closed")

async def get_redis(request : Request) -> redis.Redis :
    return request.app.state.redis