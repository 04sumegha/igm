from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, HttpUrl

class StatusEnum(str, Enum):
    Open = "OPEN"
    Closed = "CLOSED"
    Processing = "PROCESSING"
    Resolved = "RESOLVED"

class LevelEnum(str, Enum):
    Issue = "ISSUE"
    Grievance = "GRIEVANCE"
    Dispute = "DISPUTE"

class AdditionalDesc(BaseModel):
    url: HttpUrl
    content_type: str

class Description(BaseModel):
    code: str #represents category
    short_desc: str
    long_desc: str
    images: Optional[List[HttpUrl]] = None
    additional_desc: Optional[AdditionalDesc] = None

class CreateIssueReq(BaseModel):
    transaction_id: str
    status: StatusEnum
    level: LevelEnum
    complainant_id: str
    source_id: str
    order_id: str
    item_id: str
    description: Description
    ref_id: Optional[str] = None
    ref_type: Optional[str] = None
    actor_name: str