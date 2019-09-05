import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(recipient, amount, donor):
    message = Mail(
        from_email=f'{donor}',
        to_emails=f'{recipient}',
        subject='Someone donated to your image',
        html_content=f'<strong> {donor} Donated {amount} to your image </strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

def follower_email(user, f_username, follower):
    message = Mail(
        from_email=f'{follower}',
        to_emails=f'{user}',
        subject='Someone request to follow your account',
        html_content=f'<strong> {f_username} request to follow you </strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))