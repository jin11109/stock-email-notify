import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

api_key = os.environ['SENDGRID_API_KEY']
from_email = os.environ['FROM_EMAIL']
to_emails = os.environ['TO_EMAILS']

message = Mail(
    from_email=from_email,
    to_emails=to_emails,
    subject='test',
    html_content='<strong>with render</strong>')

sg = SendGridAPIClient(api_key)
response = sg.send(message)
print(response.status_code)
print(response.body)
print(response.headers)
