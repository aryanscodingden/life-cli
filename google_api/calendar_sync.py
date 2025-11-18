from googleapiclient.discovery import build
from google_api.auth import get_credentials
from tzlocal import get_localzone_name


def create_event(task):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    local_tz = get_localzone_name()

    event = {
        "summary": task.title,
        "description": task.note,
        "start": {"dateTime": task.due.isoformat(),
                  "timeZone": local_tz,
                  },
        "end": {"dateTime": (task.due).isoformat(),
                "timeZone": local_tz,
                },
    }

    result = service.events().insert(calendarId="primary", body=event).execute()
    return result["id"]

def delete_event(event_id):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    service.events().delete(calendarId="primary", eventId=event_id).execute()



