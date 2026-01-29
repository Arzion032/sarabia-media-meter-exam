# main.py
from task_app import TaskApp
from task_db import TaskDB
def main():
    db = TaskDB(user="task_user", password="taskpassword", database="task_app")
    ui = TaskApp(db=db)
    ui.run()
    db.close()

if __name__ == "__main__":
    main()