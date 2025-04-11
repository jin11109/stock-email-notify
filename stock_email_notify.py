import os
from flask import Flask, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route('/send-email', methods=['GET'])
def send_mail():
    try:
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
        return f'Email sent: {response.status_code}', 20
        
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run()