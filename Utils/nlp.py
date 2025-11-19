import re
import dateparser
from datetime import datetime, timedelta

TIME_REGEX = r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b"


EVENT_KEYWORDS = [
    "meeting", "call", "appointment", "class", "interview", "event", "flight", "exam", "birthday", "event", "deadline", "doctor"
]

TOMORROW_KEYWORDS = {
    "tomorrow",
    "tommorrow",
    "tommrow",
    "toomrow",
    "tomorow",
    "tommorow",
}

def extract_time(text:str):
    """Extract time"""
    match = re.search(TIME_REGEX, text.lower())
    if not match:
        return None
    
    hour = int(match.group(1))
    minute = int(match.group(2)) if match.group(2) else 0
    ampm = match.group(3)

    if ampm == "pm" and hour !=12:
        hour += 12
    if ampm == "am" and hour == 12:
        hour = 0

    return hour, minute

def parse_input(text: str):
    """Parses with natural lang"""
    text_lower = text.lower()
    is_event = any(word in text_lower for word in EVENT_KEYWORDS)
    dt = dateparser.parse(text, settings={
        "PREFER_DATES_FROM": "future",
        "RELATIVE_BASE": datetime.now(),
        "RETURN_AS_TIMEZONE_AWARE": False,
    })
    extracted_time = extract_time(text)

    if dt is None and extracted_time:
        hour, minute = extracted_time
        today = datetime.now()
        dt = today.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if dt is None and any(word in text_lower for word in TOMORROW_KEYWORDS):
        tomorrow = datetime.now() + timedelta(days=1)
        if extracted_time:
            hour, minute = extracted_time
            dt = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
        else:
            dt = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)

    if dt is None:
        return {"error": True}
    
    is_event = any(k in text_lower for k in EVENT_KEYWORDS)

    duration = None
    if "hour" in text_lower:
        words = text_lower.split()
        for i, w in enumerate(words):
            if w.isdigit() and (i+1 < len(words) and "hour" in words[i+1]):
                duration = int(w)
                break

    

    title = text.strip()

    return {
        "is_event": is_event,
        "datetime": dt,
        "title": title, 
        "duration": duration
    }