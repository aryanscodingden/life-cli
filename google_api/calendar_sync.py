from googleapiclient.discovery import build
from google_api.auth import get_credentials


def create_event(task):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": task.title,
        "description": task.note,
        "start": {"dateTime": task.due.isoformat(),
                  "timeZone": "Asia/Kolkata"
                  },
        "end": {"dateTime": (task.due).isoformat(),
                "timeZone":"Asia/Kolkata"
                },
    }

    result = service.events().insert(calendarId="primary", body=event).execute()
    return result["id"]

def delete_event(event_id):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    service.events().delete(calendarId="primary", eventId=event_id).execute()

