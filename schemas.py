from typing import Optional

from fastapi import Path
from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str = Field(min_length=10, max_length=13)
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ListingRequest(BaseModel):
    title: str
    description: str
    location: str
    address: str
    rooms: int
    floors: int
    property_type: str
    operation_type: str
    price: int

class ReviewRequest(BaseModel):
    rating: int = Path(gt=0, lt=6)
    comment: str

class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class UpdatePhoneNumberRequest(BaseModel):
    new_phone_number: str

class UpdateProfileRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]