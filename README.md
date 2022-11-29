# Revisor
### Motivation
Implementation of `multi file checker` AV engines. Revisor would enable users to collate the information from independent analysis of 3 AV engines which can generate a elaborate analysis report containing corroborative information on the malicious nature of the input file, thereby offering more information to the user about the input file.

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
  sudo docker-compose up -d
  ```

### Flowchart
The below flowchart describes our Revisor application comprising Frontend, Backend and Cloud services components.

<img width="400" alt="flownew" src="https://user-images.githubusercontent.com/100332027/204668945-3ce71a0d-b2e6-4061-aba0-132ae52a094d.PNG">

### Results
UI

<img width="400" alt="UI" src="https://user-images.githubusercontent.com/100332027/204435532-67f90f69-fad0-413d-8886-3d2ac7c7460e.PNG">

Report sent to User email

<img width="400" alt="report 101" src="https://user-images.githubusercontent.com/100332027/204668861-757ef2ea-4453-45d6-ad14-48682bea7c15.PNG">


### API Endpoints
There are a couple of APIs exposed as part of the project
  * `GET <host>:80/` - browse home page on the browser
  * `GET <host>:5000/` - Health check API
  * `POST <host>:5000/upload_file` - Upload file for scanning

### Limitations
  * The input file size is limited to 32mb
  * False positives in malware identification are a frequent drawback of malware scanning software


### Contributors
  - [Abhiram Sarja](https://www.linkedin.com/in/asarja)
  - [Namruth Reddy](https://www.linkedin.com/in/namruth-reddy/)
  - [Prateek Vutkur](https://www.linkedin.com/in/prateek-vutkur/)
  - [Alekhya Digumarthy](https://www.linkedin.com/in/alekhya-digumarthy/)


