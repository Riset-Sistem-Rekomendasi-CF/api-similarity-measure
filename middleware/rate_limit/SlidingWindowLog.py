import redis.asyncio as redis
import time

from fastapi import HTTPException, Request, Depends
from config.client_redis import get_redis
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

# Code By Gemini
class SlidingWindowLog() :
    def __init__(self, rate_limit, per_seconds):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds

    async def __call__(self, request : Request, redis_client: redis.Redis = Depends(get_redis)) : 
        ip = request.client.host
        current_time = time.time()
        
        # Create a unique key for each user's sorted set in Redis
        key = f"rate_limit:{ip}"
        
        # The window is from (current_time - window_size) to current_time
        window_start = current_time - self.per_seconds

        # Use a Redis pipeline for atomic operations
        async with redis_client.pipeline() as pipe:
            # 1. Clean Up Old Logs: Remove timestamps older than our window
            #    ZREMRANGEBYSCORE removes members with a score between -inf and window_start
            await pipe.zremrangebyscore(key, '-inf', window_start)

            # 2. Count: Get the number of requests in the current window
            await pipe.zcard(key)

            # Execute the commands and get the results
            results = await pipe.execute()
            current_count = results[1]

        # 3. Decide: Check if the current count is at the limit
        print(current_count)
        print(self.rate_limit)
        if current_count >= self.rate_limit:
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded.",
            )

        # 4. Log the Timestamp: Add the current request's timestamp to the sorted set.
        #    We use the timestamp for both the score and the member.
        #    Adding a unique member value prevents items with the exact same score from being treated as one.
        await redis_client.zadd(key, {f"{current_time}": current_time})
        
        # Set an expiration on the key so Redis doesn't fill up with old user data
        await redis_client.expire(key, self.per_seconds)
