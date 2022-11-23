# Revisor
Basic implementation of `multi file checker` AV engines. One can use this service to scan ANY type of files for maliciousness.

### Tech Stack
  * **Front End:** HTML5, CSS3, Java Script
  * **Backend:** Python Flask, AWS, DynamoDB, AWS S3
  * **AV Engines:** Virus Total, Clam AV, and customised YARA rules to check malware

### Set Up

* Replace the AWS credentials in `config/aws/credentials` with appropriate values
* Update the below _ENVIRONMENT_ variables in `docker-compose.yaml`:
  * _REVISOR_EMAIL_
  * _REVISOR_EMAIL_PASSWORD_
  * _VT_API_KEY_
  * _CLAMD_IP_
* Run below command to set up the docker images and run the containers

  ```
  sudo docker compose up -d
  ```

### API Endpoints
There are a couple of APIs exposed as part of the project
  * `GET <host>:80/` - browse home page on the browser
  * `GET <host>:5000/` - Health check API
  * `POST <host>:5000/upload_file` - Upload file for scanning

### Contributors
  - [Abhiram Sarja](https://www.linkedin.com/in/asarja)
  - [Namruth Reddy](https://www.linkedin.com/in/namruth-reddy/)
  - [Prateek Vutkur](https://www.linkedin.com/in/prateek-vutkur/)
  - [Alekhya Digumarthy](https://www.linkedin.com/in/alekhya-digumarthy/)


