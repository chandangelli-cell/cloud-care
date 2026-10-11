# CloudCare – Smart Cloud-Based Hospital Management System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0.3-brightgreen.svg)](https://palletsprojects.com/p/flask/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy%202.0-red.svg)](https://www.sqlalchemy.org/)
[![Cloud Native](https://img.shields.io/badge/Cloud-AWS%20%7C%20Azure-orange.svg)](#cloud-deployment)
[![Tests Passing](https://img.shields.io/badge/Tests-15%20Passed-success.svg)](#automated-testing)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> **Healthcare Management, Simplified by the Cloud.**  
> CloudCare is a complete, enterprise-grade, cloud-native Hospital Management System (HMS) developed with Python Flask, SQLAlchemy ORM, Bootstrap 5, custom medical glassmorphic design, and cloud storage abstractions (AWS S3 & Azure Blob Storage).

---

## 📑 Table of Contents

1. [System Architecture](#system-architecture)
2. [Cloud Database Schema (14 Tables)](#cloud-database-schema)
3. [User Roles & Functional Modules](#user-roles--functional-modules)
4. [Technology Stack](#technology-stack)
5. [Quick Start & Local Development (Windows / PowerShell)](#quick-start--local-development)
6. [Demo Accounts](#demo-accounts)
7. [Cloud Deployment Guide (AWS & Azure)](#cloud-deployment)
8. [Backup & Disaster Recovery Procedures](#backup--disaster-recovery)
9. [Automated Testing](#automated-testing)
10. [REST API Documentation](#rest-api-documentation)
11. [Project Presentation Outline](#project-presentation-outline)

---

## 🏛️ System Architecture

CloudCare follows a decoupled 3-tier cloud architecture designed for high availability, compliance, and multi-tenant security:

```mermaid
graph TB
    subgraph Client Layer
        Browser["Desktop & Mobile Browsers<br/>(Bootstrap 5 + Chart.js + Vanilla JS)"]
    end

    subgraph Cloud Application Layer
        ALB["Application Load Balancer / Nginx (HTTPS)"]
        Flask["Flask Web Application<br/>(Gunicorn WSGI Workers)"]
        subgraph Blueprints
            Auth["Auth & RBAC"]
            Patient["Patient Portal"]
            Doctor["Doctor Portal"]
            Appt["Appointment Engine"]
            Records["Clinical Records"]
            Rx["Prescription Builder"]
            Billing["Billing & Payments"]
            Reports["Cloud Storage Adapter"]
            Admin["Admin Analytics Hub"]
        end
    end

    subgraph Cloud Data & Services Layer
        DB[("Cloud Relational Database<br/>(Amazon RDS / Azure PostgreSQL / SQLite)")]
        Storage[("Private Cloud Object Store<br/>(Amazon S3 / Azure Blob Storage)")]
        Monitor["Monitoring & Logging<br/>(CloudWatch / Azure Monitor)"]
    end

    Browser -->|HTTPS / TLS 1.3| ALB
    ALB --> Flask
    Flask --> Auth
    Flask --> Patient
    Flask --> Doctor
    Flask --> Appt
    Flask --> Records
    Flask --> Rx
    Flask --> Billing
    Flask --> Reports
    Flask --> Admin
    Flask -->|SQLAlchemy ORM Connection Pool| DB
    Reports -->|Short-lived Signed URLs / SAS| Storage
    Flask -->|Audit Trails & Metrics| Monitor
```

---

## 🗄️ Cloud Database Schema

The database consists of 14 normalized relational tables with foreign keys, indexes, cascaded integrity, and audit logging:

```mermaid
erDiagram
    users ||--o| patients : "has profile"
    users ||--o| doctors : "has profile"
    users ||--o{ notifications : "receives"
    users ||--o{ audit_logs : "triggers"
    departments ||--o{ doctors : "belongs to"
    doctors ||--o{ doctor_availability : "configures"
    patients ||--o{ appointments : "books"
    doctors ||--o{ appointments : "attends"
    appointments ||--o| medical_records : "documents"
    appointments ||--o| prescriptions : "prescribes"
    appointments ||--o| bills : "invoiced by"
    prescriptions ||--o{ prescription_items : "contains"
    patients ||--o{ medical_reports : "owns"
    doctors ||--o{ medical_reports : "uploads"
    bills ||--o{ payments : "settled via"

    users {
        int id PK
        string email UK
        string password_hash
        string role
        boolean is_active
        datetime last_login_at
        datetime created_at
    }

    patients {
        int id PK
        int user_id FK
        string patient_identifier UK
        string full_name
        string mobile_number
        date date_of_birth
        string gender
        string blood_group
        text address
        string emergency_contact
    }

    doctors {
        int id PK
        int user_id FK
        int department_id FK
        string full_name
        string specialization
        string qualification
        int experience_years
        float consultation_fee
        string room_number
        boolean is_active
    }

    departments {
        int id PK
        string name UK
        text description
        string icon
        boolean is_active
    }

    doctor_availability {
        int id PK
        int doctor_id FK
        int day_of_week
        time start_time
        time end_time
        int slot_duration_minutes
        boolean is_available
    }

    appointments {
        int id PK
        string appointment_number UK
        int patient_id FK
        int doctor_id FK
        date appointment_date
        time start_time
        time end_time
        text reason_for_visit
        string status
        text cancellation_reason
    }

    medical_records {
        int id PK
        string record_number UK
        int patient_id FK
        int doctor_id FK
        int appointment_id FK
        date consultation_date
        text clinical_notes
        text diagnosis
        text treatment_notes
        boolean is_released_to_patient
    }

    prescriptions {
        int id PK
        string prescription_number UK
        int patient_id FK
        int doctor_id FK
        int appointment_id FK
        date issue_date
        text instructions
        date follow_up_date
    }

    prescription_items {
        int id PK
        int prescription_id FK
        string medication_name
        string dosage
        string frequency
        string duration
        string instructions
    }

    medical_reports {
        int id PK
        string report_number UK
        int patient_id FK
        int doctor_id FK
        string title
        string category
        string original_filename
        string storage_key
        int file_size_bytes
        string mime_type
        string storage_provider
        boolean is_released
        datetime uploaded_at
    }

    bills {
        int id PK
        string bill_number UK
        int patient_id FK
        int appointment_id FK
        float consultation_charge
        float service_charges
        float tax_amount
        float total_amount
        string payment_status
        date issue_date
        date due_date
    }

    payments {
        int id PK
        string transaction_id UK
        int bill_id FK
        int patient_id FK
        float amount_paid
        string payment_method
        string payment_status
        string payment_reference
        datetime payment_date
    }

    notifications {
        int id PK
        int user_id FK
        string title
        text message
        string category
        boolean is_read
        string link_url
        datetime created_at
    }

    audit_logs {
        int id PK
        int user_id FK
        string ip_address
        string action
        string resource_type
        string resource_id
        text details
        string status
        datetime timestamp
    }
```

---

## 👥 User Roles & Functional Modules

### A. Patient
- **Registration & Authentication**: Form validation, secure session management, and instant password hashing.
- **Doctor Directory & Specialist Search**: Filter by medical department, doctor qualification, fee, or clinical condition.
- **Dynamic Slot Booking**: Interactive AJAX calendar slot picker excluding booked slots with concurrent double-booking prevention.
- **Consultation History**: Filter past and upcoming appointments with cancellation workflows.
- **Medical Records**: Access released diagnosis, clinical observations, and therapeutic instructions.
- **Prescription Downloads**: View active prescriptions and download electronically certified PDF copies.
- **Medical Report Storage**: Secure access to lab tests and imaging scans stored in private cloud storage.
- **Simulated Payment Settlement**: Settle bills with Cards, UPI, or Netbanking, receiving official PDF invoices.
- **In-App Notifications**: Real-time alerts for booking confirmations, prescription releases, and billing updates.

### B. Doctor
- **Clinical Dashboard**: Real-time view of today's schedule, pending visits, and patients treated.
- **Availability Schedule Manager**: Configure weekly working days, operating hours, and custom appointment duration (15 to 60 min).
- **Patient Dossier Inspection**: Authorized view of a patient's historical diagnoses, past prescriptions, and diagnostic scans.
- **Consultation Recording**: Document examination observations, diagnoses, and release status.
- **Interactive Prescription Builder**: Add multiple medicine rows dynamically with medication name, dosage, frequency, and instructions.
- **Report Uploading**: Upload lab and radiology documents directly associated with the patient's record.
- **Status Progression**: Mark appointments as Confirmed or Completed.

### C. Hospital Administrator
- **Executive Operations Dashboard**: Hospital KPIs computed dynamically from real database records (Total Patients, Active Doctors, Consultations Handled, Revenue, and Outstanding Receivables).
- **Chart.js Visualizations**: 12-month patient booking trends and appointment status distribution.
- **Doctor Staff Management**: Add new doctors, assign departments, configure initial schedules, or deactivate accounts.
- **Patient Account Controls**: Audit registered patients and toggle account suspension.
- **Hospital-Wide Appointment Oversight**: Global search, filter by doctor/status/date, and update states.
- **Manual Invoicing**: Issue custom hospital bills with breakdown of consultation and facility charges.
- **Compliance Audit Trail**: Immutable logging of all clinical views, document downloads, logins, and status updates with IP address and timestamps.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, FontAwesome 6.5, Chart.js 4.4 |
| **Backend** | Python 3.10+, Flask 3.0.3, Flask Blueprints, Flask-Login, Flask-WTF |
| **ORM & Database** | SQLAlchemy 2.0, SQLite (Local Dev), PostgreSQL / MySQL (Cloud Production) |
| **Document Generation** | ReportLab 4.2 (Official Prescription & Tax Invoice PDFs) |
| **Cloud Storage** | AWS S3 SDK (`boto3`), Azure Blob Storage SDK (`azure-storage-blob`), Local Fallback |
| **Testing** | Pytest 8.2, Pytest-Flask |
| **Production WSGI** | Gunicorn 22.0 |

---

## 🚀 Quick Start & Local Development

### 1. Prerequisites
- Windows 10/11, macOS, or Linux
- Python 3.10 or higher
- PowerShell or Bash terminal

### 2. Setup Virtual Environment
In your PowerShell terminal:
```powershell
# Navigate to the project directory
cd c:\Users\Chand\OneDrive\Desktop\pocket-medicator

# Create Python virtual environment
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Initialize Database & Seed Demo Data
```powershell
# Create all 14 tables in SQLite
flask --app run.py init-db

# Populate with realistic doctors, departments, patients, appointments, and bills
flask --app run.py seed-data
```

### 5. Launch Local Development Server
```powershell
python run.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 🔑 Demo Accounts

For immediate evaluation, the login page (`/login`) includes **1-click quick fill buttons** for the following pre-configured demonstration accounts:

| Role | Email | Password | Description |
|---|---|---|---|
| **Administrator** | `admin@cloudcare.hospital` | `Admin12345!` | Full executive access, audit trail, staff management |
| **Doctor** | `dr.smith@cloudcare.hospital` | `Doctor12345!` | Dr. Robert Smith (Cardiology) |
| **Doctor** | `dr.chen@cloudcare.hospital` | `Doctor12345!` | Dr. Emily Chen (Neurology) |
| **Patient** | `patient.john@example.com` | `Patient12345!` | John Doe (Has scheduled & historical appointments) |
| **Patient** | `patient.alice@example.com` | `Patient12345!` | Alice Johnson |

To create a brand new custom administrator from the command line:
```powershell
flask --app run.py create-admin --email your.admin@hospital.com --password YourSecurePassword123!
```

---

## ☁️ Cloud Deployment Guide

### Option A: AWS Deployment (Elastic Beanstalk + RDS + S3)

#### 1. Amazon RDS PostgreSQL Database
1. Open the **AWS RDS Console** and select **Create Database**.
2. Engine: **PostgreSQL 15+**.
3. Template: **Free Tier** (or Production Multi-AZ for high availability).
4. Settings: DB instance identifier `cloudcare-db`, master username `cloudadmin`, master password `YourStrongPassword!`.
5. Under Connectivity, ensure **Public access** is set to `Yes` or attach it to the same VPC as your Elastic Beanstalk environment.
6. Note the RDS endpoint: e.g. `cloudcare-db.cxxxxxx.us-east-1.rds.amazonaws.com`.

#### 2. Amazon S3 Private Bucket for Medical Documents
1. Open the **AWS S3 Console** and click **Create bucket**.
2. Bucket name: `cloudcare-medical-reports`.
3. Region: `us-east-1`.
4. **Block Public Access**: Keep **Block all public access** checked (HIPAA security). CloudCare serves files securely via pre-signed URLs!
5. In IAM, create a service user or attach a policy to the Elastic Beanstalk instance role granting `s3:PutObject`, `s3:GetObject`, and `s3:DeleteObject`.

#### 3. AWS Elastic Beanstalk Deployment
1. Install AWS EB CLI: `pip install awsebcli`.
2. Initialize environment:
   ```bash
   eb init -p python-3.10 cloudcare-hms --region us-east-1
   ```
3. Set Environment Variables in `.ebextensions/01_flask.config` or through EB Console:
   - `DATABASE_URL=postgresql://cloudadmin:YourStrongPassword!@cloudcare-db.cxxxxxx.us-east-1.rds.amazonaws.com:5432/cloudcare_db`
   - `STORAGE_PROVIDER=aws_s3`
   - `S3_BUCKET_NAME=cloudcare-medical-reports`
   - `AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY`
   - `AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY`
   - `SECRET_KEY=generate-a-strong-random-secret-key-32-chars`
4. Deploy the application:
   ```bash
   eb create cloudcare-prod-env
   eb deploy
   ```

---

### Option B: Microsoft Azure Deployment (App Service + Azure PostgreSQL + Blob Storage)

#### 1. Azure Database for PostgreSQL
```bash
az postgres flexible-server create \
  --resource-group rg-cloudcare \
  --name cloudcare-psql-server \
  --admin-user cloudadmin \
  --admin-password "YourStrongPassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable
```

#### 2. Azure Blob Storage
```bash
az storage account create \
  --name cloudcarestorageaccount \
  --resource-group rg-cloudcare \
  --location eastus \
  --sku Standard_LRS

az storage container create \
  --account-name cloudcarestorageaccount \
  --name cloudcare-reports \
  --public-access off
```

#### 3. Azure App Service
```bash
az webapp up \
  --resource-group rg-cloudcare \
  --plan cloudcare-appservice-plan \
  --name cloudcare-hms-app \
  --runtime "PYTHON:3.10" \
  --startup-file "startup.sh"

# Set App Settings (Environment Variables)
az webapp config appsettings set \
  --resource-group rg-cloudcare \
  --name cloudcare-hms-app \
  --settings \
    STORAGE_PROVIDER="azure_blob" \
    AZURE_STORAGE_CONNECTION_STRING="<YourConnectionString>" \
    AZURE_CONTAINER_NAME="cloudcare-reports" \
    DATABASE_URL="postgresql://cloudadmin:YourStrongPassword123!@cloudcare-psql-server.postgres.database.azure.com:5432/postgres" \
    SECRET_KEY="generate-random-secret-key"
```

---

## 🛡️ Backup & Disaster Recovery

### Automated Database Backup
- **AWS RDS**: Configured with automated daily snapshots with 35-day retention and continuous Point-In-Time Restore (PITR) within 5-minute increments.
- **Azure PostgreSQL**: Configured with geo-redundant backups retained for 7 to 35 days.

### Storage Bucket Disaster Recovery
- S3 / Azure Blob Storage versioning enabled.
- Cross-region replication (CRR) enabled between `us-east-1` (Primary) and `us-west-2` (Disaster Recovery).

### Restoration Testing Protocol
1. Stand up a staging test database from the snapshot:
   ```bash
   aws rds restore-db-instance-to-point-in-time \
     --source-db-instance-identifier cloudcare-db \
     --target-db-instance-identifier cloudcare-db-restore-test \
     --restore-time 2026-10-10T00:00:00.000Z
   ```
2. Verify table integrity and run pytest test suite against restored database.
3. Terminate test restore instance after audit confirmation.

---

## 🧪 Automated Testing

The project includes automated integration tests covering Authentication, Role-Based Access Control (RBAC), Data Isolation, Appointment Scheduling, Duplicate Prevention, Billing Calculations, and File Upload Validations.

Run tests using pytest:
```powershell
.\.venv\Scripts\python -m pytest -v tests
```

### Test Coverage Highlights:
- `test_patient_registration_success`: Validates field checks, uniqueness, and password hashing.
- `test_duplicate_booking_prevention`: Proves concurrent conflict detection prevents overlapping doctor slots.
- `test_patient_data_isolation_billing`: Proves patients cannot access or settle unauthorized patient bills.
- `test_invoice_pdf_generation`: Validates ReportLab generating real binary PDF invoices.
- `test_invalid_file_extension_rejected`: Verifies rejection of unauthorized file formats (`.exe`).

---

## 📡 REST API Documentation

| Endpoint | Method | Role | Description |
|---|---|---|---|
| `/api/health` | `GET` | Public | Cloud infrastructure health-check |
| `/api/doctors` | `GET` | Public | List active doctors & specialties |
| `/api/doctors/<id>` | `GET` | Public | Doctor profile & available schedules |
| `/api/departments` | `GET` | Public | List medical departments |
| `/appointments/available-slots` | `GET` | Public/Auth | Live available slots calculation for a date |
| `/api/notifications` | `GET` | Authenticated | User's in-app notifications |
| `/api/notifications/mark-read` | `POST` | Authenticated | Mark notifications read |
| `/api/analytics/admin` | `GET` | Admin | Real-time KPI metrics & trend data |

---

## 🎤 Project Presentation Outline

1. **Slide 1: Title & Vision**
   - CloudCare: Smart Cloud-Based Hospital Management System
   - Bridging patients, doctors, and administration through a scalable cloud platform.
2. **Slide 2: Problem Statement & Healthcare Challenges**
   - Fragmented records, double-booking errors, and insecure paper document distribution.
3. **Slide 3: Cloud Architecture**
   - Elastic compute (AWS Beanstalk / Azure App Service).
   - Private document storage (AWS S3 / Azure Blob) with pre-signed authorization.
   - Managed relational database with automated snapshots.
4. **Slide 4: Key Stakeholder Workflows**
   - Patients: Instant appointment scheduling, verified clinical notes, invoice settlements.
   - Doctors: Dynamic schedule management, consultation notes, multi-item prescription issuance.
   - Administrators: Hospital KPI metrics, Chart.js trends, audit logs, and account access management.
5. **Slide 5: Security & Compliance**
   - Salted password hashing, zero-trust RBAC, and HIPAA-ready immutable audit trail.
6. **Slide 6: Live Demonstration & Results**
   - Demo booking flow, prescription PDF download, and administrative analytics hub.

---

## 📄 License
This project is licensed under the MIT License.
