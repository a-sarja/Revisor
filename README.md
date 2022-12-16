# Revisor - Multi AV file analyzer (Student project)
### Motivation
  * Rising amount of total malware and Potentially Unwanted Applications (PUA).
  * Multi AV file analyzer for better accuracy and efficiency.
  * Ease of use and deployment. Platform agnostic property.
  * Open source resources (Cost effective).
  * API support and building automation.

### Tech Stack
  * **Front End:** HTML5, CSS3, Java Script
  * **Backend:** Python, Flask, AWS - DynamoDB and S3, AV components - Virus Total, Clam AV and crowd sourced Yara rules.

### Set Up
* Download the source code onto your machine or any cloud instance.
* Install Docker.
* Replace the AWS credentials in `config/aws/credentials` with your AWS keys. (To access S3 and DynamoDB services).
* Replace the certificates in `config/backend/certs` with your certificate key pair. (To encrypt the communication between frontend and backend through HTTPS)
* Create new or use an existing email ID that can be used for sending reports. _REVISOR_EMAIL_
* Generate a virus total API key. VT_API_KEY
* Update the below _ENVIRONMENT_ variables in `docker_files/docker-compose.yaml`:
  * _REVISOR_EMAIL_
  * _REVISOR_EMAIL_PASSWORD_
  * _VT_API_KEY_
  * _CLAMD_IP_
* Run below command to set up the docker images and run the containers

  ```
  sudo docker-compose up -d
  ```

### Architecture
High level architecture of the project is shown below:

![Arch](/Images/arch.png?raw=True "Architecture")

### Product screenshots
Front end website/UI to upload the file to be analyzed

![front_end](/Images/front-end.png?raw=True "FrontEnd-UI")

File anayzer report is sent in the form of email. Reports include the summary PDF report and additional files for more context.

![report](/Images/report.png?raw=True "Report")

### API Endpoints
APIs exposed as part of the project and can be used after the deployment is sucessful
  * `GET <host>:443/` - browse home page on the browser
  * `GET <host>:5000/` - Health check API
  * `POST <host>:5000/upload_file` - Upload file for scanning


### Contributors (LinkedIn) 
  - [Abhiram Sarja](https://www.linkedin.com/in/asarja)
  - [Namruth Reddy](https://www.linkedin.com/in/namruth-reddy/)
  - [Prateek Vutkur](https://www.linkedin.com/in/prateek-vutkur/)
  - [Alekhya Digumarthy](https://www.linkedin.com/in/alekhya-digumarthy/)


### Disclaimer
This is a student project (POC) and is not meant for use in production.

Please contact [Abhiram](abhiramsarja@gmail.com) or [Namruth](namruth@outlook.com) for more details