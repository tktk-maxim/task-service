from contextlib import asynccontextmanager
from typing import AsyncGenerator
from tortoise.contrib.fastapi import RegisterTortoise

from fastapi import FastAPI

from config import get_db_url


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    print(f"Connecting DB {get_db_url()}")

    async with RegisterTortoise(
        application,
        db_url=get_db_url(),
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(title="Task service", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello world"}
