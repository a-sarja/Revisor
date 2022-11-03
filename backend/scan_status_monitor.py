import os
import time
import traceback

import file_utils
from aws_dynamodb_utils import AwsDynamoDbClient
from aws_s3_utils import AwsS3Client
from email_utils import send_scan_result_email

LOCAL_TEMP_FOLDER = "downloaded_files/"  # Change it to the /tmp/<revisor> in prod environment


def download_files(filepath, sha256, s3_obj):

    vt_scan_filename = sha256 + "/" + str(sha256) + "_results.csv"
    vt_scan_local = filepath + str(sha256) + "_results.csv"

    yara_scan_filename = sha256 + "/" + str(sha256) + "_yara_keywords.txt"
    yara_scan_local = filepath + str(sha256) + "yara_results.txt"

    clamav_scan_filename = sha256 + "/" + str(sha256) + "_ClamAVScan_Report.txt"
    clamav_scan_local = filepath + str(sha256) + "_ClamAVScan_Report.txt"

    s3_obj.download_file(s3_file_name=vt_scan_filename, local_file_name=vt_scan_local)
    s3_obj.download_file(s3_file_name=yara_scan_filename, local_file_name=yara_scan_local)
    s3_obj.download_file(s3_file_name=clamav_scan_filename, local_file_name=clamav_scan_local)

    return vt_scan_local, yara_scan_local, clamav_scan_local


if __name__ == '__main__':

    # Create a temporary directory if not exists already
    if not os.path.exists(LOCAL_TEMP_FOLDER):
        os.mkdir(LOCAL_TEMP_FOLDER)

    ddb_object = AwsDynamoDbClient()
    s3_object = AwsS3Client()
    try:
        while True:
            reports_to_be_emailed = ddb_object.fetch_data_to_send_email()
            if reports_to_be_emailed:
                reports = {}
                for each in reports_to_be_emailed:
                    reports[each['id']] = each['uploaded_by']

                if reports:
                    print(str(len(reports)), ' Emails to be sent..')
                    for each_key, each_value in reports.items():

                        vt_scan_local, yara_scan_local, clamav_scan_local = download_files(filepath=LOCAL_TEMP_FOLDER, sha256=str(each_key), s3_obj=s3_object)
                        # Send the email
                        if clamav_scan_local and yara_scan_local and vt_scan_local:
                            send_scan_result_email(destination_email=str(each_value), vt_scan_local=vt_scan_local, yara_scan_local=yara_scan_local, clamav_scan_local=clamav_scan_local)
                            # Delete the downloaded files from local as soon as they are sent to the user through emails
                            file_utils.delete_file(filepath=clamav_scan_local)
                            file_utils.delete_file(filepath=yara_scan_local)
                            file_utils.delete_file(filepath=vt_scan_local)

                            # Update the email status to `sent`
                            ddb_object.update_email_status(sha256=str(each_key))

                    print("A batch of emails has been sent")

            time.sleep(30)  # Sleeping for sometime to wait for new scan reports uploaded to S3 -> 30 seconds is ideal time

    except Exception as ex:
        traceback.print_exception(ex)
        print(str(ex))
