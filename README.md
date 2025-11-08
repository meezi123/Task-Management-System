# Task Management System

A **FastAPI**-based Task Management System that allows users to manage tasks efficiently. This project includes all mandatory CRUD operations as well as additional bonus features such as task search and priority sorting.

---

## Features

- **User Authentication**: Register and login to get an access token.  
- **Task Management**:  
  - Create, read, update, and delete tasks  
  - Filter tasks by status  
  - Search tasks by title or description  
  - Get tasks sorted by priority  
- **Authorization**: Secure API endpoints using access tokens.  
- **Bonus Features**

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/meezi123/Task-Management-System
cd Task-Management-System
```
2. Create a virtual environment and activate it:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Linux/Mac
source .venv/bin/activate

```
3. Install the required packages:
```bash
pip install -r requirements.txt
```
## Running the Server
1. Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```
- The server will be available at: http://127.0.0.1:8000
## Running Tests

1. Run all test cases using pytest:
```bash
pytest -v
```
## How to Use
- Register a new user via the API.

- Login using your credentials to get an access token.

- Click the Authorize button in the Swagger UI and provide your username and password.

- Once authorized, you can perform all task operations.

## API Documentation

1. FastAPI automatically generates API docs:

- Swagger UI: http://127.0.0.1:8000/docs

- ReDoc: http://127.0.0.1:8000/redoc

## Bonus Features
- Searching based on title and description
- Sorting based on priority (low to high)
- JWT authentication (secure routes)
- Background tasks notification
## Author

- Rameez Qureshi
- Computer Science Graduate, FAST NUCES Lahore

