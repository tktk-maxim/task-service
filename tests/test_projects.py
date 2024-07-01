import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_positive_create_project(client: AsyncClient) -> None:
    response = await client.post("/project/create/", json={"name": "Task-service", "description": "Description"})
    assert response.status_code == 200
    assert response.json()["name"] == "Task-service"


@pytest.mark.anyio
async def test_positive_update_project(client: AsyncClient) -> None:
    response = await client.get("/project/all/")
    project_id = response.json()[-1]["id"]
    response = await client.put(f"/project/{project_id}",
                                json={"name": "Task-service", "description": "NEW Description"})
    assert response.status_code == 200, response.text
    assert response.json() == {"id": project_id, "name": "Task-service", "description": "NEW Description"}


@pytest.mark.anyio
async def test_positive_get_projects(client: AsyncClient) -> None:
    response = await client.get("/project/all/")
    assert response.status_code == 200
    data = response.json()
    assert data != []


@pytest.mark.anyio
async def test_negative_get_project(client: AsyncClient) -> None:
    response = await client.get(f"/project/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Project obj with id: -1 not found"


@pytest.mark.anyio
async def test_positive_get_project(client: AsyncClient) -> None:
    response = await client.get("/project/all/")
    project_id = response.json()[-1]["id"]
    response = await client.get(f"/project/{project_id}")
    assert response.status_code == 200
    assert response.json()["name"] is not None


@pytest.mark.anyio
async def test_positive_delete_project(client: AsyncClient) -> None:
    response = await client.get("/project/all/")
    project_id = response.json()[-1]["id"]
    response = await client.delete(f"/project/{project_id}")
    assert response.json()["deleted"] is True


@pytest.mark.anyio
async def test_negative_delete_project(client: AsyncClient) -> None:
    response = await client.delete(f"/project/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Project obj with id: -1 not found"
