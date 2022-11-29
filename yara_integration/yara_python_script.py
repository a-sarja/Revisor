import yara
import time
import sys
import os
import pathlib
import json
curdir = os.getcwd()
revisor_path = curdir.replace("/yara_integration", "")

sys.path.insert(0, revisor_path)

from backend.aws_s3_utils import *
from backend.aws_dynamodb_utils import *
from backend.file_utils import *

aws_s3 = AwsS3Client()
aws_ddb = AwsDynamoDbClient()


rules_dirs = ["crowd_sourced_yara_rules", "custom_yara_rules"]


def mycallback(data):
    if data['meta'] and len(data['meta']) >=3 :
        matched_rules[data['rule']] = data['meta']
    return yara.CALLBACK_CONTINUE


yara_files = []

for rules_dir in rules_dirs:
    for path, currentDirectory, files in os.walk(rules_dir):
        for file in files:
            file_ext = pathlib.Path(os.path.join(path, file)).suffix
            if file_ext == '.yar' or file_ext == '.yara':
                yara_files.append(os.path.join(path, file))

while True:

    unscanned_files = aws_ddb.get_unscanned_files('yara_av')

    if unscanned_files:
        print(unscanned_files)

        for file in unscanned_files:
            matched_rules = {}

            db_file_id = file['id']
            aws_ddb.update_scan_status(db_file_id, 1, 'yara_av')

            pwd = os.getcwd()

            new_path = pwd + f'/{db_file_id}'
            print(new_path)
            if not os.path.exists(new_path):
                os.makedirs(new_path)

            aws_s3.download_file(f'{db_file_id}/{db_file_id}', f'{db_file_id}/{db_file_id}')

            unzip_file(f'{db_file_id}', f'{db_file_id}/{db_file_id}', "CY7900")

            for rule_file in yara_files:
                try:
                    rules = yara.compile(rule_file)
                    match = rules.match(f'{db_file_id}/{db_file_id}', callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)

                except:
                    continue

            with open(f"{db_file_id}/{db_file_id}_yara_report.json", "w") as results_fp:
                results_fp.write(json.dumps(matched_rules, indent=4))

            aws_s3.upload_file(f"{db_file_id}/{db_file_id}_yara_report.json", f"{db_file_id}/{db_file_id}_yara_report.json")

            aws_ddb.update_scan_status(db_file_id, 2, 'yara_av')

    else:
        print("No unscanned files found")
        time.sleep(60)
