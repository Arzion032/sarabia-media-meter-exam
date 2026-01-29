# task_db.py
import mysql.connector
from mysql.connector import Error
from task import Task

class TaskDB:
    def __init__(self, host="localhost", user="task_user", password="taskpassword", database="task_app"):
        
        # credentials should be stored securely in .env, 
        # but for simplicity, they are hardcoded here
        
        self.conn = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conn.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def create_task(self, task: Task):
        cursor = self.conn.cursor()
        sql = """
        INSERT INTO tasks (task_id, title, description, due_date, priority, status, creation_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (task.task_id, task.title, task.description, task.due_date, task.priority,
                  task.status, task.creation_date)
        cursor.execute(sql, values)
        self.conn.commit()
        cursor.close()

    def fetch_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT task_id, title, description, due_date, priority, status, creation_date FROM tasks")
        rows = cursor.fetchall()
        cursor.close()
        tasks = []
        for row in rows:
            t = Task(row[1], row[2], row[3], row[4], row[5])
            t.task_id = row[0]
            t.creation_date = row[6]
            tasks.append(t)
        return tasks

    def update_task(self, task_id: str, **kwargs):
        if not kwargs:
            return
        fields = []
        values = []
        for k, v in kwargs.items():
            fields.append(f"{k}=%s")
            values.append(v)
        values.append(task_id)
        sql = f"UPDATE tasks SET {', '.join(fields)} WHERE task_id=%s"
        cursor = self.conn.cursor()
        cursor.execute(sql, values)
        self.conn.commit()
        cursor.close()

    def delete_task(self, task_id: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_id=%s", (task_id,))
        self.conn.commit()
        cursor.close()

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
