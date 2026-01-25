from crud import baseQueries
from models.show_model import ShowModel
from db.mongodb import DatabaseCollections
from typing import Optional, Dict, List, Any

async def db_get_show_by_id(show_id: int) -> Optional[ShowModel]:
    data = await baseQueries.get(DatabaseCollections.SHOWS, {"_id": show_id})
    return ShowModel(**data) if data else None

async def db_insert_show(show: ShowModel):
    data = show.model_dump(by_alias=True)
    return await baseQueries.insert(
        DatabaseCollections.SHOWS,
        data
    )

async def db_update_show(show_id: int, data: Dict[str, Any]):
    return await baseQueries.update(
        DatabaseCollections.SHOWS,
        show_id,
        data
    )

async def db_delete_show(show_id: int):
    return await baseQueries.delete(
        DatabaseCollections.SHOWS,
        {"_id": show_id}
    )

async def db_delete_many_shows(show_ids: List[int]):
    return await baseQueries.delete_many(
        DatabaseCollections.SHOWS,
        show_ids
    )

def db_get_cursor(projection: Optional[Dict[str, Any]]):
    return baseQueries.get_cursor(
        DatabaseCollections.SHOWS,
        projection
    )




