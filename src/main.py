from contextlib import asynccontextmanager
from typing import AsyncGenerator
from tortoise.contrib.fastapi import RegisterTortoise

from fastapi import FastAPI

from config import get_db_url, settings


from routers.projects import router as router_project


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    print(f"Connecting DB {get_db_url(settings.run_test)}")

    async with RegisterTortoise(
        application,
        db_url=get_db_url(settings.run_test),
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(title="Task service", lifespan=lifespan)


app.include_router(
    router=router_project,
    prefix="/project",
    tags=["Project"]
)


@app.get("/")
async def root():
    return {"message": "Hello world"}
