from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

def authenticate_gmail():
    # Load OAuth 2.0 credentials
    creds = Credentials.from_authorized_user_file('credentials.json')

    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)

    return service

def send_email(subject, body, to_email):
    # Authenticate with Gmail API
    gmail_service = authenticate_gmail()

    # Create message
    message = create_message("crimereports.itms448project@gmail.com", to_email, subject, body)

    # Send message
    send_message(gmail_service, "crimereports.itms448project@gmail.com", message)

def create_message(sender, to, subject, message_text):
    message = {"raw": None}

    message["raw"] = base64.urlsafe_b64encode(
        f"From: {sender}\nTo: {to}\nSubject: {subject}\n\n{message_text}".encode("utf-8")
    ).decode("utf-8")

    return message

def send_message(service, user_id, message):
    try:
        message = (
            service.users()
            .messages()
            .send(userId=user_id, body=message)
            .execute()
        )
        print("Message Id: %s" % message["id"])
        return message
    except Exception as e:
        print("An error occurred: %s" % e)
        return None
