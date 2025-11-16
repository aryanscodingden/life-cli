import gkeepapi

def login():
    keep = gkeepapi.Keep()
    email = input("Google Email:")
    app_pw = input("App Password(Google App Password): ")
    keep.login(email, app_pw)
    return keep

def create_keep_note(task):
    keep = login()
    note = keep.createnote(task.title, task.note)
    keep.sync()
    return note.id

def delete_keep_note(note_id):
    keep = login()
    note = keep.get(note_id)
    keep.delete(note)
    keep.sync()

