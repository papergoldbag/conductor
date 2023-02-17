import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from conductor.core.misc import settings


def send_mail(to_email: str, subject: str, text: str):
    return

    toaddr = to_email

    msg = MIMEMultipart()
    msg['From'] = settings.mailru_login
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = text
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL(settings.mailru_server, settings.mailru_port)
    server.login(settings.mailru_login, settings.mailru_password)
    # server.sendmail(settings.mailru_login, toaddr, msg.as_string())
    # server.quit()
