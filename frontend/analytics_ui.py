import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime,date
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics():
    st.subheader("Expense Analytics")

    # Date Range Selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 1, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 12, 31))

    if st.button("Analyze"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        try:
            response = requests.post(f"{API_URL}/analytics/", json=payload)

            if response.status_code == 200:
                analytics_data = response.json()

                if not analytics_data:
                    st.warning("No expenses found in the given range.")
                else:
                    # Display summary
                    st.metric("Total Expense", f"₹{analytics_data['total_expense']:.2f}")
                    st.metric("Transactions", analytics_data['transaction_count'])
                    st.metric("Average Daily Spend", f"₹{analytics_data['average_daily_spend']:.2f}")

                    # Category Breakdown
                    breakdown_df = pd.DataFrame(analytics_data["category_breakdown"])
                    breakdown_df = breakdown_df.sort_values(by="total", ascending=False).head(5)
                    st.dataframe(breakdown_df)

                    # Pie Chart
                    fig1, ax1 = plt.subplots()
                    ax1.pie(
                        breakdown_df['total'],
                        labels=breakdown_df['category'],
                        autopct='%1.1f%%',
                        startangle=90,
                        wedgeprops={'edgecolor': 'white'}
                    )
                    ax1.set_title("Top 5 Spending Distribution by Category")
                    st.pyplot(fig1)

                    # Bar Chart
                    fig2, ax2 = plt.subplots()
                    ax2.bar(breakdown_df['category'], breakdown_df['total'], color='skyblue')
                    ax2.set_title("Top 5 Total Spending per Category")
                    ax2.set_xlabel("Category")
                    ax2.set_ylabel("Total Expense")
                    st.pyplot(fig2)

                    # Top 5 Expenses
                    st.markdown("### Top 5 Highest Expenses")
                    top_df = pd.DataFrame(analytics_data["top_expenses"])
                    st.table(top_df)

            else:
                st.error("Failed to fetch analytics data.")
        except Exception as e:
            st.error(f"Error: {e}")
