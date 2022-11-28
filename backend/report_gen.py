import json
import traceback
from reportlab.pdfgen import canvas


def generate_pdf_report(file_name, file_hash, uploaded_by, uploaded_timestamp, vt_report, clamav_report):

    try:
        report_fileName = file_name + '_revisor_report.pdf'  # this will be the name of the report
        title = 'REVISOR REPORT'
        intro1 = 'REVISOR a malicious file analyzer. Its a student project.'
        intro2 = 'We check for file maliciousness using virus total AV engines.'
        intro3 = "We also use ClamAV to analyze the file locally."
        intro4 = 'Crowd-sourced yara rules are also used to find keywords and more'
        intro5 = 'references for the file.'
        intro6 = 'Read more about it here - https://github.com/a-sarja/Revisor'

        pdf = canvas.Canvas(report_fileName)

        with open(vt_report, "r") as vt_fp:
            vt_summary = vt_fp.read()

        clam_detection = 0
        clam_viruses = None
        with open(clamav_report, "r") as clam_fp:
            clam_dict = json.loads(clam_fp.read())
            if clam_dict['data']['result'][0]['is_infected'] == 1:
                clam_detection = 1
                clam_viruses = clam_dict['data']['result'][0]['viruses']

        pdf.setFont("Courier-Bold", 24)
        pdf.drawCentredString(300, 770, title)

        # drawing a line
        pdf.line(30, 760, 550, 760)

        text = pdf.beginText(40, 740)
        text.setFont("Courier", 12)
        text.textLine(intro1)
        text.textLine(intro2)
        text.textLine(intro3)
        text.textLine(intro4)
        text.textLine(intro5)

        text.textLine(" ")
        text.textLine(intro6)

        text.setFont("Courier", 12)
        pdf.drawText(text)

        text = pdf.beginText(40, 630)
        text.setFont("Courier-Bold", 18)
        text.textLine("File summary")
        text.setFont("Courier", 12)
        # text.textLine("File details go here")
        text.textLine("File Name: " + file_name)
        text.textLine("Digest: " + file_hash)
        text.textLine("Uploaded By (Email): " + uploaded_by)
        text.textLine("Uploaded Time (UTC): " + uploaded_timestamp)

        text.textLine(" ")

        text.setFont("Courier-Bold", 18)
        text.textLine("Virus total top 10 AV engines")
        text.setFont("Courier", 12)
        text.textLine("Top enterprise AV engines were identified using AV-Comparatives.org")
        text.textLine("Read more about them here - ")

        text.textLine("https://www.av-comparatives.org/enterprise/comparison/")
        text.textLine(" ")

        text.setFont("Courier", 12)
        text.textLine(vt_summary)
        text.textLine("Please check the CSV file for results of each of the AV engines")
        text.textLine(" ")
        text.textLine(" ")

        text.setFont("Courier-Bold", 18)
        text.textLine("Clam-AV Report")
        text.setFont("Courier", 12)
        text.textLine("ClamAV is an open source AV engine. Read more here - https://www.clamav.net/")
        text.setFont("Courier", 12)

        if clam_detection == 1:
            text.textLine("ClamAV detected the file as malicious")
            text.textLine(f"Viruses found: {clam_viruses}")

        else:
            text.textLine("ClamAV didn't detect the file as malicious")

        text.textLine(" ")
        text.textLine(" ")

        text.setFont("Courier-Bold", 18)
        text.textLine("Crowd-sourced Yara rules")
        text.setFont("Courier", 12)
        text.textLine("Crowd-sourced yara rules that matched the file are attached in")
        text.textLine("the YARA-report.json file ")

        pdf.drawText(text)

        pdf.save()
        return report_fileName

    except Exception as ex:

        traceback.print_exception(ex)
        print('[PDF Report Generation] Exception: ' + str(ex))
        return None
