from typing import Any, Optional
from common.utils import (
    get_gsheet_client,
    persist_to_dynamodb,
    send_sqs_notification,
    upsert_gsheet_row
)
from config import (
    GSHEET_KEY
)
from common.model import RequestModel, ResponseModel, AllowCode

# --- MAIN HANDLER ---
def lambda_handler(event: dict, context: Optional[Any] = None):
    resp = ResponseModel()
    try:
        event: RequestModel = RequestModel(**event)
        if event.allow_code not in AllowCode._value2member_map_.keys():
            raise Exception('reject')
        
        # Health check / Wakeup
        if event.allow_code == 'wakeup':
            resp.status_code = 200
            resp.body = 'wakeup'
            return resp.model_dump()

        # Persist to DynamoDB
        persist_to_dynamodb(event.body.model_dump())

        # Send to SQS (email only)
        send_sqs_notification(event)

        # Prepare for Google Sheet update
        sheet_event = event.body.model_dump()
        sheet_event.pop('mail', None)
        gcp_client = get_gsheet_client()
        spreadsheet = gcp_client.open_by_key(GSHEET_KEY)
        upsert_gsheet_row(spreadsheet.sheet1, sheet_event)
        
        resp.status_code = 200
        resp.body = 'OK'
    except Exception as e:
        resp.status_code = 500
        resp.error = str(e)
    
    return resp.model_dump()
