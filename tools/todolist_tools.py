import json
from typing import Optional
from todoist_api_python.api import TodoistAPI
from config.config import TODOIST_API_KEY
from langchain_core.tools import tool

api = TodoistAPI(TODOIST_API_KEY)


@tool
def add_task(task: str) -> str:
    """Add a new task to Todoist and return task details (id, project, content)."""
    try:
        new_task = api.add_task(content=task)
        result = {
            "status": "added",
            "task": new_task.content,
            "id": new_task.id,
            "project_id": new_task.project_id,
        }
    except Exception as e:
        result = {"status": "error", "error": str(e)}

    return json.dumps(result, ensure_ascii=False)


@tool
def get_task(project_id: Optional[str] = None) -> str:
    """
    Fetch all tasks from Todoist. Optional: filter by project_id.
    Returns list of tasks with details.
    """
    readable_task: list[dict[str, Optional[str]]] = []
    try:
        task_list = api.get_tasks(project_id=project_id)

        # Flatten if nested list
        flat_tasks = []
        for t in task_list:
            if isinstance(t, list):
                flat_tasks.extend(t)
            else:
                flat_tasks.append(t)

        for task in flat_tasks:
            # --- Debug safe print ---
            print("TASK TYPE:", type(task))
            print("RAW:", task if isinstance(task, (dict, list)) else task.__dict__)

            # Handle due safely
            due_string = "No due date"
            if hasattr(task, "due") and task.due:
                if hasattr(task.due, "date"):
                    due_string = f"Due: {task.due.date}"
                elif isinstance(task.due, dict) and "date" in task.due:
                    due_string = f"Due: {task.due['date']}"
                elif isinstance(task.due, list):
                    due_string = f"Due: {', '.join(map(str, task.due))}"

            # Priority mapping
            priority_map = {
                1: "Priority 4 (Lowest)",
                2: "Priority 3",
                3: "Priority 2",
                4: "Priority 1 (Highest)"
            }
            priority_level = getattr(task, "priority", None)
            priority_level = priority_map.get(priority_level, "Normal")

            readable_task.append({
                "Task": getattr(task, "content", str(task)),
                "Due": due_string,
                "Priority": priority_level,
                "Project": getattr(task, "project_id", "Unknown"),
                "Labels": getattr(task, "labels", []),
            })

        result = {"status": "ok", "tasks": readable_task}

    except Exception as e:
        result = {"status": "error", "error": str(e)}

    return json.dumps(result, ensure_ascii=False)