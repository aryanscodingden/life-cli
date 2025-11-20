from googleapiclient.discovery import build
from Core.storage import get_tasks, update_calender_event
from google_api.auth import get_credentials
import tzlocal
import pytz
from datetime import datetime



def create_event(task):
    """
    Create Google Calendar event.
    """
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    tz = str(tzlocal.get_localzone())
    start_dt = task.due.isoformat()
    end_dt = task.due.isoformat()

    event = {
        "summary": task.title,
        "description": task.note,
        "start": {
            "dateTime": start_dt,
            "timeZone": tz,
        },
        "end": {
            "dateTime": end_dt,
            "timeZone": tz,
        },
    }

    result = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return result["id"]


def delete_event(event_id):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    service.events().delete(calendarId="primary", eventId=event_id).execute()


def calendar_sync():
    """
    Sync ONLY calendar events (is_event = True)
    """
    tasks = get_tasks()

    for t in tasks:
        if not t.is_event:
            continue

        if t.due and not t.calender_event_id:
            event_id = create_event(t)
            update_calender_event(t.id, event_id)




def calendar_auto_sync():
    calendar_sync()
