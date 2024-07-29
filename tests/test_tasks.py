import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_positive_create_task(client: AsyncClient) -> None:
    project = await client.post("/project/create/", json={"name": "Task-service", "description": "Description"})
    response = await client.post("/task/create/", json={
        "name": "Task-1",
        "description": "T-Description",
        "estimated_days_to_complete": 3,
        "project_id": project.json()["id"]
    })
    assert response.json()["name"] == "Task-1"


@pytest.mark.anyio
async def test_negative_create_without_name(client: AsyncClient) -> None:
    response = await client.post("/task/create/", json={
        "name": "",
        "description": "T-Description",
        "estimated_days_to_complete": 3,
        "project_id": "str"
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Field cannot be empty"


@pytest.mark.anyio
async def test_negative_create_task(client: AsyncClient) -> None:
    response = await client.post("/task/create/", json={
        "name": "Task-1",
        "description": "T-Description",
        "estimated_days_to_complete": 3,
        "project_id": "str"
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == ("Input should be a valid integer, "
                                                   "unable to parse string as an integer")


@pytest.mark.anyio
async def test_positive_update_task(client: AsyncClient) -> None:
    response = await client.get("/task/all/")
    assert response.status_code == 200
    task_id = response.json()[-1]["id"]
    response = await client.put(f"/task/{task_id}", json={
        "name": "Task-1",
        "description": "NEW-Description",
        "estimated_days_to_complete": 3,
        "project_id": response.json()[-1]["project_id"]
    })
    assert response.status_code == 200
    assert response.json()["description"] == "NEW-Description"


# @pytest.mark.anyio
# async def test_positive_assign_task_employee(client: AsyncClient) -> None:
#     response = await client.get("/task/all/")
#     assert response.status_code == 200
#     task_id = response.json()[-1]["id"]
#     response = await client.patch(f"/task/{task_id}", json={"employee_id": 1})
#     assert response.status_code == 200
#     assert response.json()["employee_id"] == 1


@pytest.mark.anyio
async def test_positive_add_hours_spent(client: AsyncClient) -> None:
    response = await client.get("/task/all/")
    assert response.status_code == 200
    task_id = response.json()[-1]["id"]
    response = await client.patch(f"/task/add_hours/{task_id}?hours=4")
    assert response.status_code == 200
    assert response.json()["hours_spent"] == 4


@pytest.mark.anyio
async def test_positive_get_task(client: AsyncClient) -> None:
    response = await client.get("/task/all/")
    assert response.status_code == 200
    task_id = response.json()[-1]["id"]
    response = await client.get(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json()["name"] is not None
    assert response.json()["description"] is not None


@pytest.mark.anyio
async def test_negative_get_task(client: AsyncClient) -> None:
    response = await client.get(f"/task/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task obj with id: -1 not found"


@pytest.mark.anyio
async def test_positive_search_task(client: AsyncClient) -> None:
    response = await client.get("/task/all/")

    task_name = response.json()[-1]["name"]
    task_description = response.json()[-1]["description"]
    task_project_id = response.json()[-1]["project_id"]

    response = await client.get(f"/task/search/?name={task_name}")
    assert response.status_code == 200
    assert response.json()[0]["name"] == task_name

    response = await client.get(f"/task/search/?description={task_description}")
    assert response.status_code == 200
    assert response.json()[0]["description"] == task_description

    response = await client.get(f"/task/search/?project_id={task_project_id}")
    assert response.status_code == 200
    assert response.json()[0]["project_id"] == task_project_id


# @pytest.mark.anyio
# async def test_positive_filter_task(client: AsyncClient) -> None:
#     response = await client.get("/task/all/")
#     task_employee_id = response.json()[-1]["employee_id"]
#     task_project_id = response.json()[-1]["project_id"]
#     task_estimated_days_to_complete = response.json()[-1]["estimated_days_to_complete"]
#
#     response = await client.get(f"/task/filter/?employee_id={task_employee_id}&project_id={task_project_id}")
#     assert response.status_code == 200
#     assert response.json()[0]["project_id"] == task_project_id
#
#     response = await client.get(f"/task/filter/?employee_id={task_employee_id}"
#                                 f"&more_days_to_complete={task_estimated_days_to_complete - 1}")
#     assert response.status_code == 200
#     assert response.json()[0]["estimated_days_to_complete"] > task_estimated_days_to_complete - 1


@pytest.mark.anyio
async def test_positive_sort_tasks(client: AsyncClient) -> None:
    response = await client.get("/task/all/")
    count_tasks = len(response.json())
    response = await client.get(f"/task/sort/?done=true")
    assert response.status_code == 200
    assert count_tasks == len(response.json())
    assert response.json()[0]["done"] == False


@pytest.mark.anyio
async def test_negative_search_task(client: AsyncClient) -> None:
    response = await client.get(f"/task/search/?project_id={-1}")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_positive_delete_task(client: AsyncClient) -> None:
    response = await client.get("/task/all/")
    task_id = response.json()[-1]["id"]
    response = await client.delete(f"/task/{task_id}")
    assert response.json()["deleted"] is True

