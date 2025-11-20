import re
import dateparser
from datetime import datetime, timedelta

TIME_REGEX = r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b"


EVENT_KEYWORDS = [
    "meeting", "call", "appointment", "class", "interview", "event", "flight", "exam", "birthday", "event", "deadline", "doctor"
]

ORDINAL_DATE_REGEX = r"\b(\d{1,2})(st|nd|rd|th)\b"
ON_DATE_REGEX = r"\bon\s+(\d{1,2})(st|nd|rd|th)?\s+(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t|tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b"

TOMORROW_KEYWORDS = {
    "tomorrow",
    "tommorrow",
    "tommrow",
    "toomrow",
    "tomorow",
    "tommorow",
}

def normalize_ordinals(text:str):
    """Converts 20th -> 20 so dataphraser can understand"""
    return re.sub(ORDINAL_DATE_REGEX, lambda m: m.group(1), text)


def extract_on_date(text: str):
    """Extract explicit 'on <date>' patterns (e.g., 'on 20th Nov')."""
    match = re.search(ON_DATE_REGEX, text.lower())
    if not match:
        return None

    day = int(match.group(1))
    month_word = match.group(3)
    current_year = datetime.now().year

    parsed = dateparser.parse(f"{day} {month_word} {current_year}")
    if parsed and parsed < datetime.now():
        parsed = dateparser.parse(f"{day} {month_word} {current_year + 1}")

    return parsed


def remove_datetime_tokens(text: str) -> str:
    """
    Remove obvious date/time tokens to create a clean title.
    """
    t = text
    t = re.sub(r'\b(on|at)\b', ' ', t, flags=re.IGNORECASE)
    t = re.sub(ORDINAL_DATE_REGEX, '', t, flags=re.IGNORECASE)
    t = re.sub(TIME_REGEX, '', t, flags=re.IGNORECASE)
    for w in ["today", "tomorrow", "tonight", "this", "next", "morning", "evening", "afternoon", "pm", "am"]:
        t = re.sub(r'\b' + re.escape(w) + r'\b', ' ', t, flags=re.IGNORECASE)

    months = ["january","february","march","april","may","june","july","august","september","october","november","december",
              "jan","feb","mar","apr","jun","jul","aug","sep","sept","oct","nov","dec"]
    for m in months:
        t = re.sub(r'\b' + re.escape(m) + r'\b', ' ', t, flags=re.IGNORECASE)

    t = re.sub(r'\s+', ' ', t).strip()
    return t

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
    text = normalize_ordinals(text)
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


    if dt is None or (dt.date() == datetime.now().date() and "on" in text_lower):
        explicit_date = extract_on_date(text)
        if explicit_date:
            if extracted_time:
                hour, minute = extracted_time
                dt = explicit_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            else:
                dt = explicit_date.replace(hour=9, minute=0, second=0, microsecond=0)
    if any(word in text_lower for word in TOMORROW_KEYWORDS):
        if dt is None:
            tomorrow = datetime.now() + timedelta(days=1)
            dt = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        elif dt.date() == datetime.now().date():
            dt = dt + timedelta(days=1)

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