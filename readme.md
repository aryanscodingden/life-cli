# Life-CLI
## A Powerful natural-language CLI that is made for developers in mind to increase productivity while working, you can manage google calender events, & add, edit, delete in google tasks using natural language! Keeps your day organized, all without leaving your terminal
### This project was made for 'midnight.hackclub.com'
## Life CLI understands human language:
'
'life task add "buy milk tomorrow morning"'
'life calendar add "meeting with john at 5pm on 20th nov"'
'life calender add "doctor appointment next monday 9am"'
'
### Time spent: 8h 37m
## Can sync to:
### Google Tasks for tasks
### Google Calender for events

# Features that make it amazing to use!
## Fast & Developer-Friendly
## Built on Typer → instant CLI
## Easy to extend or modify
## Lightweight — no heavy dependencies

# Commands to help you out!
## py life.py --help (Helps you see all the comands)
## py life.py calender add "event"
## py life.py task add "task"

# Clone the repo 
## git clone https://github.com/aryanscodingden/life-cli
## cd life-cli
## pip install -r req.txt

# ❗Important❗
## To make sure this CLI works, you must do the following steps:
### - Go to Google Cloud Console:
### - 'https://console.cloud.google.com'
### - Click Select Project → New Project
### - Name it anything (example: LifeCLI)
### - Click Create
### - In the left sidebar, click APIs & Services → Library
### - Search for each of the following and click Enable:
### - Google Calendar API
### - Google Tasks API
### - Go to APIs & Services → Credentials
### - Click Create Credentials
### - Select: Desktop Application
### - You will see Download JSON – click it.
### - This file is your 'credentials.json'

## If you are facing a scope issue:
### Go to API & Services → OAuth Consent Screen
### Choose Internal
### Scopes page → Add + the following scopes:
### 'https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/tasks'

# Sucessfully setup! Now run 'py life.py sign-in & then py life.py --help for help!

# Support 
## You can mail me at aryanscode@gmail.com, or raise a issue and i'll fix it!
