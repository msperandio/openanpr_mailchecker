import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config_mgr import ConfigMgr


class AlertMailSender:
    def __init__(self, plate: str):
        config = ConfigMgr().config
        self.subject = config['email_for_alerts']['subject'] + ": " + plate
        self.body = config['email_for_alerts']['body']

        # account credentials
        self.sender_email = config['email_for_alerts']['sender_address']
        self.receiver_email = config['email_for_alerts']['receiver_address']
        self.password = config['email_for_alerts']['password']
        self.smtp_add = config['email_for_alerts']['smtp_add']
        self.smtp_port = config['email_for_alerts']['smtp_port']

        # Create a multipart message and set headers
        self.message = MIMEMultipart()
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = self.subject
        self.message["Bcc"] = self.receiver_email  # Recommended for mass emails

        # Add body to email
        self.message.attach(MIMEText(self.body, "plain"))

    def send_alert_mail_with_attachment(self, filename):
        # Open PDF file in binary mode
        print(self.subject)
        print(filename)
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        # Add attachment to message and convert message to string
        self.message.attach(part)
        text = self.message.as_string()
        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_add, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, text)
