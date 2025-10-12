import sys
sys.path.append('.')
import logging

from gev_ai.tools.agent_tools.todo import ToDoTool
from gev_ai.services.logger import GevaiLogger

logger: logging.Logger = GevaiLogger(name=__name__, file="gevai.log").get_logger()

def test_todo_functionality():
    """Test the basic CRUD operations of the ToDoTool"""
    
    logger.info("Testing ToDoTool functionality...")
    
    todo_tool = ToDoTool()
    
    logger.info("\n1. Adding tasks:")
    result1 = todo_tool.add_task("Complete the project")
    logger.info(f"   Result: {result1}")
    
    result2 = todo_tool.add_task("Write documentation")
    logger.info(f"   Result: {result2}")
    
    result3 = todo_tool.add_task("Run tests")
    logger.info(f"   Result: {result3}")
    
    logger.info("\n2. Viewing tasks:")
    tasks = todo_tool.view_tasks()
    logger.info(f"   {tasks}")
    
    logger.info("\n3. Removing task with ID 2:")
    remove_result = todo_tool.remove_task(2)
    logger.info(f"   Result: {remove_result}")
    
    logger.info("\n4. Viewing tasks after removal:")
    tasks_after = todo_tool.view_tasks()
    logger.info(f"   {tasks_after}")
    
    logger.info("\n5. Trying to remove non-existent task (ID 999):")
    invalid_remove = todo_tool.remove_task(999)
    logger.info(f"   Result: {invalid_remove}")

if __name__ == "__main__":
    test_todo_functionality()
