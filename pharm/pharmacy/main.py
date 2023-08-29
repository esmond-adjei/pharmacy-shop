from contextlib import asynccontextmanager

from fastapi import FastAPI

from pharmacy.database.core import Base, SessionMaker, engine
from pharmacy.routers.users import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    with SessionMaker() as session:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/ping")
def ping_pong() -> dict[str, str]:
    return {"message": "pong... hello there!"}


@app.get("/hello/{name}")
def hello_name(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}
