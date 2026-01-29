from task import Task
from datetime import datetime
class TaskManager:
    
    def __init__(self, db=None):
        self.tasks = []
        self.db = db
        
        # Load tasks from DB at start of the app
        if self.db:
            self.tasks = self.db.fetch_all_tasks()
        
    def add_task(self, title, description, due_date, priority_lvl:str = "Medium", status: str = "Pending"):
        
        priority_options = ["Low", "Medium", "High"]
        status_options = ["Pending", "In Progress", "Completed"]
        
        priority_lvl = priority_lvl.strip().title()
        status = status.strip().title()
        
        # Validation of required fields
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if not description.strip():
            raise ValueError("Description cannot be empty.")
        if due_date is None:
            raise ValueError("Due date must be provided.")
        
        # Additional validation
        if status not in status_options:
            raise ValueError(f"Status must be one of {status_options}.")
        if priority_lvl not in priority_options:
            raise ValueError(f"Priority level must be one of {priority_options}.")
        if due_date < datetime.now().date():
            raise ValueError("Due date cannot be in the past.")
        
        task = Task(title, description, due_date, priority_lvl, status)
        print("inside task manager add task")
        self.tasks.append(task)
        
        if self.db:
            self.db.create_task(task)
            
        return task
        
        
    def list_tasks(self):
        return self.tasks
    
    def update_task(self, task_id: str, **kwargs):
        for task in self.tasks:
            if task.task_id == task_id:
                for k, v in kwargs.items():
                    if hasattr(task, k):
                        setattr(task, k, v)
                if self.db:
                    self.db.update_task(task_id, **kwargs)
                return task
        raise ValueError("Task not found")
        
    def mark_task_as_completed(self, task_id: str):
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_as_done()
                return self.update_task(task_id, status="Completed")
        raise ValueError("Task not found.")
    
    def remove_task(self, task_id: str):
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        if self.db:
            self.db.delete_task(task_id)