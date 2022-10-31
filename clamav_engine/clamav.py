import os
import sys
import time
import requests

curdir = os.getcwd()
revisor_path = curdir.replace("/clamav_engine", "")
sys.path.insert(0, revisor_path)

from backend.aws_dynamodb_utils import AwsDynamoDbClient
from backend.aws_s3_utils import AwsS3Client
from backend.file_utils import unzip_file, delete_file, write_file

LOCAL_TEMP_FOLDER = "/home/abhiram/Desktop/CY7900/clamav_files"  # Change it to the /tmp/<revisor> in prod environment


class ClamAVEngine:

    def __init__(self):
        self.av_name = 'clamav'
        self.host = 'http://localhost:8080'
        self.url = self.host + '/api/v1/scan'
        self.app_form_key = 'FILE'

    def scan_file(self, filepath):

        if not os.path.exists(filepath):
            return

        file_to_be_scanned = [(self.app_form_key, open(filepath, 'rb'))]
        scan_report = requests.post(self.url, files=file_to_be_scanned)
        if scan_report.status_code == 200:
            return str(scan_report.text)

    def clamav_process(self, aws_ddb, aws_s3):

        files_to_be_scanned = aws_ddb.get_unscanned_files(scan_engine=self.av_name)
        print(len(files_to_be_scanned), ' samples are sent to Clam AV for scanning..')

        for file in files_to_be_scanned:

            db_file_id = file['id']
            aws_ddb.update_scan_status(db_file_id, 1, scan_engine=self.av_name)

            aws_s3.download_file(f'{db_file_id}/{db_file_id}', f'{LOCAL_TEMP_FOLDER}/{db_file_id}')
            unzip_file(folder=f'{LOCAL_TEMP_FOLDER}/{db_file_id}', zip_filename=db_file_id, password='CY7900')

            scan_result = self.scan_file(filepath=f'{LOCAL_TEMP_FOLDER}/{db_file_id}')
            if scan_result:
                # Update the scan status to 2 indicating scan completed
                aws_ddb.update_scan_status(db_file_id, 2, scan_engine=self.av_name)

                # Write the scan result to a file to be emailed to the customer
                print(str(scan_result))
                write_file(
                    filename=f'{db_file_id}{"_ClamAVScan_Report.txt"}',
                    path=f'{LOCAL_TEMP_FOLDER}',
                    content=str(scan_result)
                )

                # Upload the report file to S3
                aws_s3.upload_file(
                    file_path=f'{LOCAL_TEMP_FOLDER}/{db_file_id}{"_ClamAVScan_Report.txt"}',
                    name=f'{str(db_file_id)}/{db_file_id}{"_ClamAVScan_Report.txt"}'
                )

                # Delete files from the local
                delete_file(filepath=f'{LOCAL_TEMP_FOLDER}/{db_file_id}')
                delete_file(filepath=f'{LOCAL_TEMP_FOLDER}/{db_file_id}{"_ClamAVScan_Report.txt"}')


if __name__ == '__main__':

    aws_s3 = AwsS3Client()
    aws_ddb = AwsDynamoDbClient()

    while True:
        clamav_engine = ClamAVEngine()
        clamav_engine.clamav_process(aws_ddb=aws_ddb, aws_s3=aws_s3)
        time.sleep(10)  # Sleep for 10 seconds between scans
