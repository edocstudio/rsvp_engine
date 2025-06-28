from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from enum import Enum
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Literal
from config import (
    SYMM_DATA,
    SALT,
    TIME_ZONE
)

def now_bkk() -> str:
    return datetime.now(ZoneInfo(TIME_ZONE)).__str__()

class AllowCode(str, Enum):
    WAKEUP = 'wakeup'
    RUNNING = 'running'

class BodyRequestModel(BaseModel):
    name: str
    surname: str 
    status: Literal['accept', 'decline']
    guest: int
    side: Literal['groom', 'bride', 'both']
    mail: str
    register_time: str = Field(default_factory=now_bkk)
    
    @field_validator("surname", mode="before")
    @classmethod
    def decrypt_surname(cls, v):
        if isinstance(v, str) and v is not None:
            try:
                v = SYMM_DATA.decrypt_aes_gcm(v, SALT).strip().title()
            except Exception as e:
                print(e)
        return v

    @field_validator("name", mode="before")
    @classmethod
    def name_title(cls, v):
        if isinstance(v, str) and v is not None:
            v = str(v).strip().title()
        return v

class RequestModel(BaseModel):
    body: BodyRequestModel
    allow_code: str | None
    req_time: str = Field(default_factory=now_bkk)
    
class ResponseModel(BaseModel):
    status_code: int = -1
    body: str | None = None
    error: str = ''
    res_time: str = Field(default_factory=now_bkk)
