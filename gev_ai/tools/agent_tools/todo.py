from sqlalchemy.orm import Session
from .interfaces import Tool
from gev_ai.database.config.database_manager import database_manager
from gev_ai.database.models.todo_tasks import Tasks
import logging

from services.logger import GevaiLogger

logger: logging.Logger = GevaiLogger(name=__name__, file="gevai.log").get_logger()


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
        logger.info(f"Tool called - Adding task: {task_description}")
        try:
            with Session(self.engine) as session:
                new_task = Tasks(task_description=task_description)
                session.add(new_task)
                session.commit()
        except Exception as e:
            print("Error adding task for more information check gevai.log")
            logger.error(f"Failed to add todo task: {e}")

            return f"Error adding task: {e}"
        return f'Task "{task_description}" added to your to-do list.'

    def view_tasks(self) -> str:
        logger.info("Tool called - Viewing tasks")
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
            print("Error viewing todo list for more information check gevai.log")
            logger.error(f"Failed to view todo list: {e}")
            return "Error retrieving tasks."

    def remove_task(self, task_number: int) -> str:
        logger.info(f"Tool called - Removing task number: {task_number}")
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
            print("Error removing task check gevai.log for more information")
            logger.error(f"Failed to remove todo task: {e}")
            return f"Error removing task: {e}"
