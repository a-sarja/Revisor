import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_scan_result_email(destination_email, pdf_report, vt_report, yara_report):

    subject = "YOUR REVISOR SCAN REPORT IS HERE!!!"

    msg_body = "Welcome to !Revisor\n\n"
    msg_body += "Please refer the attached report files for Revisor Scan details!"
    msg_body += "\n\nThanks,\n Team !Revisor"

    sender_email = os.environ.get("REVISOR_EMAIL")
    password = os.environ.get("REVISOR_EMAIL_PASSWORD")
    if not sender_email or not password:
        print('ENV variables are empty. Unable to send reports via email')
        return

    receiver_email = str(destination_email)

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(msg_body, "plain"))

    # Add Revisor Scan Report as attachment
    with open(pdf_report, "rb") as attachment1:
        # Add file as application/octet-stream
        part1 = MIMEBase("application", "octet-stream")
        part1.set_payload(attachment1.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part1)
    # Add header as key/value pair to attachment part
    part1.add_header(
        "Content-Disposition",
        f"attachment; filename=REVISOR_SCAN_REPORT.pdf",
    )

    # Add VirusTotal Scan Report as attachment
    with open(vt_report, "rb") as attachment2:
        # Add file as application/octet-stream
        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(attachment2.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part2)
    # Add header as key/value pair to attachment part
    part2.add_header(
        "Content-Disposition",
        f"attachment; filename= VT_REPORT.csv",
    )

    # Add YaraAV Scan Report as attachment
    with open(yara_report, "rb") as attachment3:
        # Add file as application/octet-stream
        part3 = MIMEBase("application", "octet-stream")
        part3.set_payload(attachment3.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part3)
    # Add header as key/value pair to attachment part
    part3.add_header(
        "Content-Disposition",
        f"attachment; filename= YARA_report.json",
    )

    # Add attachments to message and convert message to string
    message.attach(part1)
    message.attach(part2)
    message.attach(part3)

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
