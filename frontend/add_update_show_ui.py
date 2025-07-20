import streamlit as st
from datetime import datetime,date
import requests
import pandas as pd


# API_URL = "http://localhost:8000"
API_URL = "https://expense-trackker.streamlit.app/"


def show():
    selected_date = st.date_input("Enter Date",date.today(),label_visibility="collapsed")
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        data = response.json()
    else:
        st.error("Failed to retrive data!!")
        data = []

    df = pd.DataFrame(data)

    st.table(df.to_dict(orient="records"))    


def add():
    with st.form("expense_form"):
        st.subheader("Add Expense")

        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Rent", "Food", "Shopping", "Entertainment", "Other"])
        note = st.text_input("Note")
        expense_date = st.date_input("Date", value=date.today())

        # Submit button
        submitted = st.form_submit_button("Submit")

    if submitted:
        params = {"expense_date": expense_date.strftime("%Y-%m-%d")}

        payload = {
            "amount": amount,
            "category": category,
            "notes": note
        }


        try:
            response = requests.post(f"{API_URL}/expenses/add", params=params, json=payload)
            if response.status_code == 200:
                st.success("Expense added successfully!")
            else:
                st.error(f"Failed to add expense")
        except Exception as e:
            st.error(f"Error: {e}")


def update():
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        # st.write(existing_expenses)
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form2"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []
        for i in range(len(existing_expenses)):
            
            amount = existing_expenses[i]['amount']
            category = existing_expenses[i]["category"]
            notes = existing_expenses[i]["notes"]
          
            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=float(amount), key=f"amount_{i}",
                                               label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category),
                                              key=f"category_{i}", label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Update Expenses")
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            params = {"expense_date": selected_date.strftime("%Y-%m-%d")}

            response = requests.post(f"{API_URL}/expenses/update",params=params, json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")