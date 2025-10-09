from sqlalchemy.orm import Session
from .interfaces import Tool
from gev_ai.database.config.database_manager import database_manager
from gev_ai.database.models.todo_tasks import Tasks


class ToDoTool(Tool):
    """A simple to-do list tool."""

    @property
    def name(self) -> str:
        return "ToDoTool"

    @property
    def description(self) -> str:
        return "A tool to manage a to-do list. You can add, view, and remove tasks."

    def __init__(self):
        self.todo_list = []
        self.engine = database_manager.engine 

    def add_task(self, task_description: str) -> str:
        try:
            with Session(self.engine) as session:
                new_task = Tasks(task_description=task_description)
                session.add(new_task)
                session.commit()
        except Exception as e:
            print(f"Error adding task: {e}")
            return f"Error adding task: {e}"
        return f'Task "{task_description}" added to your to-do list.'

    def view_tasks(self) -> str:
        try:
            with Session(self.engine) as session:
                tasks_list = session.query(Tasks).all()
                if not tasks_list:
                    return "Your to-do list is empty."
                tasks = "\n".join(
                    f"{task.id}. {task.task_description}" for task in tasks_list
                )
            return f"Your to-do list:\n{tasks}"
        except Exception as e:
            print(f"Error viewing tasks: {e}")
            return "Error retrieving tasks."

    def remove_task(self, task_number: int) -> str:
        try:
            with Session(self.engine) as session:
                task = session.query(Tasks).filter(Tasks.id == task_number).first()
                if task:
                    session.delete(task)
                    session.commit()
                    return f"Task number {task_number} removed from your to-do list."
                else:
                    return "Invalid task number."
        except Exception as e:
            print(f"Error removing task: {e}")
            return f"Error removing task: {e}"
