import yara
import sys
import os
import pathlib
curdir = os.getcwd()
revisor_path = curdir.replace("/yara_integration", "")

sys.path.insert(0, revisor_path)

from backend.aws_s3_utils import *
from backend.aws_dynamodb_utils import *

aws_s3 = AwsS3Client()
aws_ddb = AwsDynamoDbClient()


rules_dir = "crowd_sourced_yara_rules"
#inp_file = sys.argv[2] 

def mycallback(data):
    all_descriptions_list.append(data['meta']['description'])
    return yara.CALLBACK_CONTINUE


yara_files = []

for path, currentDirectory, files in os.walk(rules_dir):
    for file in files:
        file_ext = pathlib.Path(os.path.join(path, file)).suffix
        if file_ext == '.yar' or file_ext == '.yara':
            yara_files.append(os.path.join(path, file))



while(1):
    #unscanned_files = aws_ddb.get_unscanned_yara_files()
    unscanned_files = aws_ddb.get_unscanned_files()
    

    if unscanned_files:
        print(unscanned_files)

        for file in unscanned_files:
            all_descriptions_list = []

            db_file_id = file['id']
            #aws_ddb.update_yara_scan_status(db_file_id, 1)
            aws_ddb.update_scan_status(db_file_id, 1)

            pwd = os.getcwd()

            new_path = pwd + f'/{db_file_id}'
            print(new_path)
            if not os.path.exists(new_path):
                os.makedirs(new_path)

            aws_s3.download_file(f'{db_file_id}/{db_file_id}', f'{db_file_id}/{db_file_id}')

            for rule_file in yara_files:
                try:
                    rules = yara.compile(rule_file)
                    match = rules.match(f'{db_file_id}/{db_file_id}', callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)

                except:
                    continue


            all_descriptions = "\n".join(all_descriptions_list)

            with open(f"{db_file_id}/{db_file_id}_yara_keywords.txt", "w") as results_fp:    
                results_fp.write(all_descriptions)

            aws_s3.upload_file(f"{db_file_id}/{db_file_id}_yara_keywords.txt",f"{db_file_id}/{db_file_id}_yara_keywords.txt")

            #aws_ddb.update_yara_scan_status(db_file_id, 2)
            aws_ddb.update_scan_status(db_file_id, 2)

    
    else:
        print("No unscanned files found")
        break