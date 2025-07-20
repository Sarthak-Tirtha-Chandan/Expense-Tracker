💸 Expense Management System
============================

A simple full-stack application for managing, analyzing, and visualizing your daily expenses. Built with **FastAPI** for the backend and **Streamlit** for the frontend.

🚀 Features
-----------
- View daily expenses
- Add new expenses
- Update existing expenses
- Analyze spending trends between two dates (category-wise breakdown, top expenses, charts)
- SQLite/MySQL support with clean separation of backend and frontend

🛠️ Tech Stack
--------------
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: MySQL
- **Charts**: Matplotlib
- **API Client**: requests

📦 Setup Instructions
---------------------

### Prerequisites
- Python 3.8 or higher
- pip

### Create Virtual Environment (Recommended)

**For Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```
> Ensure `backend/main.py` contains your FastAPI app and the path is correct.

### Run the Frontend (Streamlit)
```bash
streamlit run frontend/app.py
```
> Make sure the API URL in `frontend/app.py` matches your backend host (e.g., http://localhost:8000)

🔗 API Endpoints
----------------
- GET `/expenses/{date}` – Get expenses for a specific date
- POST `/expenses/add` – Add an expense for a date
- POST `/expenses/update` – Update all expenses for a date
- POST `/analytics/` – Analyze expenses in a date range

📊 Analytics Output
-------------------
When analyzing a date range, you will get:
- Total expenses
- Number of transactions
- Average daily spend
- Category-wise breakdown (total & percentage)
- Top 5 highest-expense entries
- Pie and bar charts using Matplotlib

📁 Project Structure
--------------------
```
expense-management/
├── backend/
│   ├── main.py
│   ├── db_helper.py
│   └── models.py
├── frontend/
│   └── app.py
├── requirements.txt
└── README.md
```
