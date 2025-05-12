from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, HttpUrl

class StatusEnum(str, Enum):
    Open = "OPEN"
    Closed = "CLOSED"

class LevelEnum(str, Enum):
    Issue = "ISSUE"
    Grievance = "GRIEVANCE"
    Dispute = "DISPUTE"

class ActionDescriptionCodeEnum(str, Enum):
    Open = "OPEN"
    Closed = "CLOSED"
    Processing = "PROCESSING"
    Resolved = "RESOLVED"
    Info_Requested = "INFO_REQUESTED"
    Info_Provided = "INFO_PROVIDED"
    Info_Not_Available = "INFO_NOT_AVAILABLE"
    Resolution_Proposed = "RESOLUTION_PROPOSED"
    Resolution_Cascaded = "RESOLUTION_CASCADED"
    Resolution_Accepted = "RESOLUTION_ACCEPTED"
    Resolution_Rejected = "RESOLUTION_REJECTED"
    Escalated = "ESCALATED"

class UpdateIssueReq(BaseModel):
    status: Optional[StatusEnum] = None
    level: Optional[LevelEnum] = None
    action_type: ActionDescriptionCodeEnum
    short_desc: str
    actor_name: str
    actor_images: Optional[List[HttpUrl]] = None
    ref_id: Optional[str] = None
    ref_type: Optional[str] = None
    complainant_id: str