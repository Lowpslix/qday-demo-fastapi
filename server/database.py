from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from server.models.notes import Note, Category


async def init_db():
    client = AsyncIOMotorClient("mongodb://root:example@localhost:27017/")

    await init_beanie(database=client.notes, document_models=[Note, Category])
