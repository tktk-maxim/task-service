from typing import List, TypeVar, Type
from fastapi import HTTPException
import httpx


from pydantic import BaseModel
from tortoise import Model
from tortoise.exceptions import DoesNotExist
from datetime import datetime

from models import Task


AnyPydanticModel = TypeVar('AnyPydanticModel', bound=BaseModel)
AnyTortoiseModel = TypeVar('AnyTortoiseModel', bound=Model)


async def checking_id_for_existence(tortoise_model_class: Type[AnyTortoiseModel], entity_id: int):
    try:
        await tortoise_model_class.get(id=entity_id)
    except DoesNotExist as e:
        raise HTTPException(status_code=404,
                            detail=f"{tortoise_model_class.__name__} obj with id: {entity_id} not found") from e


async def checking_employee_for_assign_task(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        events = response.json()["events"]
        current_date = datetime.now().date()
        for event in events:
            if event.begin <= current_date <= event.end:
                raise HTTPException(status_code=422,
                                    detail='It is impossible to assign a task to an employee on vacation/business trip')


async def create_entity(tortoise_model_class: Type[AnyTortoiseModel],
                        entity: AnyPydanticModel) -> AnyTortoiseModel:
    entity_obj = await tortoise_model_class.create(**entity.dict())
    return entity_obj


async def update_entity(tortoise_model_class: Type[AnyTortoiseModel],
                        entity_id: int, entity: AnyPydanticModel) -> AnyTortoiseModel:
    await checking_id_for_existence(tortoise_model_class, entity_id)

    await tortoise_model_class.filter(id=entity_id).update(**entity.dict())
    entity_obj = await tortoise_model_class.get(id=entity_id)
    return entity_obj


async def get_all_entity(tortoise_model_class: Type[AnyTortoiseModel]) -> List[AnyTortoiseModel]:
    return await tortoise_model_class.all()


async def get_entity(tortoise_model_class: Type[AnyTortoiseModel], entity_id: int) -> AnyTortoiseModel:
    await checking_id_for_existence(tortoise_model_class, entity_id)
    return await tortoise_model_class.get(id=entity_id)


async def delete_entity(tortoise_model_class: Type[AnyTortoiseModel], entity_id: int):
    await checking_id_for_existence(tortoise_model_class, entity_id)
    deleted = await tortoise_model_class.filter(id=entity_id).delete()
    if not deleted:
        raise HTTPException(status_code=404,
                            detail=f"{tortoise_model_class.__name__} obj with id: {entity_id} not found")
    return {"deleted": True}


async def search_task(name: str, description: str, project_id: int) -> List[Task]:

    response = Task.all()

    flag = False
    if name != "":
        flag = True
        response = response.filter(name=name)
    if description != "":
        flag = True
        response = response.filter(description=description)
    if project_id != -1:
        flag = True
        response = response.filter(project_id=project_id)
    return await response if flag else []


async def assign_task_employee(url: str, task_id: int, employee_id: int):
    await checking_id_for_existence(Task, task_id)
    await checking_employee_for_assign_task(url=url)

    current_date = datetime.now().date()

    await Task.filter(id=task_id).update(employee_id=employee_id, date_of_receiving=current_date)
    return await get_entity(Task, task_id)


async def add_hours_spent(task_id: int, hours: int):
    await checking_id_for_existence(Task, task_id)
    task = await Task.get(id=task_id)
    await Task.filter(id=task_id).update(hours_spent=task.hours_spent+hours)
    return await Task.filter(id=task_id).get()


async def filter_tasks(filter_param: AnyPydanticModel, employee_id: int) -> List[Task]:
    params = {key: value for key, value in filter_param.dict().items() if value is not None}

    if "more_days_to_complete" in params.keys():
        params["estimated_days_to_complete__gt"] = params.pop("more_days_to_complete")
    if "less_days_to_complete" in params.keys():
        params["estimated_days_to_complete__lt"] = params.pop("less_days_to_complete")

    response = Task.filter(employee_id=employee_id, **params).all()
    return await response


async def sort_tasks(sort_param: AnyPydanticModel) -> List[Task]:
    params = []

    for key, value in sort_param.dict().items():
        if value is not None:
            params.append(key) if value else params.append(f"-{key}")

    response = await Task.all().order_by(*params)
    return response


async def get_burning_tasks() -> List[Task]:
    tasks = await get_all_entity(Task)

    current_date = datetime.now().date()
    burning_tasks = []
    for task in tasks:
        if task.employee_id is not None:

            if 0 <= ((datetime.strptime(task.date_of_receiving, "%Y-%m-%d").date()
                     - current_date).days + task.estimated_days_to_complete) < 4:
                if not task.done:
                    burning_tasks.append(task)

    return burning_tasks
