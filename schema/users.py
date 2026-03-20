from pydantic import BaseModel, Field,ConfigDict


class UserInfo(BaseModel):
    email: str
    password: str