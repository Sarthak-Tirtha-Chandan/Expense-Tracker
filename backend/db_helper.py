import mysql.connector
from contextlib import contextmanager
from logger_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sarthak",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)

    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()




def fetch_all_records():
    logger.info("All expenses fetched")
    with get_db_cursor() as cursor:
        cursor.execute("select * from expenses")
        expenses = cursor.fetchall()
        return expenses


def fetch_expenses_for_date(expense_date):
    logger.info(f"Expenses of date : {expense_date} fetched")
    with get_db_cursor() as cursor:
        cursor.execute("select * from expenses where expense_date = %s",(expense_date,))
        expenses = cursor.fetchall()
        return expenses



def insert_expenses(expense_date,amount,category,note):
    logger.info(f"Expenses inserted on date : {expense_date} with amount:{amount} , category: {category} , note: {note}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",(expense_date,amount,category,note))
        expenses = cursor.fetchall()
        return expenses



def delete_expenses_for_date(expense_date):
    logger.info(f'Expenses of date : {expense_date} deleted')
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))



def fetch_expenses_between(start_date, end_date):
    logger.info(f"Fetching expenses between {start_date} and {end_date}")
    
    with get_db_cursor() as cursor:
        query = """
            SELECT amount, category, notes, expense_date AS date
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
        """
        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()
        logger.info(f"Fetched {len(rows)} rows")
        return [dict(row) for row in rows]


def fetch_expense_summary(start_date,end_date):
    logger.info(f"Summary fetched between {start_date} and {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
                select category , SUM(amount) as total
                from expenses
                where expense_date between %s and %s
                group by category
            ''',(start_date,end_date)
        )

        data = cursor.fetchall()
        return data
    
def fetch_monthly_expense_summary():
    logger.info(f"fetch_expense_summary_by_months")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT month(expense_date) as expense_month, 
               monthname(expense_date) as month_name,
               sum(amount) as total FROM expenses
               GROUP BY expense_month, month_name;
            '''
        )
        data = cursor.fetchall()
        return data
    

# if __name__ == "__main__":
#     print(fetch_expense_summary("2025-07-20","2025-07-20"))