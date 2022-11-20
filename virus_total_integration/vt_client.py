import requests
import sys
import time
import csv
import os
import pandas as pd


curdir = os.getcwd()
revisor_path = curdir.replace("/virus_total_integration", "")

sys.path.insert(0, revisor_path)

from config.virus_total.config import vt_api_key

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
        

        print("Analysis completed")
        file_name = os.path.basename(file_path)

        #code to get top 10 AVs
        av_data = pd.read_csv("export.csv")
        av_data.sort_values(["Blocked", "FPs"], axis=0, ascending=[False, True], inplace=True)

        list_of_avs = av_data.values.tolist()

        av_names = []
        av_count = 0
        detection_count = 0
        for av in list_of_avs:
            av_names.append(av[0].lower().replace(" ",""))

        print("Top 10 AVs found")

        with open(f"{file_name}/{file_name}_results.csv", "w", newline='') as results_fp:
            writer = csv.writer(results_fp)
            header = ["engine_name", "engine_version", "result", "category", "method", "engine_update_date"]
            writer.writerow(header)
            for av in av_names:
                for engine in response_dict['data']['attributes']['results']:
                    
                    engine_name = response_dict['data']['attributes']['results'][engine]["engine_name"]
                    engine_version = response_dict['data']['attributes']['results'][engine]["engine_version"]
                    engine_result = response_dict['data']['attributes']['results'][engine]["result"]
                    engine_category = response_dict['data']['attributes']['results'][engine]["category"]
                    engine_method = response_dict['data']['attributes']['results'][engine]["method"]
                    engine_update = response_dict['data']['attributes']['results'][engine]["engine_update"]
                    
                    engine_name_updated = engine_name.lower().replace(" ", "")
                    if engine_name_updated == av:
                        if av_count == 10:
                            break

                        av_count += 1

                        if engine_category == 'malicious':
                            detection_count += 1
                        engine_detail = [engine_name, engine_version, engine_result,\
                            engine_category, engine_method, engine_update]
                        writer.writerow(engine_detail)

        print("CSV file created")    

        detection_percentage = (detection_count/10)*100

        summary_string = f"{detection_percentage}% of top AVs detected the file as malicious"

        with open(f"{file_name}/{file_name}_summary.txt", "w") as results_fp:    
            results_fp.write(summary_string)

        print("Summary file created")

        return (f"{file_name}/{file_name}_summary.txt",f"{file_name}/{file_name}_results.csv")