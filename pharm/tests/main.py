from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()
engin = create_engine("sqlite:///./pharm.db", echo=True)


@app.get("/ping")
def ping_pong() -> dict[str, str]:
    return {"message": "pong... hello there!"}


@app.get("/hello/{name}")
def hello_name(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}


app.post("/hello")


def hello_name_post(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}
