# Life-CLI
A Powerful natural-language CLI that is `Made for developers` in mind to `Increase productivity while working`, you can manage google calender events, & `add, edit, delete in google tasks using natural language`! Keeps your day organized, all `Without leaving your terminal`
This project was made for `'midnight.hackclub.com'`
<br>
<br>
![gif](https://github.com/aryanscodingden/life-cli/blob/main/Assets/Calender%20Add.gif)

## Life CLI understands human language:
`life task add "buy milk tomorrow morning`
<br>
`life calendar add "meeting with john at 5pm on 20th nov`
<br>
`life calender add "doctor appointment next monday 9am`
<br>

### Time spent: 8h 37m
## Can sync to:
Google Tasks for tasks
<br>
Google Calender for events
<br>
# Features that make it amazing to use!
- Fast & Developer-Friendly
- Built on Typer → instant CLI
- Easy to extend or modify
- Lightweight — no heavy dependencies

# Commands to help you out!
`py life.py --help (Helps you see all the comands)`
<br>
`py life.py calender add "event"`
<br>
`py life.py task add "task"`
<br>

# Clone the repo 
`git clone https://github.com/aryanscodingden/life-cli`
<br>
`cd life-cli`
<br>
`pip install -r req.txt`
<br>

# ❗Important❗
## To make sure this CLI works, you must do the following steps:
 - Go to Google Cloud Console:
 - 'https://console.cloud.google.com'
 - Click Select Project → New Project
 - Name it anything (example: LifeCLI)
 - Click Create
 - In the left sidebar, click APIs & Services → Library
 - Search for each of the following and click Enable:
 - Google Calendar API
 - Google Tasks API
 - Go to APIs & Services → Credentials
 - Click Create Credentials
 - Select: Desktop Application
 - You will see Download JSON – click it.
 - This file is your 'credentials.json'

## If you are facing a scope issue:
 Go to API & Services → OAuth Consent Screen
 Choose Internal
 Scopes page → Add + the following scopes:
`'https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/tasks'`

# Sucessfully setup! Now run 'py life.py sign-in & then py life.py --help for help!

# Support 
## You can mail me at aryanscode@gmail.com, or raise a issue and i'll fix it!