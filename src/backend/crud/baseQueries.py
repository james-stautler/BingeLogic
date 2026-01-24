from db.mongodb import db 
from typing import List, Optional, Any, Dict 

async def get(collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return await db[collection].find_one(query)

async def get_many(collection: str, query: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
    pointer = db[collection].find(query).limit(limit)
    return await pointer.to_list(length=limit)

async def insert(collection: str, data: Dict[str, Any]) -> str:
    result = await db[collection].insert_one(data)
    return str(result.inserted_id)

async def update(collection: str, id_val: Any, data: Dict[str, Any]):
    return await db[collection].update_one(
        {"_id": id_val},
        {"$set": data}
    )

async def delete(collection: str, query: Dict[str, Any]):
    return await db[collection].delete_one(query)

