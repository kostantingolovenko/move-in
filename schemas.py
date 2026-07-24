from typing import Optional
from typing import List
from pydantic import BaseModel, Field, EmailStr

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str = Field(min_length=10, max_length=13)
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ListingImageRequest(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True

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
    rating: int = Field(gt=0, lt=6)
    comment: str

class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class UpdatePhoneNumberRequest(BaseModel):
    new_phone_number: str

class UpdateProfileRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str

    model_config = {"from_attributes": True}

class ListingImageResponse(BaseModel):
    id: int
    image_url: str

    model_config = {"from_attributes": True}

class ListingDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    address: str
    rooms: int
    floors: int
    property_type: str
    operation_type: str
    price: int

    images: List[ListingImageResponse] = []
    model_config = {"from_attributes": True}

class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str

    model_config = {"from_attributes": True}