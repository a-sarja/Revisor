import time
import traceback

import file_utils
from aws_dynamodb_utils import AwsDynamoDbClient
from aws_s3_utils import AwsS3Client
from email_utils import send_scan_result_email

LOCAL_TEMP_FOLDER = "/home/abhiram/Desktop/CY7900/downloaded_files/"  # Change it to the /tmp/<revisor> in prod environment


def download_files(filepath, sha256, s3_obj):

    remote_csv_filename = sha256 + "/" + str(sha256) + "_results.csv"
    remote_summary_filename = sha256 + "/" + str(sha256) + "_summary.txt"
    csv_local = filepath + str(sha256) + "_results.csv"
    summary_local = filepath + str(sha256) + "_summary.txt"

    s3_obj.download_file(s3_file_name=remote_csv_filename, local_file_name=csv_local)
    s3_obj.download_file(s3_file_name=remote_summary_filename, local_file_name=summary_local)
    return csv_local, summary_local


if __name__ == '__main__':

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
                    for each_key, each_value in reports.items():
                        csv_file_local, summary_file_local = download_files(filepath=LOCAL_TEMP_FOLDER, sha256=str(each_key), s3_obj=s3_object)
                        # Send the email
                        if summary_file_local and csv_file_local:
                            send_scan_result_email(destination_email=str(each_value), summary_filepath=summary_file_local, csv_filepath=csv_file_local)
                            # Delete the downloaded files from local as soon as they are sent to the user through emails
                            file_utils.delete_file(filepath=summary_file_local)
                            file_utils.delete_file(filepath=csv_file_local)
                            # Update the email status to `sent`
                            ddb_object.update_email_status(sha256=str(each_key))

            print("A batch of emails has been sent")
            time.sleep(30)  # # Sleeping for sometime to wait for new scan reports uploaded to S3 -> 30 seconds is ideal time

    except Exception as ex:
        traceback.print_exception(ex)
        print(str(ex))
