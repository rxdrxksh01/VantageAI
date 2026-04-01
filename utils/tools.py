from langchain.tools import tool
from gcal.google_cal import get_upcoming_events, create_event
from gmail.gmail_reader import read_latest_emails, read_unread_emails, search_emails, get_email_content
from memory.store import recall_memory, save_memory

@tool
def calendar_get_events() -> str:
    """Get upcoming Google Calendar events for the user. Use when user asks about schedule, events, or what's happening."""
    return get_upcoming_events()

@tool
def calendar_create_event(title: str, date: str, time: str) -> str:
    """Create a new Google Calendar event. Use when user wants to schedule or add something.
    date format: YYYY-MM-DD
    time format: HH:MM
    """
    return create_event(title, date, time)

@tool
def gmail_read_latest() -> str:
    """Read the latest emails from Gmail inbox. Use when user asks to read, check or see emails."""
    return read_latest_emails()

@tool
def gmail_read_unread() -> str:
    """Read unread emails from Gmail. Use when user asks about unread or new emails."""
    return read_unread_emails()

@tool
def gmail_search(query: str) -> str:
    """Search emails by any keyword, sender name, domain, or topic.
    query: any relevant search term from what the user described
    """
    return search_emails(query)

@tool
def gmail_get_content(query: str) -> str:
    """Get the full content of a specific email.
    Use the most specific keyword from what the user described as the query.
    query: most specific identifying word or phrase from user's description
    """
    return get_email_content(query)



@tool
def memory_search(query: str) -> str:
    """Search past conversation memories. Use when user asks about something previously discussed.
    query: what to search for in memory
    """
    return recall_memory(query)