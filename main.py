from fastapi import FastAPI

from server.database import init_db
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from server.routes.notes import router as notes_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(notes_router, tags=["User Operations"])


@app.on_event("startup")
async def start_db():
    await init_db()
