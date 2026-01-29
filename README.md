# Task Manager Application

A command-line task management application built with Python that allows users to create, read, update, and delete tasks. The application uses MySQL for persistent data storage and ULID for unique task identification.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Database Setup Guide](#database-setup-guide)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Overview](#api-overview)
- [File Descriptions](#file-descriptions)
- [Troubleshooting](#troubleshooting)

## Features

- **Create Tasks**: Add new tasks with title, description, due date, and priority level
- **List Tasks**: View all tasks with their details
- **Update Tasks**: Modify existing task information
- **Mark as Completed**: Mark tasks as done
- **Delete Tasks**: Remove tasks from the system
- **Data Persistence**: All tasks are stored in a MySQL database
- **Unique IDs**: Uses ULID for unique task identification
- **Input Validation**: Comprehensive validation for all inputs
- **Interactive Menu**: User-friendly command-line interface

## Project Structure

```
OLFU/
├── app/
│   ├── main.py              # Application entry point
│   ├── task.py              # Task model class
│   ├── task_app.py          # UI layer
│   ├── task_manager.py      # Business logic layer
│   └── task_db.py           # Database layer
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── .venv/                   # Virtual environment
```

## Installation & Setup

### Prerequisites

- Python 3.7+
- MySQL Server
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

### Step 4: Database Setup (See detailed guide below)

Follow the **Database Setup Guide** section to create the MySQL database and tables.

## Database Setup Guide

### Task Management App – Database Setup

This guide will help you set up MySQL for the Task Management App on a Linux system.

#### 1. Install MySQL

If you don't have MySQL installed, run:

```bash
sudo apt update
sudo apt install mysql-server
```

Check the installation:

```bash
mysql --version
```

#### 2. Log in as MySQL root

```bash
sudo mysql
```

On a fresh Linux install, root uses socket authentication (no password).

You should see the MySQL prompt:

```
mysql>
```

#### 3. Create the database

```sql
CREATE DATABASE task_app;
USE task_app;
```

`task_app` is the database where all tasks will be stored.

#### 4. Create the tasks table

```sql
CREATE TABLE tasks (
    task_id VARCHAR(26) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    priority VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    creation_date DATETIME NOT NULL
);
```

**Table Details:**
- **task_id**: ULID (unique identifier, 26 chars)
- **title**: Task name (required)
- **description**: Task details (optional)
- **due_date**: When task is due (date only)
- **priority**: Low, Medium, or High
- **status**: Pending, In Progress, or Completed
- **creation_date**: Datetime when the task was created

#### 5. Create a dedicated database user

It's best practice not to use root for your app:

```sql
CREATE USER 'task_user'@'localhost' IDENTIFIED BY 'taskpassword';
GRANT ALL PRIVILEGES ON task_app.* TO 'task_user'@'localhost';
FLUSH PRIVILEGES;
```

Verify the user was created:

```sql
SELECT user FROM mysql.user;
```

Exit MySQL:

```sql
EXIT;
```

## Configuration

The database connection is configured in `app/main.py` with the following default credentials:

- **Host**: localhost
- **User**: task_user
- **Password**: taskpassword
- **Database**: task_app

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

Once the application runs:

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

The `list_tasks` method:
- Displays all tasks in the system
- Shows task ID, title, due date, priority level, and status
- Returns an empty message if no tasks exist
- Tasks are displayed in the order they were created

### Updating a Task

```
Choose an option: 3
-- Update Task --
Task ID: 01ARZ3NDEKTSV4RRFFQ69G5FAV
```

### Marking Task as Done

```
Choose an option: 4
Task ID: 01ARZ3NDEKTSV4RRFFQ69G5FAV
```

### Removing a Task

```
Choose an option: 5
Task ID: 01ARZ3NDEKTSV4RRFFQ69G5FAV
```

## API Overview

### Task Class (`app/task.py`)

Represents a single task with attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| task_id | str | Unique ULID identifier |
| title | str | Task title |
| description | str | Task description |
| due_date | date | Due date |
| priority | str | Priority level (Low, Medium, High) |
| status | str | Status (Pending, In Progress, Completed) |
| creation_date | datetime | Creation timestamp |

### TaskManager Class (`app/task_manager.py`)

Handles business logic and validation:

**Methods:**
- `add_task()` - Create a new task with validation
- `list_tasks()` - Retrieve all tasks
- `list_tasks_filtered()` - Filter tasks by due_date, priority, or status
- `update_task()` - Update task fields
- `mark_task_as_completed()` - Mark task as done
- `remove_task()` - Delete a task

### TaskDB Class (`app/task_db.py`)

Handles database operations:

**Methods:**
- `connect()` - Establish MySQL connection
- `create_task()` - Insert task into database
- `fetch_all_tasks()` - Retrieve all tasks from database
- `update_task()` - Update task in database
- `delete_task()` - Delete task from database
- `close()` - Close database connection

### TaskApp Class (`app/task_app.py`)

Handles user interface and interactions:

**Methods:**
- `run()` - Start the interactive menu loop
- `show_menu()` - Display menu options
- `add_task()` - Handle task creation flow
- `list_tasks()` - Handle task listing flow
- `update_task()` - Handle task update flow
- `mark_completed()` - Handle task completion flow
- `remove_task()` - Handle task deletion flow

## File Descriptions

### `app/main.py`
Application entry point that initializes the database connection and runs the application.

### `app/task.py`
Defines the Task class with ULID generation and task attributes.

### `app/task_manager.py`
Core business logic layer with CRUD operations and validation.

### `app/task_db.py`
Database abstraction layer handling MySQL operations.

### `app/task_app.py`
User interface layer with command-line menu and interactions.

## Troubleshooting

### Database Connection Issues

If you encounter "Error connecting to MySQL":
- Verify MySQL server is running: `sudo systemctl status mysql`
- Check database credentials are correct
- Ensure database `task_app` exists
- Verify user `task_user` has proper permissions

### Date Format Issues

Always use the format `YYYY-MM-DD` (e.g., `2026-02-15`)

### Module Import Errors

Ensure you're running from the `app/` directory:
```bash
cd app
python main.py
```

## Dependencies

- **ulid-py** - For generating ULIDs
- **mysql-connector-python** - For MySQL database connectivity

## Support

For issues or questions, please refer to the project repository or contact the development team.
