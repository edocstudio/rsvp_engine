# RSVP Online – Lambda API Request

Automate and secure your wedding guest invitations and RSVP tracking with a scalable, serverless backend powered by AWS Lambda.

---

## Features

- **Secure RSVP API** endpoint with API Key (via AWS API Gateway)
- **Real-time guest data storage** and tracking
- **Automated notifications** and data sync to Google Sheets
- **End-to-end encryption** for guest privacy
- **Fully serverless**, cost-efficient and scalable
- **Seamless integration** with event organizer’s Google Sheets

---

## Architecture Overview

- **Route 53** – Domain Name Service for custom domain (optional)
- **CloudFront** – CDN for performance and SSL termination
- **S3** – Static hosting for Flutter Web App
- **Flutter Web App** – User-facing interface for RSVP
- **API Gateway** (with API Key) – Exposes RESTful endpoints and protects RSVP API
- **AWS Lambda (Main Handler)** – Core compute, processes all RSVP logic
- **DynamoDB** – Stores RSVP and guest info (NoSQL, scalable)
- **Amazon SQS** – Asynchronous message queue for notification pipeline
- **Google Sheets API** – Organizer view and data sync
- **AWS Lambda (Email Consumer)** – Consumes SQS, triggers notification emails
- **AWS SES** – Email delivery service
- **Python** (with gspread, pandas, cryptography) – Logic and security

---

## Architecture Diagram

```
[User]
   |
   v
[Route 53]
   |
   v
[CloudFront]
   |
   v
[S3 (Flutter Web Hosting)]
   |
   v
[Flutter Web App]
   |
   v
[API Gateway (with API Key)]
   |
   v
[Lambda (Main Handler)]
  /    |        \
 /     |         \
v      v          v
[DynamoDB] [Google Sheets] [SQS]
                                |
                                v
                      [Lambda (Email Consumer)]
                                |
                                v
                              [SES]
```

---

## How it Works

1. **Guest** submits RSVP via the Flutter web app
2. **API Gateway** (with API Key) receives the request and triggers **AWS Lambda**
3. **Lambda (Main Handler)** function decrypts and validates RSVP data, then:
   - Stores the data in **DynamoDB**
   - Sends notification messages via **SQS**
   - Updates a connected **Google Sheet** for organizer tracking
4. **Lambda (Email Consumer)** processes SQS messages and sends emails via **SES**
5. Organizers view RSVP status in real-time from Google Sheets

---

## AWS Lambda Usage

AWS Lambda is the central compute component in this project. It processes all incoming RSVP requests, orchestrates data flow between AWS services (DynamoDB, SQS), and manages integration with Google Sheets. Lambda ensures that every operation is secure, event-driven, and scales automatically with zero server management.

---

## Tech Stack

- **AWS Route 53**
- **AWS CloudFront**
- **AWS S3** (Flutter Web Hosting)
- **Flutter** (Web App)
- **AWS API Gateway** (API Key)
- **AWS Lambda**
- **Amazon DynamoDB**
- **Amazon SQS**
- **Google Sheets API**
- **AWS SES**
- **Python** (gspread, pandas, cryptography)

---

## Getting Started

### Prerequisites

- AWS account with access to Lambda, API Gateway, DynamoDB, SQS, SES, S3, CloudFront, Route 53
- Google Cloud service account JSON credentials (for Google Sheets API)
- Python 3.11+ for local development

### Setup

1. **Clone this repo**
2. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```
3. **Deploy AWS resources**\
   (see `infrastructure/` or use your preferred IaC tool)
4. **Set up environment variables:**
   - `GSHEET_KEY` (Google Sheet doc ID)
   - `DYNAMODB_TABLE` (Name of DynamoDB table)
   - `SQS_URL` (SQS queue URL)
   - `DATA_KEY` (Symmetric encryption key or password)
   - `GCP_CRED_PATH` (Path to Google Cloud service account JSON)
   - `EMAIL_FROM` (Sender email for SES/SMTP)
   - `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USN`, `SMTP_PWD` (for SMTP option)
   - `GMAP_LINK` (Google Map URL for event, optional)
5. **Deploy the Lambda functions**\
   (see deployment instructions or use AWS Console/CLI)
6. **Configure API Gateway** with an API Key and link to your Lambda
7. **Deploy Flutter Web App** to S3 and connect custom domain via CloudFront/Route 53

### Usage

- **Send a POST request** (with encrypted RSVP data) to the API Gateway endpoint
- **Use your API Key** in the request as required
- RSVP data will be securely processed and synced to all targets

---

## Security

- All RSVP and guest data is encrypted end-to-end (AES-GCM with PBKDF2)
- API endpoints are secured via API Gateway with API Key
- No guest data is stored unencrypted at any point
- Secrets and credentials are injected via environment variables (never hard-coded)

---

## Contact

Ittipon Bangudsareh\
[coversoul.bank@gmail.com](mailto:coversoul.bank@gmail.com)

---

## Google Sheets (Demo/Organizer View)

[RSVP Tracking Google Sheet](https://docs.google.com/spreadsheets/d/1TyGwlNcNG0Rjh6UcXxSHAqm2GTtbs1kzlxvhl9t5eMM/edit?usp=sharing)

---

## Demo

- **Demo**: [RSVP Online - AWSLambdaHackathon2025](https://youtu.be/1c4nMngYk-U)

---

## Related Repositories

This project is part of a complete serverless RSVP management system.  
See also:

- [Lambda API Request (Main Handler)](https://github.com/your-username/lambda-api-request) – Accepts and processes RSVP submissions
- [Lambda SQS Consumer (Email Notifier)](https://github.com/your-username/lambda-sqs-consumer) – Consumes messages from SQS and sends confirmation emails via SES

Both repositories work together as part of the same architecture and are required for end-to-end functionality.

---

**Contributions, feedback, and ideas are welcome!**
