from fastapi import HTTPException
from typing import List, TypeVar, Type

from pydantic import BaseModel
from tortoise import Model
from tortoise.exceptions import DoesNotExist


AnyPydanticModel = TypeVar('AnyPydanticModel', bound=BaseModel)
AnyTortoiseModel = TypeVar('AnyTortoiseModel', bound=Model)


async def checking_id_for_existence(tortoise_model_class: Type[AnyTortoiseModel], entity_id: int):
    try:
        await tortoise_model_class.get(id=entity_id)
    except DoesNotExist:
        raise HTTPException(status_code=404,
                            detail=f"{tortoise_model_class.__name__} obj with id: {entity_id} not found")


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

