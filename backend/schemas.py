from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class StoreBase(BaseModel):
    name: str = Field(..., description="Store name in Arabic or English")
    cat: str = Field(..., description="Category code: r, m, s, h, f, g")
    phone: Optional[str] = Field(None, description="Contact phone number")
    open24: bool = Field(False, description="Whether open 24 hours")


class StoreCreate(StoreBase):
    pass


class StoreOut(StoreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class InquiryCreate(BaseModel):
    name: str = Field(..., description="Full name of applicant")
    phone: str = Field(..., description="Phone/WhatsApp number")
    business: str = Field(..., description="Commercial activity type")
    message: Optional[str] = Field(None, description="Requested area or additional details")


class InquiryOut(BaseModel):
    id: int
    name: str
    phone: str
    business: str
    message: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

