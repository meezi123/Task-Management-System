from fastapi import FastAPI, HTTPException, Depends,BackgroundTasks, status
from sqlalchemy.orm import Session
from database import Base, engine , get_db
from task_model import Task, StatusEnum ,priorityEnum
from typing import List, Optional
from user_routes import router as user_router
from auth import get_current_user
from notify import notify_status_change
from schemas import TaskSchema

# Database setup

# Create all tables (runs once)
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(title="Task Management System")


app.include_router(user_router)


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Task Management System API"}


# Create task api
@app.post("/tasks/", response_model=TaskSchema , status_code=status.HTTP_201_CREATED)
def create_task(task: TaskSchema, db: Session = Depends(get_db) , user: str = Depends(get_current_user) ):
    try:
        db_task = Task(
            title=task.title,
            description=task.description,
            status=StatusEnum(task.status),
            priority=priorityEnum(task.priority)
        )

        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db.query(Task).filter(Task.id == db_task.id).first()

    except HTTPException:
        raise
    except Exception as e:
        # catch block for handling errors
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred: {str(e)}"
        )


# Get task by ID api
@app.get("/tasks/{task_id}", response_model=TaskSchema)
def get_task_by_id(task_id: int, db: Session = Depends(get_db),user: str = Depends(get_current_user)):
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()

        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        return db_task

    except HTTPException:
        raise
    except Exception as e:
        # catch block for handling errors
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred: {str(e)}"
        )



# Get all tasks with optional status filter api
@app.get("/tasks/", response_model=List[TaskSchema])
async def get_all_tasks(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    try:
        if status:
            try:
                status_enum = StatusEnum(status)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid status")
            # Fetch tasks with the specified status
            tasks =  db.query(Task).filter(Task.status == status_enum).all()

            if not tasks:
                raise HTTPException(
                    status_code=404,
                    detail="No tasks found with the specified status"
                )
            return tasks
        else:
            return  db.query(Task).all()

    except HTTPException:
        raise
    except Exception as e:
        # catch block for handling errors
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred: {str(e)}"
        )


# Update task api
@app.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int,
    task: TaskSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)

):
    task_to_update = db.query(Task).filter(Task.id == task_id).first()
    if not task_to_update:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task_to_update.status
    task_to_update.title = task.title
    task_to_update.description = task.description
    task_to_update.status = task.status
    task_to_update.priority = task.priority

    db.commit()
    db.refresh(task_to_update)

    # Trigger notification if status changed
    if old_status != task.status:
        background_tasks.add_task(
            notify_status_change,
            task_id=task_id,
            new_status=task_to_update.status
        )

    return task_to_update



# Delete task api
@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db),user: str = Depends(get_current_user)):
    try:
        # Fetch the task
        task_to_delete =db.query(Task).filter(Task.id == task_id).first()

        if not task_to_delete:
            raise HTTPException(status_code=404, detail="Task not found")

        # Delete the task
        db.delete(task_to_delete)
        # Commit changes
        db.commit()
        return {"message": "Task deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        # catch block for handling errors
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error occurred: {str(e)}"
        )

# Bonus Features


#Seacrh tasks by title or description api
@app.get("/tasks/search/", response_model=List[TaskSchema] )
async def search_tasks(
    to_be_filtered: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)

):
    try:
        # Search tasks by title or description
        tasks =  db.query(Task).filter(
            (Task.title.ilike(f"%{to_be_filtered}%")) | (Task.description.ilike(f"%{to_be_filtered}%"))
        ).all()

        if not tasks:
            raise HTTPException(status_code=404, detail="No such tasks exist")

        return tasks

    except HTTPException:
        raise
    except Exception as e:
        # catch block for handling errors
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred: {str(e)}"
        )


# Get tasks sorted by priority api
@app.get("/tasks/priority/", response_model=List[TaskSchema])
async def get_tasks_sorted_by_priority(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    try:
        priority_order = {
            "high": 1,
            "medium": 2,
            "low": 3
        }

        tasks = db.query(Task).all()
        # Sort tasks based on priority
        sorted_tasks = sorted(tasks, key=lambda task: priority_order[task.priority.value])

        if not sorted_tasks:
            raise HTTPException(status_code=404, detail="No tasks found")

        return sorted_tasks

    except HTTPException:
        raise
    except Exception as e:
        # catch block for handling errors
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred: {str(e)}"
        )
