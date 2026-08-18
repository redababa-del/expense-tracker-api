from pydantic import BaseModel

class Expense(BaseModel):
    amount: float
    category: str
    date: str
    user_id: int


class UserRegister(BaseModel):
    name : str
    email : str
    password : str


class LoginRequest(BaseModel):
    email: str
    password: str