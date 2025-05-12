from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from models.base import Base

class Description(BaseModel):
    code: str
    short_desc: str
    long_desc: str
    images: Optional[List[HttpUrl]] = None
    url: Optional[str] = None

class ActionDescription(BaseModel):
    code: str
    short_desc: str
    name: Optional[str] = None
    images: Optional[List[HttpUrl]] = None

class ActorDetail(BaseModel):
    userId: str
    name: str

class Actions(BaseModel):
    id: str
    descriptor: ActionDescription
    updated_at: datetime
    action_by: str
    actor_details: ActorDetail
    ref_id: Optional[str] = None
    ref_type: Optional[str] = None

class ResolutionDesc(BaseModel):
    code: str
    short_desc: str
    name: Optional[str] = None

class TagDescriptor(BaseModel):
    code: str

class TagList(BaseModel):
    descriptor: TagDescriptor
    value: str

class Tags(BaseModel):
    descriptor: TagDescriptor
    list: List[TagList]

class Resolutions(BaseModel):
    id: str
    updated_at: datetime
    proposed_by: str
    descriptor: ResolutionDesc
    ref_id: Optional[str] = None
    ref_type: Optional[str] = None
    tags: Optional[List[Tags]] = None

class Name(BaseModel):
    name: str

class Contact(BaseModel):
    phone: str
    email: EmailStr

class GroDetail(BaseModel):
    type: str
    org: Name
    person: Name
    contact: Contact

class ODRDetail(BaseModel):
    type: str
    org: Name
    person: Name
    contact: Contact

class ResolutionTime(BaseModel):
    duration: str

class Issue(Base):
    network_issue_id: str
    transaction_id: str   #done
    status: str   #done
    level: str   #done
    expected_resolution_time: ResolutionTime
    actual_resolution_time: Optional[ResolutionTime] = None
    complainant_id: str   #done
    source_id: str   #done
    order_id: str   #done
    item_id: str   #done
    respondent_ids: Optional[List[str]] = None
    description: Description   #done
    actions: List[Actions]
    resolution: Optional[List[Resolutions]] = None
    gro_details: Optional[List[GroDetail]] = None
    finalized_odr: Optional[ODRDetail] = None