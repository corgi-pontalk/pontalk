---
Categories: Automation
Tags: gmail, automation
slug: "python-email-auto-sort"
date: 2025-09-08
status: "publish"
---

# How to Automatically Sort Emails with Python
## Introduction

Is your inbox overflowing with unread messages? Manually sorting emails into folders can be time-consuming and stressful. With a small Python script, you can automate this process and let your computer do the boring work. In this article, we’ll build a simple script that labels Gmail messages automatically.

## Requirements

- Python 3
- A Gmail account
- Gmail API access
- Libraries: `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`

Install the libraries:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Step 1: Enable the Gmail API

1. Open Google Cloud Console and create a project.  
2. Enable **Gmail API** for that project.  
3. Create **OAuth 2.0 Client ID (Desktop app)** credentials.  
4. Download `credentials.json` and place it in your project folder.

## Step 2: Authenticate and Connect

```python
from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)
```

## Step 3: Create or Find Labels

We’ll need a label ID to apply to messages. The function below finds a label by name (e.g., `GitHub`) or creates it if it doesn’t exist.

```python
def get_or_create_label_id(service, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for lb in labels:
        if lb['name'].lower() == label_name.lower():
            return lb['id']
    body = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }
    created = service.users().labels().create(userId='me', body=body).execute()
    return created['id']
```

## Step 4: Sort Incoming Emails

Example: apply the `GitHub` label to all messages from `notifications@github.com`.

```python
def sort_emails(service):
    label_id = get_or_create_label_id(service, 'GitHub')
    results = service.users().messages().list(
        userId='me', q="from:notifications@github.com", maxResults=50
    ).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No GitHub emails found.")
        return

    for msg in messages:
        msg_id = msg['id']
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'addLabelIds': [label_id]}
        ).execute()
        print(f"Labeled message: {msg_id}")
```

## Step 5: Run the Script

```python
if __name__ == "__main__":
    svc = get_service()
    sort_emails(svc)
```

## Conclusion

With the Gmail API and Python, you can take control of your inbox and eliminate repetitive sorting. Extend this idea by labeling newsletters, creating daily digests, or even auto-responding to specific senders.

> Full source code and updates: (GitHub link to be added)

