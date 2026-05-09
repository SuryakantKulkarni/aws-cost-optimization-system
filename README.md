<div align="center">

# ☁️ AWS Cost Optimization System

### Cloud • Automation • Monitoring • DevOps

<br/>

[![AWS](https://img.shields.io/badge/AWS-Cloud-orange?style=for-the-badge\&logo=amazonaws)](/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge\&logo=python)](/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?style=for-the-badge\&logo=streamlit)](/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black?style=for-the-badge\&logo=githubactions)](/)
[![Linux](https://img.shields.io/badge/Platform-Ubuntu%20Linux-yellow?style=for-the-badge\&logo=ubuntu)](/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](/)

<br/>

> **Automated AWS cost monitoring and analytics platform built using AWS, Python, Streamlit, and DevOps tools.**

<br/>

**AWS Lambda • EventBridge • SNS • S3 • EC2 • GitHub Actions • PM2**

</div>

---

## 📌 Project Overview

The AWS Cost Optimization System is a cloud-native automation platform that monitors AWS billing data, generates cost reports, stores them in Amazon S3, sends email alerts using SNS, and visualizes analytics through a live Streamlit dashboard hosted on AWS EC2.

The project also includes automated deployment using GitHub Actions and PM2 process management for continuous dashboard availability.

---

## 🏗️ System Architecture

```text
EventBridge Scheduler
        ↓
AWS Lambda Function
        ↓
AWS Cost Explorer API
        ↓
Amazon S3 + Amazon SNS
        ↓
Streamlit Dashboard on EC2
        ↓
GitHub Actions Deployment Pipeline
```

---

## ⚡ Tech Stack

<div align="center">

| ☁️ Cloud |   🐍 Backend   |    📊 Dashboard    |    ⚙️ DevOps   |
| :------: | :------------: | :----------------: | :------------: |
|    AWS   | Python + Boto3 | Streamlit + Plotly | GitHub Actions |

| 🗄️ Storage |  🔔 Alerts | 🖥️ Hosting |     🐧 OS    |
| :---------: | :--------: | :---------: | :----------: |
|  Amazon S3  | Amazon SNS |   AWS EC2   | Ubuntu Linux |

</div>

---

## ☁️ AWS Services Used

| Service            | Purpose                           |
| ------------------ | --------------------------------- |
| AWS Lambda         | Automated billing data collection |
| AWS Cost Explorer  | Fetch AWS spending data           |
| Amazon EventBridge | Schedule Lambda daily             |
| Amazon SNS         | Send email alerts                 |
| Amazon S3          | Store billing reports             |
| Amazon EC2         | Host Streamlit dashboard          |
| AWS IAM            | Manage permissions                |

---

## 🔄 Project Workflow

### 1️⃣ AWS Billing Data Collection

AWS Lambda fetches billing data using AWS Cost Explorer API.

### 2️⃣ Automated Scheduling

Amazon EventBridge automatically triggers Lambda every day.

### 3️⃣ Cost Report Generation

Lambda generates billing reports and uploads them to Amazon S3.

### 4️⃣ Alert Notifications

Amazon SNS sends email alerts when AWS spending exceeds the threshold.

### 5️⃣ Dashboard Visualization

The Streamlit dashboard reads reports from S3 and displays analytics.

### 6️⃣ Live Cloud Deployment

The dashboard is hosted publicly on an AWS EC2 instance.

### 7️⃣ Automated Deployment Pipeline

GitHub Actions automatically deploys new changes to EC2.

---

## 📁 Project Structure

```text
aws-cost-optimization-system/
│
├── 📂 src/
│   ├── lambda_handler.py
│   ├── cost_analyzer.py
│   └── notifier.py
│
├── 📂 .github/
│   └── 📂 workflows/
│       └── deploy.yml
│
├── 📂 screenshots/
│
├── dashboard.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Local Setup

### Clone Repository

```bash
git clone https://github.com/SuryakantKulkarni/aws-cost-optimization-system.git
cd aws-cost-optimization-system
```

---

### Run Streamlit Dashboard

```bash
streamlit run dashboard.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

## 🖥️ EC2 Deployment

### Connect to EC2

```bash
ssh -i cloud-ai-key.pem ubuntu@YOUR_PUBLIC_IP
```

---

### Install Required Packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip git -y
pip3 install streamlit boto3 pandas plotly --break-system-packages
```

---

### Run Dashboard Publicly

```bash
~/.local/bin/streamlit run dashboard.py \
--server.port 8501 --server.address 0.0.0.0
```

Open in browser:

```text
http://YOUR_PUBLIC_IP:8501
```

---

## 🔥 PM2 Process Management

```bash
sudo apt install nodejs npm -y
sudo npm install -g pm2

pm2 start streamlit --name aws-dashboard -- run dashboard.py \
--server.port 8501 --server.address 0.0.0.0

pm2 save
pm2 list
```

---

## 🔄 GitHub Actions CI/CD

### Required GitHub Secrets

| Secret Name | Description           |
| ----------- | --------------------- |
| EC2_HOST    | EC2 Public IP         |
| EC2_USER    | EC2 Username          |
| EC2_SSH_KEY | Full .pem key content |

---

## ☁️ AWS Architecture




---

## 🔐 Security Notes

✅ Used GitHub Secrets for sensitive credentials

✅ Excluded `.pem` files using `.gitignore`

✅ IAM permissions configured for AWS services

✅ Deployment access secured using SSH keys

---

## 🚀 Future Improvements

* CloudWatch monitoring integration
* NGINX reverse proxy setup
* HTTPS configuration
* Service-wise billing analytics
* Advanced dashboard insights
* Cost anomaly detection
* Resource utilization monitoring

---

## 🤝 Connect With Me

<div align="center">

### Suryakant Kulkarni

Cloud & DevOps Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge\&logo=linkedin)](https://www.linkedin.com/in/suryakantkulkarni)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge\&logo=github)](https://github.com/SuryakantKulkarni)

</div>

---

<div align="center">

## ⭐ If you found this project helpful, consider starring the repository!

**Cloud • Automation • DevOps • Continuous Learning 🚀**

</div>
