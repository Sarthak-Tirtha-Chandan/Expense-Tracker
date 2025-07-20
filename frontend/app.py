import streamlit as st
from datetime import datetime,date
import requests
import pandas as pd
from add_update_show_ui import show,add,update
from analytics_ui import analytics
from analytics_by_months import analytics_months_tab

API_URL = "http://localhost:8000"

st.title("Expense Management System")

tab1,tab2,tab3,tab4,tab5 = st.tabs(["Show","Add","Update","Analytics By Category","Analytics By Month"])

with tab1:
    show()

with tab2: 
    add()

with tab3:
    update()

with tab4:
    analytics()

with tab5:
    analytics_months_tab()