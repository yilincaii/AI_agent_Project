import json
from typing import Optional
from todolist_api_python.api import TodoListAPI
from config.config import TODOLIST_API_KEY

api = TodoListAPI(TODOLIST_API_KEY)

def add_task(task:str)->str:
    try:
        new_task = api.add_task(content = task)
        results = {
            "status": "added",
            "task" : new_task.content,
            "id" : new_task.id,
            "project_id" : new_task.project_id,

        }
    except Exception as e:
        result = {"status": "error", "error": str(e)}
    return json.dumps(result,ensure_ascii=False)
def get_tasks()->str:
    readable__task = list(dict[str,Optional[str]]) = []
    try:
        task_api = api.get_tasks()
        for task in task_list:
            due_string = f"Due {task.due_date}" if task.due else "No due date"

            priority_map = {
                1:"Priority 4 (loswest)",
                2:"Priority 3",
                3:"Priority 2",
                4:"Priority 1(highest)",

            }
            priority_level = priority_map.get(task.priority,"normal")

            readable__task.append({
                "Task" : task.content,
                "Due" : due_string,
                "Priority" : priority_level,
                "Project" : getattr(task,"project_id","Unknown"),
                "Labels" : getattr(task,"label"),

            })
            result = {"status": "ok", "tasks": readable__task}
    except Exception as e:
        result = {"status": "error", "error": str(e)}


    return json.dumps(result,ensure_ascii=False)