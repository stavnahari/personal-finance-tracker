from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
