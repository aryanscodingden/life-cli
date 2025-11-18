from googleapiclient.discovery import build
from google_api.auth import get_credentials
from Core.storage import get_tasks, update_calender_event, update_keep_note, mark_done, addTask, update_google_task_id
from datetime import datetime

def get_service():
    creds = get_credentials()
    return build("tasks", "v1", credentials=creds)

def pull_google_tasks():
    """Fetch all google tasks"""
    service = get_service()
    result = service.tasks().list(tasklist='@default').execute()
    return result.get("items", [])

def push_local_task_to_google(task):
    """Create google task."""
    service = get_service()

    body = {
        "title": task.title,
        "notes": task.note if task.note else "",
    }

    if task.due:
        body['due'] = task.due.isoformat() + "Z"

    created = service.tasks().insert(tasklist="@default", body=body).execute()
    return created["id"]

def delete_google_task(gtask_id):
    service = get_service()
    service.tasks().delete(tasklist="@default", task=gtask_id).execute()

def sync_tasks_two_way():
    """Full two-way sync"""
    
    print("Starting Google tasks sync")

    local_tasks = get_tasks()
    google_tasks = pull_google_tasks()

    gmap = {t["id"]: t for t in google_tasks}

    for task in local_tasks:
        if not task.google_task_id:
            gid = push_local_task_to_google(task)
            update_google_task_id(task.id, gid)
            print(f"Created on google tasks {task.title}")
        else:
            gtask = gmap.get(task.google_task_id)
            if gtask:
                changed = (
                    gtask.get("title") != task.title or 
                    gtask.get("notes", "") != (task.note or "")
                )
                if changed:
                    update_google_task_id(task, task.google_task_id)
                    print(f"Updated on Google: {task.title}")

    local_gids = {t.google_task_id for t in local_tasks if t.google_task_id}

    for g in google_tasks:
        gid = g["id"]

        if gid not in local_gids:
            title = g.get("title", "Untitled Task")
            notes = g.get("notes", "")

            due = g.get("due")
            if due:
                due_dt = datetime.fromisoformat(due.replace("Z", ""))
            else:
                due_dt = None

            new_id = addTask(
                title,
                notes,
                due_dt.isoformat() if due_dt else None
            )
            update_google_task_id(new_id, gid)

            print(f'Pulled from google: {title}')
        
        if g.get("status") == "completed":
            for lt in local_tasks:
                if lt.google_task_id == gid:
                    mark_done(lt.id)
                    print(f"Completed in google, removed locally as well: {lt.title}")

    print("Google Tasks two-way sync complete.")

