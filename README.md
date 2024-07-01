# Swish backend API

This is a flask backend server used to access SWISHs API. The server will log and save payment history in a database

## Clone git project
```bash
git clone https://github.com/2peppe2/Swish_backend
```
## Installation

```bash
pip install -r requirements.txt
````

## Add environment file
To run this project, you will need to add an environment file named `.env` at the root of your project. This file should contain all the necessary configuration variables required by the application. Here's a template to get you started:

Copy this template to a file named .env in the root of the project

```plaintext
SECRET_KEY = 'PETRUS_ÄR_BÄST_INGEN_PROTESTERAR'
JWT_SECRET_KEY = "SECRET_KEY"
ENVIRONMENT = "dev"
FLASK_CONFIG = "development"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin"
ROOT_PATH = "./"
MERCHANT_SWISH_NUMBER = "1234679304"
PEM_CERT_NAME = "Swish_Merchant_TestCertificate_1234679304.pem"
KEY_CERT_NAME = "Swish_Merchant_TestCertificate_1234679304.key"
SWISH_ROOT_CERT_NAME = "Swish_TLS_RootCA.pem"
```

## Add certificates
In the certs folder add the required Swish certificates.

Example:

```plaintext
cert/
├─ Swish_Merchant_TestCertificate_1234679304.pem
├─ Swish_Merchant_TestCertificate_1234679304.key
└─ Swish_TLS_RootCA.pem
```

## Run server
To run the server run the following command in the root folder
```bash
python run.py
```

