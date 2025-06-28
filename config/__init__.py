from os import getenv
from common.security import SymmetricData

# --- ENV & CONST ---
GSHEET_KEY = getenv('GSHEET_KEY')
DYNAMODB_TABLE = getenv('DYNAMODB_TABLE')
SQS_URL = getenv('SQS_URL')
DATA_KEY = getenv('DATA_KEY')
GCP_CRED_PATH = getenv('GCP_CRED_PATH')
SALT = getenv('SALT')
TIME_FORMAT = getenv('TIME_FORMAT')
TIME_ZONE = getenv('TIME_ZONE')

# --- GCP SETUP ---
GCP_SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# --- SYMMETRIC ---
SYMM_DATA = SymmetricData()