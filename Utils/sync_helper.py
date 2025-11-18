from google_api.calendar_sync import create_event
from google_api.tasks_sync import sync_tasks_two_way
from Core.storage import get_tasks, update_calender_event 

def auto_sync():
    print("Auto-Sync Started")
    sync_tasks_two_way() #Fetches tasks from google tasks aswell

    for task in get_tasks():
        if task.due and not task.calender_event_id:
            event_id = create_event(task)
            update_calender_event(task.id, event_id)
print("Auto-Sync Complete")



