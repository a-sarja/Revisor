# Revisor — Secure, Distributed Multi-Antivirus File Scanning Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Supported-blue.svg)](https://docs.docker.com/compose/)
[![AWS Support](https://img.shields.io/badge/AWS-S3%20%26%20DynamoDB-orange.svg)](https://aws.amazon.com/)

Revisor is a modern, distributed, and highly extensible multi-antivirus scanning pipeline designed for high accuracy, speed, and platform-independent security analysis. By combining multiple detection mechanisms—signature-based (ClamAV), custom rulesets (Yara), and reputation/multi-scanner clouds (VirusTotal)—Revisor provides a robust first line of defense against modern malware and Potentially Unwanted Applications (PUAs).

---

## 🌟 Key Features

* **Multi-Engine Detection**: Leverages the combined power of **ClamAV**, custom/crowdsourced **Yara rules**, and the **VirusTotal API** for comprehensive file analysis.
* **Asynchronous Microservices Architecture**: Decoupled backend and scanning engines coordinate via AWS S3 and DynamoDB, allowing easy scaling of individual components.
* **Secure-by-Design**: Uploaded files are zipped and password-protected (`pyminizip`) during ingestion to prevent accidental execution and secure transit.
* **HTTPS Encryption**: Fully supports SSL/TLS certificates on both the frontend web server (Apache) and backend APIs (Flask).
* **Automated Reporting**: Aggregates scan results from all engines and generates a professional PDF report sent directly to the user's email along with raw analysis CSV/JSON attachments.

---

## 🏗️ Architecture

Revisor employs a decentralized, event-driven microservices pattern:

```
                  ┌──────────────────────┐
                  │     Frontend Web     │
                  │   (Apache / HTTPS)   │
                  └──────────┬───────────┘
                             │ (HTTPS POST /upload-file)
                             ▼
                  ┌──────────────────────┐
                  │     Backend API      │
                  │   (Flask / HTTPS)    │
                  └─────┬──────────┬─────┘
   (Upload Zip)         │          │         (Create File Record)
   ┌────────────────────┘          └─────────────────────┐
   ▼                                                     ▼
┌──────────────────────┐                       ┌──────────────────┐
│        AWS S3        │                       │   AWS DynamoDB   │
│  (revisorfiles-v2)   │                       │ (revisor_files)  │
└──────────────────────┘                       └──────────────────┘
   ▲                ▲                                    ▲
   │                │                                    │
   │ (Download/     │ (Upload Reports)                   │ (Fetch/Update Status)
   │  Scan Sample)  │                                    │
   └────────────────┴──────────┬─────────────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
     ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
     │    ClamAV    │   │  VirusTotal  │   │  Yara Rules  │
     │ Worker Agent │   │ Worker Agent │   │ Worker Agent │
     └──────────────┘   └──────────────┘   └──────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Scan Status Monitor │
                    │    & Report Gen     │
                    └──────────┬──────────┘
                               │
                               ▼ (SMTP TLS)
                    ┌─────────────────────┐
                    │ Email Notification  │
                    │   (PDF / CSV / JSON)│
                    └─────────────────────┘
```

1. **Ingestion**: The user uploads a file through the HTTPS frontend.
2. **Lockdown & Upload**: The backend hashes the file (SHA256), packages it in a password-protected zip file, uploads it to S3 (`revisorfiles-v2`), and registers the scan tasks in DynamoDB (`revisor_files`).
3. **Decoupled Scanning**: Individual scanning workers (ClamAV, Yara, and VirusTotal) poll DynamoDB for pending scans, download the zip from S3, extract it using the shared password, run their analysis, upload results to S3, and mark their task complete.
4. **Aggregation & Delivery**: The scan status monitor collects all results once all three engines complete, generates a PDF summary report, and emails it to the user.

---

## 📁 Repository Structure

```
.
├── backend/                  # Flask REST API server, database utils, and email notifier
│   ├── aws_dynamodb_utils.py # AWS DynamoDB integration
│   ├── aws_s3_utils.py       # AWS S3 file upload/download utilities
│   ├── email_utils.py        # PDF & attachment email service
│   ├── file_utils.py         # Archiving and temp file handling
│   ├── report_gen.py         # PDF report compiler using ReportLab
│   ├── scan_status_monitor.py# Scanner monitor and dispatch coordinator
│   └── revisor.py            # Flask app server entrypoint
├── frontend/                 # Client UI built with HTML5, CSS3, JS, and nicepage
│   ├── upload-api-service.js # Frontend script communicating with backend
│   └── index.html            # Main file upload landing page
├── clamav_engine/            # ClamAV scanning integration worker
├── virus_total_integration/  # VirusTotal cloud scanning integration worker
├── yara_integration/         # Custom & crowdsourced Yara rules scanning worker
├── config/                   # Configuration directory for AWS and SSL keys
│   ├── aws/                  # Target folder for AWS config and credentials files
│   └── certs/                # Target folder for frontend and backend SSL certificates
├── docker_files/             # Service Dockerfiles and Docker Compose configuration
└── docs/                     # Additional project documents and scanner logs
```

---

## 🚀 Getting Started

### 📋 Prerequisites

Before deploying Revisor, ensure you have:
* **Docker & Docker Compose** installed.
* **AWS Credentials**: An IAM user with access permissions for AWS S3 and AWS DynamoDB.
* **AWS Resources**:
  * An S3 bucket named `revisorfiles-v2`.
  * A DynamoDB table named `revisor_files` with partition key `id` (String).
* **VirusTotal API Key**: Sign up at [VirusTotal](https://www.virustotal.com/) and retrieve your API key.
* **Email Account for SMTP**: An email account (e.g., Gmail) and an App Password configured for sending report emails.

---

### 🔧 Setup & Configuration

Follow these steps to configure and build the application stack:

#### 1. Setup AWS Credentials
Create the directory `config/aws` if it does not exist, and add two files:

* **`config/aws/config`**:
  ```ini
  [default]
  region = us-east-2
  ```

* **`config/aws/credentials`**:
  ```ini
  [default]
  aws_access_key_id = YOUR_AWS_ACCESS_KEY_ID
  aws_secret_access_key = YOUR_AWS_SECRET_ACCESS_KEY
  ```

*Note: These files will be copied into `/root/.aws` inside the backend, ClamAV, Yara, and VirusTotal containers to enable programmatic access to S3 and DynamoDB.*

#### 2. Generate SSL/TLS Certificates
Generate self-signed SSL certificate key pairs for both the frontend and backend servers.

* **Backend Certificates**:
  ```bash
  mkdir -p config/certs/backend
  openssl req -new -x509 -keyout config/certs/backend/server.pem -out config/certs/backend/cert.pem -days 365 -nodes
  ```

* **Frontend Certificates**:
  ```bash
  mkdir -p config/certs/frontend
  openssl req -new -x509 -keyout config/certs/frontend/server.key -out config/certs/frontend/server.crt -days 365 -nodes
  ```

#### 3. Update Yara Rules
Initialize the crowdsourced Yara rules database by cloning the target rule repositories:
```bash
cd yara_integration
python3 yara_rules_download.py
```
*(To update your cloned Yara rules later, run `python3 yara_rules_update.py`)*

#### 4. Configure Environment Variables
Open `docker_files/docker-compose.yaml` and update the environment variable values:

* **Backend Service**:
  * `REVISOR_EMAIL`: The email address sending scan reports.
  * `REVISOR_EMAIL_PASSWORD`: The App Password for the sending email account.
* **VirusTotal Service**:
  * `VT_API_KEY`: Your VirusTotal API Key.
* **ClamAV REST API Service (CRA)**:
  * `CLAMD_IP`: The IP address of your host machine running Docker (needed for ClamAV REST API communication).

---

### 📦 Run the Containers

To build the images and launch the complete stack in the background, navigate to the docker files directory and run:

```bash
cd docker_files
docker-compose up --build -d
```

To stop all services:
```bash
docker-compose down
```

---

## 🔌 API Reference

### 1. Welcome & Initializer
* **Endpoint**: `GET /`
* **Port**: `5000`
* **Description**: Verifies API backend health and initializes the background `scan_status_monitor` worker process.
* **Response**:
  ```json
  {
    "code": 1000,
    "message": "Welcome to Revisor - The Next Generation AV Engine!"
  }
  ```

### 2. Upload File for Scan
* **Endpoint**: `POST /upload-file`
* **Port**: `5000`
* **Headers**: `Content-Type: multipart/form-data`
* **Parameters**:
  * `user_file` (File, required): The target file to scan (must be less than 32 MB).
  * `user_email` (String, required): The destination email address for the report.
* **Response (New File)**:
  ```json
  {
    "code": 1004,
    "message": "File is successfully uploaded and sent for scanning"
  }
  ```
* **Response (Cached File)**:
  ```json
  {
    "code": 1004,
    "message": "File already in the database",
    "report": "..."
  }
  ```

---

## 📊 Application Interface

### File Upload Dashboard
The secure frontend dashboard for uploading files and inputting the notification email address.
![front_end](/Images/front-end.png?raw=True "FrontEnd-UI")

### Email Report Summary
Sample of the auto-generated PDF report and CSV/JSON analysis files sent to the user upon scan completion.
![report](/Images/report.png?raw=True "Report")

---

## 🤝 Contributors

* **[Namruth Reddy](https://www.linkedin.com/in/namruth-reddy/)** — [namruth@outlook.com](mailto:namruth@outlook.com)
* **[Abhiram Sarja](https://www.linkedin.com/in/asarja)** — [abhiramsarja@gmail.com](mailto:abhiramsarja@gmail.com)
* **[Prateek Vutkur](https://www.linkedin.com/in/prateek-vutkur/)**
* **[Alekhya Digumarthy](https://www.linkedin.com/in/alekhya-digumarthy/)**

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
