import requests
import sys
import time
import csv

from aws_s3_utils import *
from aws_dynamodb_utils import *


'''
vt_api_key = 'a5472f3bf8cb8e67ed3829028d299b709d29286c4d862f67584617c0dc7bce43'


url_file = "https://www.virustotal.com/api/v3/files"

if len(sys.argv) < 2:
    print("Please input a filename as an argument to the script")
    exit(0)

file_name = sys.argv[1]

try:
    files = {"file": open(file_name, "rb")}

except:
    print("Entered filename not found")
    exit(0)

headers = {
    "accept": "application/json",
    "x-apikey": vt_api_key
}

response = requests.post(url_file, files=files, headers=headers)

print(response.text)

response_dict = response.json()

file_id = response_dict['data']['id']

print(f"file_id:{file_id}")

file_id = 'ZDYxNWQyZjQ4ODRmNmVmZmJmYTUxZTljYjgxOTI5YjQ6MTY2NTU5NDU5OQ=='

url_report = f"https://www.virustotal.com/api/v3/analyses/{file_id}"

response = requests.get(url_report, headers=headers)

response_dict = response.json()

#print(response_dict)
while(response_dict['data']['attributes']['status'] == "queued"):
    print("Waiting for analysis to be completed")
    time.sleep(30)
    response = requests.get(url_report, headers=headers)
    response_dict = response.json()
 
#print(response_dict['data']['attributes']['stats'])

#with open(f"{file_name}_summary.txt", "w") as results_fp:    
#    results_fp.write(str(response_dict['data']['attributes']['stats']))

with open(f"{file_name}_results.csv", "w", newline='') as results_fp:
    writer = csv.writer(results_fp)
    header = ["engine_name", "engine_version", "result", "category", "method", "engine_update_date"]
    writer.writerow(header)
    for engine in response_dict['data']['attributes']['results']:
        #print(engine)
        
        #print(response_dict['data']['attributes']['results'][engine]["engine_version"])
        engine_name = response_dict['data']['attributes']['results'][engine]["engine_name"]
        engine_version = response_dict['data']['attributes']['results'][engine]["engine_version"]
        engine_result = response_dict['data']['attributes']['results'][engine]["result"]
        engine_category = response_dict['data']['attributes']['results'][engine]["category"]
        engine_method = response_dict['data']['attributes']['results'][engine]["method"]
        engine_update = response_dict['data']['attributes']['results'][engine]["engine_update"]
        
        engine_detail = [engine_name, engine_version, engine_result,\
             engine_category, engine_method, engine_update]
        writer.writerow(engine_detail)


    #results_fp.write(str(response_dict['data']['attributes']['results']))

'''

aws_s3 = AwsS3Client()

aws_ddb = AwsDynamoDbClient()

#print(aws_ddb.get_file_details('0d7adfadb89fb2b7f774fbcd6be3cb18afcf13276e2b8efa0867f3f77158e99a'))
#print(aws_s3.upload_file("utils.py", "utils/utils_py"))
#aws_s3.download_file('utils/utils_py', 'utils_py')
print(aws_ddb.get_unscanned_files())

#aws_file_details = aws_ddb.get_file_details('0d7adfadb89fb2b7f774fbcd6be3cb18afcf13276e2b8efa0867f3f77158e99a')
#print(type(aws_file_details))
#print(aws_file_details)

#file_s3_location = aws_file_details['s3_url']
#file_id = aws_file_details['id']
#print(file_s3_location)

#aws_s3.download_file(file_id, file_id)