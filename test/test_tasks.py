from fastapi import status

# Basic CRUD test cases

def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Test Task"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Task"
    assert data["status"] == "pending"
    assert data["priority"] == "medium"


def test_create_task_missing_title(client):
    response = client.post("/tasks/", json={"description": "No title"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_task_by_id(client):
    response = client.post("/tasks/", json={"title": "Get Task"})
    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Task"


def test_get_task_invalid_id(client):
    response = client.get("/tasks/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_task(client):
    response = client.post("/tasks/", json={"title": "Old Title"})
    task_id = response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New Title", "status": "in-progress", "priority": "high"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "in-progress"
    assert data["priority"] == "high"


def test_update_task_invalid_id(client):
    response = client.put(
        "/tasks/9999",
        json={"title": "Invalid Update", "status": "completed", "priority": "low"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task(client):
    response = client.post("/tasks/", json={"title": "Task to delete"})
    task_id = response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_200_OK

    # Ensure deleted task is gone
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_task_invalid_id(client):
    response = client.delete("/tasks/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# Additional features / filters


def test_get_all_tasks(client):
    # Create two tasks
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2", "status": "completed"})

    response = client.get("/tasks/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2


def test_get_tasks_by_status(client):
    client.post("/tasks/", json={"title": "Pending Task", "status": "pending"})
    client.post("/tasks/", json={"title": "Completed Task", "status": "completed"})

    response = client.get("/tasks/?status=completed")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    for task in data:
        assert task["status"] == "completed"

def test_get_tasks_by_invalid_status(client):
    response = client.get("/tasks/?status=invalid")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_search_tasks(client):
    client.post("/tasks/", json={"title": "Searchable Task"})
    response = client.get("/tasks/search/?to_be_filtered=Searchable")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert any("Searchable" in t["title"] for t in data)


def test_search_tasks_no_results(client):
    response = client.get("/tasks/search/?to_be_filtered=NoSuchTask")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_tasks_sorted_by_priority(client):
    client.post("/tasks/", json={"title": "High Priority", "priority": "high"})
    client.post("/tasks/", json={"title": "Low Priority", "priority": "low"})
    response = client.get("/tasks/priority/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    priorities = [t["priority"] for t in data]
    # Should start with high priority and end with low
    assert priorities[0] == "high"
    assert priorities[-1] == "low"
