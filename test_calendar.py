from gcal.google_cal import get_upcoming_events, create_event

# Test reading events
print("Upcoming events:")
print(get_upcoming_events())

# Test creating an event
print("\nCreating test event...")
result = create_event(
    summary="VANTAGE Test Meeting",
    date_str="2026-04-01",
    time_str="15:00",
    duration_hours=1
)
print(result)