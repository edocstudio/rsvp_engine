from typing import Dict, Any
from boto3 import client, resource
from json import dumps
from google.oauth2.service_account import Credentials
from gspread import authorize, Worksheet
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from pandas import DataFrame, concat
from config import (
    GCP_CRED_PATH,
    GCP_SCOPE,
    SQS_URL,
    DYNAMODB_TABLE,
    SYMM_DATA,
    SALT
)
from common.model import RequestModel


def get_gsheet_client():
    creds = Credentials.from_service_account_file(GCP_CRED_PATH, scopes=GCP_SCOPE)
    return authorize(creds)

def upsert_gsheet_row(sheet: Worksheet, msg: Dict[str, Any]):
    """
    Upsert (update/insert) row in Google Sheet using name+surname as composite key.
    """
    try:
        new_df = DataFrame([msg])
        current_df = get_as_dataframe(sheet).dropna(how="all")
        key_cols = ['name', 'surname']
        updated_df = concat([
            current_df[~current_df[key_cols].apply(tuple, axis=1)
            .isin(new_df[key_cols].apply(tuple, axis=1))],
            new_df
        ], ignore_index=True)
        set_with_dataframe(sheet, updated_df)
    except Exception as e:
        raise Exception(f"Failed to upsert Google Sheet: {e}")

def send_sqs_notification(event: RequestModel):
    """
    Send a notification message to SQS if mail is present.
    """
    try:
        mail = SYMM_DATA.decrypt_aes_gcm(event.body.mail, SALT)
        if mail and str(mail).lower() not in ('', 'none', 'null'):
            sqs = client('sqs', region_name='ap-southeast-1')
            res = sqs.send_message(
                QueueUrl=SQS_URL,
                MessageBody=dumps({
                    "full_name": ' '.join([event.body.name, event.body.surname]),
                    "mail": mail,
                    "side": event.body.side,
                    "guest": event.body.guest,
                    "status": event.body.status
                }),
                MessageGroupId="wedding-invitation",
            )
            print(f"SQS sent: {res}")
    except Exception as e:
        raise Exception(f"Failed to send SQS: {e}")

def persist_to_dynamodb(body: dict):
    """
    Persist event to DynamoDB.
    """
    try:
        dynamodb = resource('dynamodb', region_name='ap-southeast-1')
        table = dynamodb.Table(DYNAMODB_TABLE)
        res = table.put_item(Item=body)
        print(f"DynamoDB saved: {res}")
    except Exception as e:
        raise Exception(f"Failed to upsert DynamoDB: {e}")
