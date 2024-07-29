from typing import List, Annotated
from fastapi import APIRouter, Depends

from crud import (create_entity, get_all_entity, get_entity, update_entity, delete_entity,
                  search_task, checking_id_for_existence, assign_task_employee, add_hours_spent,
                  filter_tasks, checking_employee_for_assign_task, sort_tasks)
from models import Task, Project
from schemas import TaskIn, TaskCreate, TaskUpdateEmployeeId, TaskFilter, TaskSort
from config import settings

router = APIRouter(
    tags=["Task"]
)


@router.post("/create/", response_model=TaskIn)
async def create_task_view(task: TaskCreate):
    await checking_id_for_existence(Project, task.project_id)
    if task.employee_id:
        await checking_employee_for_assign_task(url=f"http://{settings.user_service_host}:{settings.user_service_port}"
                                                    f"/employee/card/{task.employee_id}")
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
    if task.employee_id:
        await checking_employee_for_assign_task(url=f"http://{settings.user_service_host}:{settings.user_service_port}"
                                                    f"/employee/card/{task.employee_id}")
    task_obj = await update_entity(tortoise_model_class=Task, entity=task, entity_id=task_id)
    return await task_obj


@router.delete("/{task_id}", response_model=dict)
async def delete_task_view(task_id: int):
    return await delete_entity(tortoise_model_class=Task, entity_id=task_id)


@router.get("/search/", response_model=List[TaskIn])
async def search_task_view(name="", description="", project_id=""):
    return await search_task(name, description, -1 if project_id == "" else project_id)


@router.patch("/{task_id}", response_model=TaskIn)
async def assign_task_employee_view(task_id: int, task_update_employee_id: TaskUpdateEmployeeId):
    task_obj = await assign_task_employee(url=f"http://{settings.user_service_host}:{settings.user_service_port}"
                                              f"/employee/card/{task_update_employee_id.employee_id}",
                                          task_id=task_id,
                                          employee_id=task_update_employee_id.employee_id)
    return await task_obj


@router.patch("/add_hours/{task_id}", response_model=TaskIn)
async def add_hours_spent_view(task_id: int, hours: int):
    await checking_id_for_existence(Task, task_id)
    task_obj = await add_hours_spent(task_id=task_id, hours=hours)
    return await task_obj


@router.get("/filter/", response_model=List[TaskIn])
async def filter_tasks_view(employee_id: int, filter_param: TaskFilter = Depends()):
    tasks = await filter_tasks(employee_id=employee_id, filter_param=filter_param)
    return tasks


@router.get("/sort/", response_model=List[TaskIn])
async def sort_tasks_view(sort_param: TaskSort = Depends()):
    tasks = await sort_tasks(sort_param=sort_param)
    return tasks
