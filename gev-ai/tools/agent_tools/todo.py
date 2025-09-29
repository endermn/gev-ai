from .interfaces import Tool


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

	def add_task(self, task: str) -> str:
		self.todo_list.append(task)
		return f'Task "{task}" added to your to-do list.'

	def view_tasks(self) -> str:
		if not self.todo_list:
			return "Your to-do list is empty."
		tasks = "\n".join(
			f"{idx + 1}. {task}" for idx, task in enumerate(self.todo_list)
		)
		return f"Your to-do list:\n{tasks}"

	def remove_task(self, task_number: int) -> str:
		if 0 < task_number <= len(self.todo_list):
			removed_task = self.todo_list.pop(task_number - 1)
			return f'Task "{removed_task}" removed from your to-do list.'
		else:
			return "Invalid task number."
