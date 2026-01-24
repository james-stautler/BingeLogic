from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from db.mongodb import client, ping_database
from api.health.Health import health_router, database_heartbeat
from api.routes.shows import shows_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    res = await ping_database()
    if res:
        print("Successfully connected to database")
    else:
        print("Unsuccessful connection to database")

    yield

    client.close()

app = FastAPI(
        title="BingeLogic-API",
        lifespan = lifespan)

app.include_router(health_router, prefix="/api")
app.include_router(shows_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "API IS WORKING"}

    

