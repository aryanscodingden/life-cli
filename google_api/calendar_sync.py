from turtle import title
from googleapiclient.discovery import build
from Core.storage import get_tasks, update_calender_event
from google_api.auth import get_credentials
from tzlocal import get_localzone_name
from Utils.nlp import parse_input
from Core.storage import save_calendar_event
import typer

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

def calendar_add(text: str):
    result = parse_input(text)

    if result.get("error"):
        typer.echo("❌ Could not detect date/time for your event.")
        return

    dt = result["datetime"]
    title = result["title"]
    duration = result["duration"]

    event_id = create_event(
        type("Event", (), {
            "title": title,
            "note": "",
            "due": dt,
            "duration": duration
        })()
    )


    save_calendar_event(
        title=title,
        note="",
        due=dt.isoformat(),
        duration=duration,
        event_id=event_id
    )

typer.echo(f"📅 Added Calendar Event: {title}")