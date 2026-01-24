from fastapi import APIRouter
from db.mongodb import client
from datetime import datetime

health_router = APIRouter(prefix="/health", tags=["System"])

@health_router.get("/")
async def database_heartbeat():

    heartbeat = {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "dependencies": {
            "database": "unknown"
        }
    }

    try:
        await client.admin.command("ping")
        heartbeat["dependencies"]["database"] = "online"
    except Exception as e:
        heartbeat["status"] = "error"
        heartbeat["dependencies"]["database"] = f"{str(e)}"

    return heartbeat
