from pydantic import BaseModel

class Expense(BaseModel):
    amount: float
    category: str
    date: str
    user_id: int