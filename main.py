from fastapi import FastAPI,HTTPException
import time
import asyncio
import logging

import pymysql
from db import getLock

class TimeoutError(Exception):
    pass

# Create an instance of FastAPI
app = FastAPI()


    
@app.get("/{seat_id}")
async def read_root(seat_id):
    try:
        await getLock(seat_id=seat_id)
    except pymysql.Error as e:
        raise HTTPException(400,"could not acquire lock")
    except TimeoutError as e:
        raise HTTPException(400,"timeout")
    return {"mssg":"Acquired and released lock"}


