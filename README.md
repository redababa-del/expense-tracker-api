# Expense Tracker API

A REST API for managing expenses across multiple users: adding, viewing, updating, and deleting expenses, plus aggregated stats by category and by month.

Built with **FastAPI** and **PostgreSQL**.

## Database setup

1. Install PostgreSQL and create a database named `expenses` (via pgAdmin or the command line).
2. Create a `.env` file at the root of the project with the following content:

```
DB_HOST=localhost
DB_NAME=expenses
DB_USER=postgres
DB_PASSWORD=your_password
```

⚠️ This file should never be pushed to GitHub (it's already excluded via `.gitignore`).

## Installation

```bash
pip install fastapi uvicorn psycopg2-binary python-dotenv
```

## Running the project

1. Create the tables (only needs to be done once):
```bash
python database.py
```

2. Start the server:
```bash
python -m uvicorn main:app --reload
```

3. Open the interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Available routes

| Method | Route | Description |
|---|---|---|
| GET | `/expenses` | List all expenses |
| GET | `/expenses/{id}` | Get a specific expense by id |
| GET | `/expenses/user/{user_id}` | List expenses for a specific user |
| GET | `/expenses/user/{user_id}/total` | Get the total of all expenses for a user |
| POST | `/expenses` | Create a new expense |
| PUT | `/expenses/{id}` | Update an existing expense |
| DELETE | `/expenses/{id}` | Delete an expense |
| GET | `/stats/category` | Get total expenses by category |
| GET | `/stats/month` | Get total expenses by month |

## Project structure

```
expense-tracker/
├── main.py         # API routes
├── database.py      # Connection and SQL queries
├── models.py        # Pydantic models
├── .env              # Environment variables (not versioned)
└── .gitignore
```