import requests
import sys
import time
import csv
import os

vt_api_key = ''

class VirusTotalClient:

    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "x-apikey": vt_api_key
        }

    def upload_file(self, file_path):
        files = {"file": open(file_path, "rb")}
        url_file = "https://www.virustotal.com/api/v3/files"
        response = requests.post(url_file, files=files, headers=self.headers)
        response_dict = response.json()
        file_id = response_dict['data']['id']
        return file_id

    def scan_file(self, file_id, file_path):
        url_report = f"https://www.virustotal.com/api/v3/analyses/{file_id}"

        response = requests.get(url_report, headers=self.headers)

        response_dict = response.json()

        while(response_dict['data']['attributes']['status'] == "queued"):
            print("Waiting for analysis to be completed")
            time.sleep(30)
            response = requests.get(url_report, headers=self.headers)
            response_dict = response.json()
        file_name = file_name = os.path.basename(file_path)

        with open(f"{file_name}/{file_name}_summary.txt", "w") as results_fp:    
            results_fp.write(str(response_dict['data']['attributes']['stats']))

        with open(f"{file_name}/{file_name}_results.csv", "w", newline='') as results_fp:
            writer = csv.writer(results_fp)
            header = ["engine_name", "engine_version", "result", "category", "method", "engine_update_date"]
            writer.writerow(header)
            for engine in response_dict['data']['attributes']['results']:
                
                engine_name = response_dict['data']['attributes']['results'][engine]["engine_name"]
                engine_version = response_dict['data']['attributes']['results'][engine]["engine_version"]
                engine_result = response_dict['data']['attributes']['results'][engine]["result"]
                engine_category = response_dict['data']['attributes']['results'][engine]["category"]
                engine_method = response_dict['data']['attributes']['results'][engine]["method"]
                engine_update = response_dict['data']['attributes']['results'][engine]["engine_update"]
                
                engine_detail = [engine_name, engine_version, engine_result,\
                    engine_category, engine_method, engine_update]
                writer.writerow(engine_detail)
        
        return (f"{file_name}/{file_name}_summary.txt",f"{file_name}/{file_name}_results.csv")