import typer
from Core.storage import *
from Core.storage import Task
from Core.storage import update_keep_note
from google_api.calendar_sync import create_event, delete_event
from google_api.keep_sync import create_keep_note, delete_keep_note
from google_api.auth import get_credentials
from Utils.printer import print_tasks
import os

app = typer.Typer()

@app.command()
def add(title: str, note: str = "", due: str = None, duration: int=None, keep:bool = False):
    tid = addTask(title, note, due, duration, keep)
    typer.echo(f"Added Task #{tid}")

@app.command()
def show():
    tasks = get_tasks()
    print_tasks(tasks)

@app.command()
def done(task_id: int):
    tasks = get_tasks()
    task = next((t for t in tasks if t.id == task_id), None)

    if not task:
        typer.echo("Task Not Found")
        raise typer.Exit()

    if task.calendar_event_id:
        delete_event(task.calendar_event_id)

    if task.keep_note_id:
        delete_keep_note(task.keep_note_id)

    mark_done(task_id)
    typer.echo(f"Completed task #{task_id}")

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
        typer.echo("You can now use calendar sync features.")
    except Exception as e:
        typer.echo(f"xSign-in failed: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    init_db()
    app()
