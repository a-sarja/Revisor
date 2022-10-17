import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import file_utils


def send_scan_result_email(destination_email, summary_filepath, csv_filepath):

    subject = "YOUR REVISOR SCAN REPORT IS HERE!!!"
    msg_body = "Welcome to Revisor Scan report!\n\n"
    summary = file_utils.read_file(filepath=summary_filepath)
    if summary:
        msg_body += "SUMMARY - \n\n"
        msg_body += summary.decode().strip()
        msg_body += "\n\n"

    msg_body += "For detailed report, please refer the attached report files."
    # detailed_report = file_utils.read_file(filepath=csv_filepath)
    # if detailed_report:
    #     msg_body += "DETAILS - \n\n"
    #     msg_body += detailed_report.decode().strip()
    #     msg_body += "\n\n"
    msg_body += "\n\nThanks,\n Team !Revisor"

    sender_email = "<EMAIL>"
    password = "<PASSWORD>"   # Keep your app password here in case of gmail - not the usual password
    receiver_email = str(destination_email)

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(msg_body, "plain"))

    # Add summary file as attachment
    with open(summary_filepath, "rb") as attachment:
        # Add file as application/octet-stream
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= SUMMARY_REPORT.txt",
    )

    # Add csv file as attachment
    with open(csv_filepath, "rb") as attachment2:
        # Add file as application/octet-stream
        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(attachment2.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part2)

    # Add header as key/value pair to attachment part
    part2.add_header(
        "Content-Disposition",
        f"attachment; filename= DETAILED_REPORT.csv",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    message.attach(part2)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
