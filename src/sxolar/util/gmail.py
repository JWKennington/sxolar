"""Utilities for sending emails using Gmail.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_SENDER = "chalkdust@sxolar.org"
EMAIL_APP_PASSWORD_ENV_KEY = "SXOLAR_EMAIL_APP_PASSWORD"

try:
    EMAIL_APP_PASSWORD = os.environ[EMAIL_APP_PASSWORD_ENV_KEY]
except KeyError:
    EMAIL_APP_PASSWORD = None


def send_email(
    subject: str,
    to: str,
    body: str,
    safe: bool = True,
    is_plain: bool = True,
):
    """Send an email using Gmail.

    Args:
        subject:
            str, The subject of the email.
        to:
            str, The email address to send the email to.
        body:
            str, The body of the email.
    """
    if EMAIL_APP_PASSWORD is None:
        raise ValueError(
            f"Please set the {EMAIL_APP_PASSWORD_ENV_KEY} environment variable to "
            f"your Gmail app password."
        )

    # Create a multipart message and set headers
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = EMAIL_SENDER
    message["To"] = to

    # Check if the email is plain text or html
    if is_plain:
        part = MIMEText(body, "plain")
        message.attach(part)
    else:
        html_content = f"""\
        <html>
          <body>
            {body}
          </body>
        </html>
        """

        # Turn these into MIMEText objects and attach them to the MIMEMultipart message
        part = MIMEText(html_content, "html")
        message.attach(part)

    # Connect to Gmail's SMTP server and send the email
    try:
        # Gmail SMTP server details
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # TLS port

        # Establish a secure session using starttls
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_APP_PASSWORD)
            server.send_message(message)

    except Exception as e:
        if safe:
            print(f"Error sending email: {e}")
        else:
            raise e
