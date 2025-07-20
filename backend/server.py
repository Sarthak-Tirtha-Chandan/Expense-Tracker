from fastapi import FastAPI,HTTPException
import db_helper
from datetime import date
from typing import List
from pydantic import BaseModel

class Expenses(BaseModel):
    amount : int
    category : str
    notes : str

class DateRange(BaseModel):
    start_date : date
    end_date : date

app = FastAPI()


@app.get("/expenses/{expense_date}",response_model= List[Expenses])
def get_expenses(expense_date : date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    return expenses


@app.post("/expenses/add")
def add_update_expenses(expense_date:date,expense:Expenses):
    db_helper.insert_expenses(expense_date,expense.amount,expense.category,expense.notes)
    return "Added successfully!!"


@app.post("/expenses/update")
def add_update_expenses(expense_date:date,expenses:List[Expenses]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expenses(expense_date,expense.amount,expense.category,expense.notes)
    return "Updated successfully!!"


@app.post("/analytics/")
def analytics(daterange: DateRange):
    
    try:
        expenses = db_helper.fetch_expenses_between(daterange.start_date, daterange.end_date)
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")

    if not expenses:
        raise HTTPException(status_code=404, detail="No data available in the selected date range.")

    total = sum(exp["amount"] for exp in expenses)
    transaction_count = len(expenses)
    num_days = (daterange.end_date - daterange.start_date).days + 1
    avg_daily = total / num_days if num_days > 0 else 0

    category_totals = {}
    for exp in expenses:
        cat = exp["category"]
        category_totals[cat] = category_totals.get(cat, 0) + exp["amount"]

    breakdown = []
    for cat, amt in category_totals.items():
        breakdown.append({
            "category": cat,
            "total": amt,
            "percentage": (amt / total * 100) if total > 0 else 0
        })

    top_expenses = sorted(expenses, key=lambda x: x["amount"], reverse=True)[:5]

    return {
        "total_expense": total,
        "transaction_count": transaction_count,
        "average_daily_spend": avg_daily,
        "category_breakdown": breakdown,
        "top_expenses": top_expenses
    }


@app.get("/monthly_summary/")
def get_analytics():
    monthly_summary = db_helper.fetch_monthly_expense_summary()
    if monthly_summary is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve monthly expense summary from the database.")

    return monthly_summary