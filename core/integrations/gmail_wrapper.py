import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class GmailAPI:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
        """Authenticate the user and set up the service."""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('gmail', 'v1', credentials=self.creds)

    def search_emails(self, query):
        """Search emails in the user's inbox based on the query."""
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        return messages

    def send_email(self, to, subject, body, attachments=None):
        """Send an email to a list of recipients with optional attachments."""
        import base64
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders

        message = MIMEMultipart()
        message['to'] = ', '.join(to) if isinstance(to, list) else to
        message['subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        if attachments:
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(attachment, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                message.attach(part)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return self.service.users().messages().send(userId='me', body={'raw': raw}).execute()

# Example usage
if __name__ == "__main__":
    gmail_api = GmailAPI()
    gmail_api.authenticate()

    # Search emails
    emails = gmail_api.search_emails('from:someone@example.com')
    print(emails)

    # Send email
    gmail_api.send_email(to=['recipient@example.com'], subject='Test Subject', body='Test Body', attachments=['/path/to/attachment'])
