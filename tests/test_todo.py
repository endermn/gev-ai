"""Test script for the ToDoTool functionality"""

import sys
sys.path.append('.')

from gev_ai.tools.agent_tools.todo import ToDoTool

def test_todo_functionality():
    """Test the basic CRUD operations of the ToDoTool"""
    
    print("Testing ToDoTool functionality...")
    
    todo_tool = ToDoTool()
    
    print("\n1. Adding tasks:")
    result1 = todo_tool.add_task("Complete the project")
    print(f"   Result: {result1}")
    
    result2 = todo_tool.add_task("Write documentation")
    print(f"   Result: {result2}")
    
    result3 = todo_tool.add_task("Run tests")
    print(f"   Result: {result3}")
    
    print("\n2. Viewing tasks:")
    tasks = todo_tool.view_tasks()
    print(f"   {tasks}")
    
    print("\n3. Removing task with ID 2:")
    remove_result = todo_tool.remove_task(2)
    print(f"   Result: {remove_result}")
    
    print("\n4. Viewing tasks after removal:")
    tasks_after = todo_tool.view_tasks()
    print(f"   {tasks_after}")
    
    print("\n5. Trying to remove non-existent task (ID 999):")
    invalid_remove = todo_tool.remove_task(999)
    print(f"   Result: {invalid_remove}")

if __name__ == "__main__":
    test_todo_functionality()
