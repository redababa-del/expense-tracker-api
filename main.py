from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from models import Expense, UserRegister, LoginRequest
from database import create_expense, get_all_expenses, get_expense_by_id, get_expenses_by_user
from database import update_expense, delete_expense, total_expenses_by_user
from database import add_user, get_user_by_email
from auth import hash_password, verify_password, create_access_token, verify_token
from fastapi.security import HTTPBearer



app = FastAPI()



oauth2_scheme = HTTPBearer()

def get_current_user_id(credentials = Depends(oauth2_scheme)):
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["user_id"]






@app.get("/expenses")
def list_expenses():
    return get_all_expenses()


@app.get("/expenses/{id}")
def get_expense(id: int, current_user_id: int = Depends(get_current_user_id)):
    expense = get_expense_by_id(id)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense[4] != current_user_id:  # index 4 = user_id, vérifie l'ordre chez toi
        raise HTTPException(status_code=403, detail="Access forbidden")

    return expense


@app.get("/expenses/user/{user_id}")
def list_expense_by_user_id(user_id: int, current_user_id: int = Depends(get_current_user_id)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    expenses = get_expenses_by_user(user_id)
    return expenses


@app.get("/expenses/user/{user_id}/total")
def get_user_total(user_id: int, current_user_id: int = Depends(get_current_user_id)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"total": total_expenses_by_user(user_id)}



@app.post("/expenses")
def add_expense(expense : Expense):
    create_expense(expense.amount, expense.category, expense.date, expense.user_id)
    return {"message": "Expense created"}



@app.put("/expenses/{id}")
def update_expense(id: int, updated_expense: Expense, current_user_id: int = Depends(get_current_user_id)):
    expense = get_expense_by_id(id)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense[4] != current_user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    update_expense(id, updated_expense.montant, updated_expense.categorie, updated_expense.date, updated_expense.user_id)
    return {"message": "Expense updated"}


@app.delete("/expenses/{id}")
def delete_expense(id: int, current_user_id: int = Depends(get_current_user_id)):
    expense = get_expense_by_id(id)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense[4] != current_user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    delete_expense(id)
    return {"message": "Expense deleted"}


from database import total_by_category, total_by_month


@app.get("/stats/category")
def expenses_by_category():
    return total_by_category()


@app.get("/stats/month")
def expenses_by_month():
    return total_by_month()


#auth :
from database import add_user, get_user_by_email
from models import UserRegister, LoginRequest, Expense
from auth import hash_password, verify_password, create_access_token


@app.post("/register")
def register(user: UserRegister):
    password_hash = hash_password(user.password)
    add_user(user.name, user.email, password_hash)
    return {"message": "User created"}


@app.post("/login")
def login(credentials: LoginRequest):
    user = get_user_by_email(credentials.email)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    stored_password_hash = user[3]

    if not verify_password(credentials.password, stored_password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"user_id": user[0]})
    return {"access_token": token, "token_type": "bearer"}