import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

class DatabaseCollections:
    SHOWS = "shows"

load_dotenv("backend.env")
uri = os.getenv("MONGO_DB_URI")
print(uri)

client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
db = client.get_database("bingelogic_db")

async def ping_database():
    try:
        await client.admin.command("ping")
        return True
    except Exception as e:
        print("Error:  " + str(e))
        return False
        


