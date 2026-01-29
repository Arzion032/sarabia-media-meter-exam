# Task Manager Application

A command-line task management application built with Python that allows users to create, read, update, and delete tasks. The application uses MySQL for persistent data storage and ULID for unique task identification.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Overview](#api-overview)
- [Database Schema](#database-schema)
- [Dependencies](#dependencies)
- [File Descriptions](#file-descriptions)

## Features

- **Create Tasks**: Add new tasks with title, description, due date, and priority level
- **List Tasks**: View all tasks with their details
- **Update Tasks**: Modify existing task information
- **Mark as Completed**: Mark tasks as done
- **Delete Tasks**: Remove tasks from the system
- **Data Persistence**: All tasks are stored in a MySQL database
- **Unique IDs**: Uses ULID (Universally Unique Lexicographically Sortable Identifier) for reliable task identification
- **Input Validation**: Validates all user inputs including dates, priorities, and task status
- **Interactive Menu**: User-friendly command-line interface

## Project Structure

```
OLFU/
├── app/
│   ├── main.py              # Application entry point
│   ├── task.py              # Task model class
│   ├── task_app.py          # UI layer (command-line interface)
│   ├── task_manager.py      # Business logic layer
│   └── task_db.py           # Database abstraction layer
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules
└── .venv/                   # Virtual environment
```

## Installation & Setup

### Prerequisites

- Python 3.7+
- MySQL Server (5.7+ or 8.0+)
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd OLFU
```

### Step 2: Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

Create a MySQL database and user with the following commands:

```sql
-- Create database
CREATE DATABASE task_app;

-- Create user (if not exists)
CREATE USER 'task_user'@'localhost' IDENTIFIED BY 'taskpassword';

-- Grant privileges
GRANT ALL PRIVILEGES ON task_app.* TO 'task_user'@'localhost';
FLUSH PRIVILEGES;

-- Create tasks table
USE task_app;

CREATE TABLE tasks (
    task_id VARCHAR(26) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    due_date DATE NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    creation_date DATETIME NOT NULL
);
```

## Configuration

The database connection is configured in `app/main.py` with the following default credentials:

- **Host**: localhost
- **User**: task_user
- **Password**: taskpassword
- **Database**: task_app

**⚠️ Security Note**: These credentials are hardcoded for simplicity. For production, use environment variables or a `.env` file.

To customize, modify the connection parameters in `app/main.py`:

```python
db = TaskDB(user="your_user", password="your_password", database="your_database")
```

## Usage

### Running the Application

```bash
cd app
python main.py
```

### Menu Options

Once the application runs, you'll see the following menu:

```
=== TASK MANAGER ===
1. Add Task
2. List Tasks
3. Update Task
4. Mark Task as Done
5. Remove Task
Q. Quit
```

### Adding a Task

```
Choose an option: 1
--- Add New Task ---
Title: Complete project report
Description: Finish the quarterly report for Q1 2026
Due Date (YYYY-MM-DD): 2026-02-15
Priority Level (Low, Medium, High) Default[Medium]: High
Status (Pending, In Progress, Completed) Default[Pending]: In Progress
Task 'Complete project report' added with ID 01ARZ3NDEKTSV4RRFFQ69G5FAV
```

### Listing Tasks

```
Choose an option: 2
--- Task List ---
ID: 01ARZ3NDEKTSV4RRFFQ69G5FAV | Title: Complete project report | Due: 2026-02-15 | Priority: High | Status: In Progress
```

### Updating a Task

```
Choose an option: 3
-- Update Task --
Task ID: 01ARZ3NDEKTSV4RRFFQ69G5FAV

Current Task Details:
Title                Description                     Due Date     Priority   Status
------------------------------------------------------------------------------------------
Complete project r Finish the quarterly report for  2026-02-15   High       In Progress

Enter new values (leave blank to keep current):
New Title: 
New Description: Update with latest figures
New Priority (Low/Medium/High): 
New Status (Pending/In Progress/Completed): Completed
New Due Date (YYYY-MM-DD): 
```

### Marking Task as Done

```
Choose an option: 4
Task ID: 01ARZ3NDEKTSV4RRFFQ69G5FAV
Task marked as completed.
```

### Removing a Task

```
Choose an option: 5
Task ID: 01ARZ3NDEKTSV4RRFFQ69G5FAV
Task removed successfully.
```

## API Overview

### Task Class (`task.py`)

The `Task` class represents a single task with the following attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| task_id | str | Unique ULID identifier (auto-generated) |
| title | str | Task title |
| description | str | Task description |
| due_date | date | Task due date |
| priority | str | Priority level (Low, Medium, High) |
| status | str | Task status (Pending, In Progress, Completed) |
| creation_date | datetime | Timestamp when task was created |

**Methods:**
- `mark_as_done()` - Changes task status to "Completed"

### TaskManager Class (`task_manager.py`)

Handles business logic and validation:

**Methods:**
- `add_task(title, description, due_date, priority_lvl, status)` - Create a new task with validation
- `list_tasks()` - Retrieve all tasks
- `update_task(task_id, **kwargs)` - Update task fields
- `mark_task_as_completed(task_id)` - Mark task as done
- `remove_task(task_id)` - Delete a task

**Validation includes:**
- Non-empty title and description
- Valid due date (not in the past)
- Valid priority level (Low, Medium, High)
- Valid status (Pending, In Progress, Completed)

### TaskDB Class (`task_db.py`)

Handles database operations:

**Methods:**
- `connect()` - Establish MySQL connection
- `create_task(task)` - Insert task into database
- `fetch_all_tasks()` - Retrieve all tasks from database
- `update_task(task_id, **kwargs)` - Update task in database
- `delete_task(task_id)` - Delete task from database
- `close()` - Close database connection

### TaskApp Class (`task_app.py`)

Handles user interface and user interactions:

**Methods:**
- `run()` - Start the interactive menu loop
- `show_menu()` - Display menu options
- `add_task()` - Handle task creation flow
- `list_tasks()` - Handle task listing flow
- `update_task()` - Handle task update flow
- `mark_completed()` - Handle task completion flow
- `remove_task()` - Handle task deletion flow

## Database Schema

### tasks Table

```sql
CREATE TABLE tasks (
    task_id VARCHAR(26) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    due_date DATE NOT NULL,
    priority VARCHAR(20) NOT NULL CHECK (priority IN ('Low', 'Medium', 'High')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('Pending', 'In Progress', 'Completed')),
    creation_date DATETIME NOT NULL
);
```

## Dependencies

Listed in `requirements.txt`:

- **ulid-py** - For generating ULIDs (Universally Unique Lexicographically Sortable Identifiers)
- **mysql-connector-python** - For MySQL database connectivity

## File Descriptions

### `app/main.py`

Application entry point that:
- Initializes the MySQL database connection
- Creates the TaskApp UI instance
- Runs the application loop
- Properly closes database connection on exit

### `app/task.py`

Defines the `Task` class with:
- Task attributes (title, description, due_date, priority, status)
- ULID generation for unique identification
- `mark_as_done()` method to update status

### `app/task_manager.py`

Core business logic layer with:
- Task CRUD operations
- Input validation (dates, priorities, status)
- Database integration
- In-memory task caching

### `app/task_db.py`

Database abstraction layer with:
- MySQL connection management
- SQL queries for task operations
- Task serialization to/from database
- Connection error handling

### `app/task_app.py`

User interface layer with:
- Interactive command-line menu
- User input handling and validation
- Task workflow management
- Formatted output display

## Error Handling

The application includes error handling for:

- Invalid date formats (expects YYYY-MM-DD)
- Past due dates
- Empty required fields
- Invalid priority/status values
- Invalid task IDs
- Database connection errors
- General exceptions with user-friendly messages

## Architecture

The application follows a **layered architecture** pattern:

```
┌─────────────────────────────────────┐
│      TaskApp (UI Layer)             │
│  - User interaction                 │
│  - Input/Output handling            │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   TaskManager (Business Logic)      │
│  - Task validation                  │
│  - CRUD operations                  │
│  - Business rules                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   TaskDB (Data Access Layer)        │
│  - Database connectivity            │
│  - SQL queries                      │
│  - Data persistence                 │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│       MySQL Database                │
│  - Data storage                     │
└─────────────────────────────────────┘
```

## Future Enhancements

Potential improvements to consider:

- User authentication and authorization
- Task categories/tags/labels
- Task filtering and sorting options
- Data export (CSV, JSON, PDF)
- Task search and advanced filtering
- Environment variable configuration (.env)
- Unit tests and integration tests
- Web API (Flask/FastAPI)
- Web UI (React/Vue)
- Task scheduling and reminders
- Recurring tasks

## Troubleshooting

### Database Connection Issues

If you encounter "Error connecting to MySQL", verify:
- MySQL server is running
- Database credentials are correct
- Database and table exist
- User has proper permissions

### Date Format Issues

Always use the format `YYYY-MM-DD` (e.g., `2026-02-15`)

### Module Import Errors

Ensure you're running the application from the `app/` directory:
```bash
cd app
python main.py
```

## License

This project is provided as-is. Include your license information here if applicable.

## Support

For issues or questions, please refer to the project repository or contact the development team.
