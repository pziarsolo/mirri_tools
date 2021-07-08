import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(receivers, fname):
    subject = "New file uploaded with validator"
    body = f"A new file has been uploaded using the validator file: {fname}"
    sender_email = "pziarsolo@cect.org"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email

    message["To"] = ", ".join(receivers)
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body))
    text = message.as_string()

    # Log in to server using secure context and send email
    server = smtplib.SMTP("localhost")
    # server.login(sender_email, password)
    server.sendmail(sender_email, receivers, text)
    server.close()

