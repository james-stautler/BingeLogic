from crud import baseQueries
from models.show_model import ShowModel
from db.mongodb import DatabaseCollections

async def get_show_by_id(show_id: str) -> Optional[ShowModel]:
    data = await baseQueries.get(DatabaseCollections.SHOWS, {"_id": show_id})
    return ShowModel(**data) if data else None

async def insert_show(show: ShowModel):
    data = show.model_dump(by_alias=True)
    return await baseQueries.insert(
        DatabaseCollections.SHOWS,
        data
    )

async def update_show(show_id: str, data: Dict[str, Any]):
    return await baseQueries.update(
        DatabaseCollections.SHOWS,
        show_id,
        data
    )

async def delete_show(show_id: str):
    return await baseQueries.delete(
        DatabaseCollections.SHOWS,
        {"_id": show_id}
    )




