import os
import sys
curdir = os.getcwd()
revisor_path = curdir.replace("/virus_total_integration", "")

sys.path.insert(0, revisor_path)

from backend.aws_s3_utils import *
from backend.aws_dynamodb_utils import *
from vt_client import *
from backend.file_utils import *

vt_api = VirusTotalClient()
aws_s3 = AwsS3Client()
aws_ddb = AwsDynamoDbClient()


if vt_api_key == '':
    print("Enter a valid API key in the VT client file")
    exit(0)

while(1):
    scan_engine = "virustotal"
    unscanned_files = aws_ddb.get_unscanned_files(scan_engine=scan_engine)

    if unscanned_files:
        print(unscanned_files)

        for file in unscanned_files:
            db_file_id = file['id']
            aws_ddb.update_scan_status(db_file_id, 1, scan_engine=scan_engine)
            pwd = os.getcwd()

            new_path = pwd + f'/{db_file_id}'
            print(new_path)
            if not os.path.exists(new_path):
                os.makedirs(new_path)

            aws_s3.download_file(f'{db_file_id}/{db_file_id}', f'{db_file_id}/{db_file_id}')

            unzip_file(f'{db_file_id}', f'{db_file_id}/{db_file_id}', "CY7900")

            vt_file_id = vt_api.upload_file(f'{db_file_id}/{db_file_id}')
            print(vt_file_id)

            (summary_name, results_name) = vt_api.scan_file(vt_file_id, f'{db_file_id}/{db_file_id}')

            aws_s3.upload_file(summary_name, summary_name)
            aws_s3.upload_file(results_name, results_name)

            aws_ddb.update_scan_status(db_file_id, 2, scan_engine=scan_engine)
    
    else:
        print("No unscanned files found")