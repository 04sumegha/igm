from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

class Country(BaseModel):
    code: str

class City(BaseModel):
    code: str

class Location(BaseModel):
    country: Optional[Country] = None
    city: Optional[City] = None

class Context(BaseModel):
    bpp_uri: str
    bpp_id: str
    domain: str
    action: str
    core_version: str
    bap_id: str
    bap_uri: str
    transaction_id: str
    message_id: str
    timestamp: datetime
    ttl: str
    location: Optional[Location] = None

class TagDescriptor(BaseModel):
    code: str

class TagList(BaseModel):
    descriptor: TagDescriptor
    value: str

class Tag(BaseModel):
    descriptor: TagDescriptor
    list: List[TagList]

class Ref(BaseModel):
    ref_id: str
    ref_type: str
    tags: Optional[List[Tag]] = []

class ExpectedTime(BaseModel):
    duration: str

class Name(BaseModel):
    name: str

class Contact(BaseModel):
    phone: str
    email: EmailStr

class Info(BaseModel):
    org: Name
    person: Name
    contact: Contact

class Actor_Info(BaseModel):
    id: str
    type: str
    info: Info

class AdditionalDesc(BaseModel):
    content_type: Optional[str] = None
    url: Optional[str] = None

class Description(BaseModel):
    code: str
    short_desc: str
    long_desc: str
    additional_desc: Optional[AdditionalDesc] = None
    images: Optional[List[HttpUrl]] = []

class ActionDescription(BaseModel):
    code: str
    short_desc: Optional[str] = None
    name: Optional[str] = None

class ActorDetails(BaseModel):
    name: str

class Action(BaseModel):
    id: str
    updated_at: datetime
    action_by: str
    description: ActionDescription
    actor_details: ActorDetails
    ref_id: Optional[str] = None
    ref_type: Optional[str] = None

class Resolution(BaseModel):
    id: str
    ref_id: str
    ref_type: str
    descriptor: ActionDescription
    tags: List[Tag]
    updated_at: datetime
    proposed_by: str

class Issue(BaseModel):
    id: str
    status: str
    level: str
    created_at: datetime
    updated_at: datetime
    source_id: str
    complainant_id: str
    last_action_id: str
    expected_response_time: ExpectedTime
    expected_resolution_time: ExpectedTime
    refs: List[Ref]
    actor_info: List[Actor_Info]
    respondent_ids: List[str]
    description: Description
    actions: List[Action]
    resolutions: Optional[List[Resolution]] = []

class Updated_Target(BaseModel):
    path: str
    action: str

class Message(BaseModel):
    issue: Issue
    updated_target: List[Updated_Target]

class Error(BaseModel):
    type: Optional[str] = None
    code: Optional[str] = None
    path: Optional[str] = None
    message: Optional[str] = None

class OnIssueReq(BaseModel):
    context: Context
    message: Message
    error: Optional[Error] = None

#Response
class Ack(BaseModel):
    status: str

class MessageAck(BaseModel):
    ack: Ack

class ErrorRes(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None

class OnIssueResponse(BaseModel):
    message: MessageAck
    error: Optional[ErrorRes] = None