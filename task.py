from datetime import datetime
import ulid


class Task:
    
    def __init__(self, title: str, description : str, due_date, priority_lvl:str, status: str):
        self.task_id = str(ulid.new())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority_lvl
        self.status = status
        self.creation_date = datetime.now()
    
    
    def mark_as_done(self):
        self.status = "Completed"
