from task_manager import TaskManager
from datetime import datetime

class TaskApp:
    def __init__(self, db=None):
        self.manager = TaskManager(db=db)
        
    def run(self):
        
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()
            try:
                if choice == "1":
                    self.add_task()
                elif choice == "2":
                    self.list_tasks()
                elif choice == "3":
                    self.update_task()
                elif choice == "4":
                    self.mark_completed()
                elif choice == "5":
                    self.remove_task()
                elif choice.lower() in ("q", "quit", "exit"):
                    print("Exiting... Goodbye!")
                    break
                else:
                    print("Invalid choice. Try again.")
            except Exception as e:
                print(f"Error: {e}")
        
        
    def show_menu(self):
        print("\n=== TASK MANAGER ===")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Mark Task as Done")
        print("5. Remove Task")
        print("Q. Quit")
        
    def add_task(self):
        print("\n--- Add New Task ---")
        title = input("Title: ").strip()
        description = input("Description: ").strip()
        due_date_str = input("Due Date (YYYY-MM-DD): ").strip()
        priority_lvl = input("Priority Level (Low, Medium, High) Default[Medium]: ").strip() or "Medium"
        status = input("Status (Pending, In Progress, Completed) Default[Pending]: ").strip() or "Pending"
        
        # Parse the due date filed
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
        
        task = self.manager.add_task(title, description, due_date, priority_lvl, status)
        print(f"Task '{task.title}' added with ID {task.task_id}")
        

    def list_tasks(self):
        print("\n-- Filter Options --")
        print("1. None")
        print("2. Priority")
        print("3. Status")
        print("4. Due Date")
        choice = input("Choose filter: ").strip()

        by = None
        value = None

        if choice == "2":
            by = "priority"
            value = input("Enter priority [Low/Medium/High]: ").strip().title()
        elif choice == "3":
            by = "status"
            value = input("Enter status [Pending/In Progress/Completed]: ").strip().title()
        elif choice == "4":
            by = "due_date"
            date_str = input("Enter due date (YYYY-MM-DD): ").strip()
            try:
                from datetime import datetime
                value = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Showing all tasks.")
                by = None
                value = None

        tasks = self.manager.list_tasks_filtered(filter_by=by, filter_value=value)
        if not tasks:
            print("No tasks found.")
            return

        print(f"{'ID':<28} {'Title':<20} {'Desc':<30} {'Due Date':<12} {'Priority':<10} {'Status':<12}")
        print("-"*110)
        for t in tasks:
            print(f"{t.task_id:<28} {t.title:<20} {t.description:<30} {t.due_date.strftime('%Y-%m-%d'):<12} {t.priority:<10} {t.status:<12}")
    

    def update_task(self):
        print("\n-- Update Task --")
        task_id = input("Task ID: ").strip()

        # Find the task first before updating
        
        task = None
        for t in self.manager.list_tasks():
            if t.task_id == task_id:
                task = t
                break

        if not task:
            print("Task not found.")
            return
        
        # Display Current Values
        print("\nCurrent Task Details:")

        print(f"{'Title':<20} {'Description':<30} {'Due Date':<12} {'Priority':<10} {'Status':<12}")
        print("-" * 90)

        print(f"{task.title:<20} {task.description:<30} {str(task.due_date):<12} {task.priority:<10} {task.status:<12}")

 
        # Ask user for new values
        print("\nEnter new values (leave blank to keep current):")
        title = input("New Title: ").strip()
        description = input("New Description: ").strip()
        priority = input("New Priority (Low/Medium/High): ").strip()
        status = input("New Status (Pending/In Progress/Completed): ").strip()
        due_date = input("New Due Date (YYYY-MM-DD): ").strip()
        
        # Build a dict for updated fields
        kwargs = {}
        if title: kwargs["title"] = title
        if description: kwargs["description"] = description
        if priority: kwargs["priority"] = priority
        if status: kwargs["status"] = status
        if due_date:
            
            try:
                from datetime import datetime
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                if due_date < datetime.now().date():
                    print("Due date cannot be in the past. Skipping update for due_date.")
                else:
                    kwargs["due_date"] = due_date
            except ValueError:
                print("Invalid date format. Skipping update for due_date.")
                
        # Update the task
        updated_task = self.manager.update_task(task_id, **kwargs)
        print(f"Task '{updated_task.title}' updated successfully.")
        
        
    def mark_completed(self):
        task_id = input("Task ID: ").strip()
        try:
            task = self.manager.mark_task_as_completed(task_id)
            print(f"Task '{task.title}' marked as completed.")
        except ValueError as e:
            print(e)

    def remove_task(self):
        print("\n-- Remove Task --")
        task_id = input("Task ID: ").strip()
        self.manager.remove_task(task_id)
        print(f"Task with ID {task_id} removed.")

