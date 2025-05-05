from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Base(BaseModel):
    is_active: bool = Field(default = True)
    created_at: datetime = Field(default_factory = datetime.now)
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True