import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(os.path.dirname(BASE_DIR), "gcal", "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gmail_token.json")

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=8081)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def get_email_body(msg):
    try:
        parts = msg["payload"].get("parts", [])
        if parts:
            data = parts[0]["body"].get("data", "")
        else:
            data = msg["payload"]["body"].get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    except:
        pass
    return ""

def read_latest_emails(max_results=5):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results,
        labelIds=["INBOX"]
    ).execute()
    messages = results.get("messages", [])
    if not messages:
        return "No emails found."
    emails = []
    for msg in messages:
        full_msg = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()
        headers = full_msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        emails.append(f"From: {sender}\nSubject: {subject}")
    return "\n---\n".join(emails)

def read_unread_emails(max_results=5):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results,
        labelIds=["INBOX", "UNREAD"]
    ).execute()
    messages = results.get("messages", [])
    if not messages:
        return "No unread emails."
    emails = []
    for msg in messages:
        full_msg = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()
        headers = full_msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        emails.append(f"From: {sender}\nSubject: {subject}")
    return "\n---\n".join(emails)



import re

def mask_sensitive_data(text):
    # Mask passwords
    text = re.sub(
        r'(password\s*[:\-=]?\s*)(\S+)',
        lambda m: m.group(1) + m.group(2)[0] + '*' * (len(m.group(2)) - 2) + m.group(2)[-1],
        text,
        flags=re.IGNORECASE
    )
    # Mask WiFi passwords
    text = re.sub(
        r'(wifi\s*password\s*[:\-=]?\s*)(\S+)',
        lambda m: m.group(1) + m.group(2)[0] + '*' * (len(m.group(2)) - 2) + m.group(2)[-1],
        text,
        flags=re.IGNORECASE
    )
    # Mask OTPs
    text = re.sub(
        r'(otp\s*[:\-=]?\s*)(\d+)',
        lambda m: m.group(1) + m.group(2)[0] + '*' * (len(m.group(2)) - 2) + m.group(2)[-1],
        text,
        flags=re.IGNORECASE
    )
    return text
def search_emails(query, max_results=20):
    service = get_gmail_service()
    
    # Try multiple search strategies
    search_attempts = [
        query,
        f"from:rishihood.edu.in" if "rishihood" in query.lower() else query,
        query.split()[0] if len(query.split()) > 1 else query,
    ]
    
    messages = []
    used_query = query
    
    for attempt in search_attempts:
        try:
            results = service.users().messages().list(
                userId="me",
                maxResults=max_results,
                q=attempt
            ).execute()
            messages = results.get("messages", [])
            if messages:
                used_query = attempt
                break
        except:
            continue
    
    if not messages:
        return f"No emails found for: {query}"
    
    emails = []
    for msg in messages:
        try:
            full_msg = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="full"
            ).execute()
            headers = full_msg["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
            date = next((h["value"] for h in headers if h["name"] == "Date"), "")
            emails.append(f"From: {sender}\nDate: {date}\nSubject: {subject}")
        except:
            continue
    
    return "\n---\n".join(emails)


def get_email_content(query):
    service = get_gmail_service()
    
    # Build smart search attempts from the query dynamically
    words = query.lower().split()
    search_attempts = [
        query,                                    # exact query
        f"from:{query}",                          # as sender
        f"subject:{query}",                       # as subject
        ' '.join(words[:2]) if len(words) > 2 else query,  # first 2 words
        words[0],                                 # just first word
    ]
    
    # If query looks like a domain or contains .edu .com etc
    for word in words:
        if '.' in word:
            search_attempts.insert(0, f"from:{word}")
    
    messages = []
    for attempt in search_attempts:
        try:
            results = service.users().messages().list(
                userId="me",
                maxResults=10,
                q=attempt
            ).execute()
            messages = results.get("messages", [])
            if messages:
                break
        except:
            continue
    
    if not messages:
        return f"No email found for: {query}"
    
    full_msg = service.users().messages().get(
        userId="me",
        id=messages[0]["id"],
        format="full"
    ).execute()
    
    headers = full_msg["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
    date = next((h["value"] for h in headers if h["name"] == "Date"), "")
    body = get_email_body(full_msg)
    
    if not body.strip():
        body = full_msg.get("snippet", "No content found")
    
    masked_body = mask_sensitive_data(body[:3000])
    
    return f"From: {sender}\nDate: {date}\nSubject: {subject}\n\nContent:\n{masked_body}"