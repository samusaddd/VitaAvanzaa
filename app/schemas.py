
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict

# ==== Auth & User ====

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

# ==== DVI ====

class DVICalcInput(BaseModel):
    # keep generic for now – you can adapt to your questionnaire later
    financial_stability: int = Field(ge=0, le=10)
    income_outlook: int = Field(ge=0, le=10)
    career_clarity: int = Field(ge=0, le=10)
    skills_level: int = Field(ge=0, le=10)
    wellbeing_status: int = Field(ge=0, le=10)
    social_integration: int = Field(ge=0, le=10)

class DVIDimensionScores(BaseModel):
    financial: float
    career: float
    wellbeing: float
    integration: float
    skills: float

class DVIProfileRead(BaseModel):
    id: int
    overall_score: float
    dimensions: DVIDimensionScores
    created_at: datetime

    class Config:
        orm_mode = True

# ==== Opportunities ====

class OpportunityBase(BaseModel):
    title: str
    category: Optional[str] = None
    provider: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    country: Optional[str] = None
    score_match: float = 0.0

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityRead(OpportunityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# ==== Feed ====

class FeedPostBase(BaseModel):
    title: str
    content: str
    tag: Optional[str] = None

class FeedPostCreate(FeedPostBase):
    pass

class FeedPostRead(FeedPostBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

# ==== Mitra ====

class ChatMessage(BaseModel):
    role: str
    content: str

class MitraChatRequest(BaseModel):
    messages: List[ChatMessage]

class MitraChatResponse(BaseModel):
    reply: str
