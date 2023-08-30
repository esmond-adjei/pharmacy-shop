from contextlib import asynccontextmanager

from fastapi import FastAPI

from pharmacy.database.core import Base, SessionMaker, engine
from pharmacy.routers import users, inventories, admins


@asynccontextmanager
async def lifespan(app: FastAPI):
    with SessionMaker() as session:
        # Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(admins.router)
app.include_router(inventories.router)


@app.get("/")
def welcome():
    return {"message": "Welcome to largest online pharmacy shop"}


@app.get("/ping")
def ping_pong() -> dict[str, str]:
    return {"message": "pong... hello there!"}


@app.get("/hello/{name}")
def hello_name(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}
