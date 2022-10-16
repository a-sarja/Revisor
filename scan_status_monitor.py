import time
import traceback

import file_utils
from aws_dynamodb_utils import AwsDynamoDbClient
from aws_s3_utils import AwsS3Client
from email_utils import send_scan_result_email

LOCAL_TEMP_FOLDER = "/home/abhiram/Desktop/CY7900/downloaded_files/"  # Change it to the /tmp/<revisor> in prod environment

if __name__ == '__main__':

    ddb_object = AwsDynamoDbClient()
    s3_object = AwsS3Client()
    try:
        while True:
            reports_to_be_emailed = ddb_object.check_scan_status()
            if reports_to_be_emailed:
                reports = {}

                for each in reports_to_be_emailed:
                    reports[each['id']] = each['uploaded_by']

                if reports:
                    for each_key, each_value in reports.items():
                        csv_file_local, summary_file_local = s3_object.download_file(file_path=LOCAL_TEMP_FOLDER, name=each_key)
                        # Send the email
                        if summary_file_local and csv_file_local:
                            send_scan_result_email(destination_email=str(each_value), summary_filepath=summary_file_local, csv_filepath=csv_file_local)

                            # Delete the downloaded files from local as soon as they are sent to the user through emails
                            file_utils.delete_file(filepath=summary_file_local)
                            file_utils.delete_file(filepath=csv_file_local)

            print("A batch of emails sent")
            time.sleep(30)  # # Sleeping for sometime to wait for new scan reports uploaded to S3 -> 30 seconds is ideal time

    except Exception as ex:
        traceback.print_exception(ex)
        print(str(ex))
