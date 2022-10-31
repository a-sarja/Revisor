import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_scan_result_email(destination_email, vt_scan_local, yara_scan_local, clamav_scan_local):

    subject = "YOUR REVISOR SCAN REPORT IS HERE!!!"

    msg_body = "Welcome to !Revisor\n\n"
    msg_body += "Please refer the attached report files for Revisor Scan details!"
    msg_body += "\n\nThanks,\n Team !Revisor"

    sender_email = "<EMAIL>"
    password = "<APP_PASSWORD>"   # Keep your app password here in case of gmail - not the usual password
    receiver_email = str(destination_email)

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(msg_body, "plain"))

    # Add VirusTotal Scan Report as attachment
    with open(vt_scan_local, "rb") as attachment1:
        # Add file as application/octet-stream
        part1 = MIMEBase("application", "octet-stream")
        part1.set_payload(attachment1.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part1)
    # Add header as key/value pair to attachment part
    part1.add_header(
        "Content-Disposition",
        f"attachment; filename= VT_REPORT.txt",
    )

    # Add YaraAV Scan Report as attachment
    with open(yara_scan_local, "rb") as attachment2:
        # Add file as application/octet-stream
        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(attachment2.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part2)
    # Add header as key/value pair to attachment part
    part2.add_header(
        "Content-Disposition",
        f"attachment; filename= YARA_AV_REPORT.csv",
    )

    # Add ClamAV report as attachment
    with open(clamav_scan_local, "rb") as attachment3:
        # Add file as application/octet-stream
        part3 = MIMEBase("application", "octet-stream")
        part3.set_payload(attachment3.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part3)
    # Add header as key/value pair to attachment part
    part3.add_header(
        "Content-Disposition",
        f"attachment; filename= CLAMAV_AV_REPORT.csv",
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
