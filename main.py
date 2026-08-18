from fastapi import FastAPI, HTTPException
from models import Expense
from database import create_expense
from database import get_all_expenses, get_expense_by_id, get_expenses_by_user
from database import update_expense, delete_expense
from database import total_expenses_by_user

app = FastAPI()



@app.get("/expenses")
def list_expenses():
    return get_all_expenses()


@app.get("/expenses/{id}")
def list_expense_id(id : int):
    expense = get_expense_by_id(id)

    if expense is None:
        raise HTTPException(status_code=404, detail="expense not found")

    return expense


@app.get("/expenses/user/{user_id}")
def list_expense_by_user_id(user_id: int):
    expenses = get_expenses_by_user(user_id)
    return expenses


@app.get("/expenses/user/{user_id}/total")
def total_expenses_user_id(user_id: int):
    total = total_expenses_by_user(user_id)
    return {"user_id": user_id, "total": total}



@app.post("/expenses")
def add_expense(expense : Expense):
    create_expense(expense.amount, expense.category, expense.date, expense.user_id)
    return {"message": "Expense created"}



@app.put("/expenses/{id}")
def update_expense_endpoint(id: int, expense_update: Expense):
    expense = get_expense_by_id(id)
    
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    update_expense(id, expense_update.amount, expense_update.category, expense_update.date, expense_update.user_id)
    
    return {"message": "Expense updated"}


@app.delete("/expenses/{id}")
def delete_expense_endpoint(id: int):
    expense = get_expense_by_id(id)
    
    if expense is None:
        raise HTTPException(status_code=404, detail="expense not found")
    
    delete_expense(id)
    
    return {"message": "expense deleted"}


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
from auth import hash_password, verify_password


@app.post("/register")
def register(user: UserRegister):
    password_hash = hash_password(user.password)
    add_user(user.name, user.email, password_hash)
    return {"message": "Utilisateur créé"}


@app.post("/login")
def login(credentials: LoginRequest):
    user = get_user_by_email(credentials.email)

    if user is None:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    stored_password_hash = user[3]  # à ajuster selon l'ordre de tes colonnes

    if not verify_password(credentials.password, stored_password_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    return {"message": "Connexion réussie"}