from typing import List
from fastapi import APIRouter


from crud import create_entity, get_all_entity, get_entity, update_entity, delete_entity
from models import Project
from schemas import ProjectIn, ProjectCreate


router = APIRouter(
    tags=["Project"]
)


@router.post("/create/", response_model=ProjectIn)
async def create_project_view(project: ProjectCreate):
    project_obj = await create_entity(tortoise_model_class=Project, entity=project)
    return project_obj


@router.get("/all/", response_model=List[ProjectIn])
async def get_projects():
    projects = await get_all_entity(tortoise_model_class=Project)
    return projects


@router.get("/{project_id}", response_model=ProjectIn)
async def get_project(project_id: int):
    project = await get_entity(tortoise_model_class=Project, entity_id=project_id)
    return project


@router.put("/{project_id}", response_model=ProjectIn)
async def update_project_view(project_id: int, project: ProjectCreate):
    project_obj = await update_entity(tortoise_model_class=Project, entity=project, entity_id=project_id)
    return await project_obj


@router.delete("/{project_id}", response_model=dict)
async def delete_project_view(project_id: int):
    return await delete_entity(tortoise_model_class=Project, entity_id=project_id)
