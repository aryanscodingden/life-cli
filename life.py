import typer
from datetime import datetime
from Core.storage import *
from Core.storage import Task
from Core.storage import update_keep_note
from google_api.calendar_sync import create_event, delete_event
from google_api.keep_sync import create_keep_note, delete_keep_note
from google_api.auth import get_credentials
from Utils.printer import print_tasks
import os
from google_api.tasks_sync import sync_tasks_two_way
from Utils.sync_helper import auto_sync
from Utils.nlp import parse_input
app = typer.Typer(help="Sync all tasks to Google Calendar and Google Keep.", add_completion=False)

calender_app = typer.Typer(help="Manage your google calender events", add_completion=False)
task_app = typer.Typer(help="Mange your google keep tasks", add_completion=False)

app.add_typer(calender_app, name="calender")
app.add_typer(task_app, name="task")

@calender_app.command("add")
def calender_add(text: str):

    result = parse_input(text)

    if result.get("error"):
        typer.echo("Could not detect date/time for your event.")
        return 
    
    dt = result["datetime"]
    title = result["title"]
    duration = result["duration"]

    temp = type("TempEvent", (), {
        "title": title,
        "note": "",
        "due": dt,
        "duration": duration
    })()
    event_id = create_event(temp)

    typer.echo(f"Calender event created: {title}")

@task_app.command("add")
def task_add(text: str):
    result = parse_input(text)

    if result.get("error"):
        typer.echo("Could not understand the task date/time. Try again.")
        return

    dt = result["datetime"]
    title = result["title"]

    tid = addTask(
        title=title,
        note="",
        due=dt.isoformat(),
        duration=result["duration"],
        keep=False
    )

    typer.echo(f"Added task: {title}")

    auto_sync()

@task_app.command("list")
def task_list():
    """Show all tasks."""
    tasks = get_tasks()
    print_tasks(tasks)

@app.command()
def sync():
    tasks = get_tasks()
    for task in tasks:
        if task.due and not task.calender_event_id:
            event_id = create_event(task)
            update_calender_event(task.id, event_id)

        if task.keep and not task.keep_note_id:
            note_id = create_keep_note(task)
            update_keep_note(task.id, note_id)
        typer.echo("Synced all tasks.")

@app.command()
def sync_tasks():
    """Force Sync tasks with google tasks """
    sync_tasks_two_way()

@app.command("sign-in")
def sign_in():
    """Sign in to Google to authorize calendar access."""
    typer.echo("Starting Google sign-in process...")
    
    if os.path.exists("creds.json"):
        os.remove("creds.json")
        typer.echo("Removed existing credentials.")
    try:
        creds = get_credentials()
        typer.echo("Successfully signed in to Google!")
        typer.echo("You can now use calendar & tasks sync features.")
    except Exception as e:
        typer.echo(f"xSign-in failed: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def add(text:str):
    """Add a task or event using natural lang"""
    result = parse_input(text)

    if not result["datetime"]:
        typer.echo("Could not detect date/time. Please try again.")
        raise typer.Exit(1)
    
    title = result["title"]
    dt = result["datetime"]
    duration = result["duration"]
    is_event = result["is_event"]

    if is_event:
        tid = addTask(title, "", dt.isoformat(), duration, False)
        typer.echo(f"Added event: {title}")
    else:
        tid = addTask(title, "", dt.isoformat(), None, False)
        typer.echo(f"Added task: {title}")

    auto_sync()


if __name__ == "__main__":
    init_db()
    app()
