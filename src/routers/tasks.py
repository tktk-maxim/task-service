from typing import List
from fastapi import APIRouter


from crud import (create_entity, get_all_entity, get_entity, update_entity, delete_entity,
                  search_task, checking_id_for_existence)
from models import Task, Project
from schemas import TaskIn, TaskCreate


router = APIRouter(
    tags=["Task"]
)


@router.post("/create/", response_model=TaskIn)
async def create_task_view(task: TaskCreate):
    await checking_id_for_existence(Project, task.project_id)
    task_obj = await create_entity(tortoise_model_class=Task, entity=task)
    return task_obj


@router.get("/all/", response_model=List[TaskIn])
async def get_tasks():
    tasks = await get_all_entity(tortoise_model_class=Task)
    return tasks


@router.get("/{task_id}", response_model=TaskIn)
async def get_task(task_id: int):
    task = await get_entity(tortoise_model_class=Task, entity_id=task_id)
    return task


@router.put("/{task_id}", response_model=TaskIn)
async def update_task_view(task_id: int, task: TaskCreate):
    await checking_id_for_existence(Project, task.project_id)
    task_obj = await update_entity(tortoise_model_class=Task, entity=task, entity_id=task_id)
    return await task_obj


@router.delete("/{task_id}", response_model=dict)
async def delete_task_view(task_id: int):
    return await delete_entity(tortoise_model_class=Task, entity_id=task_id)


@router.get("/search/", response_model=List[TaskIn])
async def search_task_view(name="", description="", project_id=""):
    return await search_task(name, description, -1 if project_id == "" else project_id)
