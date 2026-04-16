from pydantic import BaseModel


class VMCreate(BaseModel):
    name: str
    status: str
    cpu: int
    memory: int
    os: str
    region: str
    owner: str


class UserCreate(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str