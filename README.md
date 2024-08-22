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
#General
VERSION = "1.0"

#Flask
ENVIRONMENT = "dev"
JWT_SECRET_KEY = 'SUPER-SECRET'
SECRET_KEY = 'SUPER-SECRET'
FLASK_CONFIG = "testing" # Options: development, testing, production, default
CSRF_ENABLED = False

#Admin user
ADMIN_EMAIL = "admin"
ADMIN_PASSWORD = "password"

#Swish
MERCHANT_SWISH_NUMBER = "1234679304" #Has to match certificate
ALLOWED_SWISH_CALLBACK_IP = "89.46.83.171"
CURRENCY = "SEK"

#Swish Certificates
PEM_CERT_NAME = "Swish_Merchant_TestSigningCertificate_1234679304.pem"
KEY_CERT_NAME = "Swish_Merchant_TestSigningCertificate_1234679304.key"
SWISH_ROOT_CERT_NAME = "Swish_TLS_RootCA.pem"

#API keys
API_KEYS = "api-key,other-api-key"

#Merchant 
MERCHANT_NAME = "Test"
MERCHANT_BASE_URL = "http://localhost:5001"
MERCHANT_API_KEY = "merchant-api-key"

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
Development certificates can be downloaded from Swish: https://developer.swish.nu/documentation/environments#certificates


## Run server
To run the server run the following command in the root folder
```bash
python run.py
```

## Run tests
To run test run the following command in the root folder
```bash
pytest
````

