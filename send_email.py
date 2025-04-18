import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

def send_mail(html_content):
    api_key = os.environ.get('SENDGRID_API_KEY')
    from_email = os.environ.get('FROM_EMAIL')
    to_emails = os.environ.get('TO_EMAILS')

    if not api_key or not from_email or not to_emails:
        raise ValueError("Some required environment variables are missing")

    try:
        message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject='Stock info',
            html_content=html_content)

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f'Email sent: {response.status_code}')

    except Exception as e:
        return f'Email sent error: {str(e)}'

if __name__ == '__main__':
    load_dotenv()
    send_mail('test')