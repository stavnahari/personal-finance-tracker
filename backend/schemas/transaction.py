import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TransactionBase(BaseModel):
    date: datetime.date
    amount: float
    merchant: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    date: Optional[datetime.date] = None
    amount: Optional[float] = None
    merchant: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
