from calendar import calendar
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

calender_app = typer.Typer()
task_app = typer.Typer()

app.add_typer(calender_app, name="calender")
app.add_typer(task_app, name="task")

@calendar.command("add")
def calender_add(name:str, date: str, time:str):
    """
    Create a calender event.
    Format: calendar <name> <DD:MM:YY> <HH:MM>
    """
    try:
        day, month, year = date.split(":")
        hour, minute = time.split(":")
        dt = datetime (
            year = int(year),
            month = int(month),
            day = int(day),
            hour = int(hour),
            minute=int(minute)
        )
    except:
        typer.echo("Invalid date/time format. Use DD:MM:YY HH:MM Format")

    tid = addTask(name, "", dt.isoformat(), None, False)
    event_id = create_event(get_tasks(tid))
    update_calender_event(tid, event_id)

    typer.echo(f"Calender event created: {name}")

@task_app.command("add")
def task_add(name: str, date: str):
    """
    Create a TO-DO list 
    Format: task add "Task Name" DD:MM
    """
    try:
        day, month = date.split(":")
        dt = datetime(datetime.now().year, int(month), int(day))
    except:
        typer.echo("Invalid date format")
        return
    tid = addTask(name, "", dt.isoformat(), None, False)
    typer.echo(f"Task added: {name}")

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
