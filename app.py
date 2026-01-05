import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(layout="wide", page_title="Business Intelligence Systems")

st.title("🏦 Business Intelligence Systems")
st.markdown("### Willkommen! Bitte wählen Sie einen Bereich:")

st.divider()

# Custom CSS for the large tiles
st.markdown("""
<style>
div.row-widget.stButton > button {
    width: 100%;
    height: 150px;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://img.icons8.com/color/480/groups.png", width=100)
    st.page_link("pages/01_Kunden_Dashboard.py", label="Kunden Dashboard", icon="👥", use_container_width=True)
    st.caption("Demographics & Card Portfolio")

with col2:
    st.image("https://img.icons8.com/color/480/transaction-list.png", width=100)
    st.page_link("pages/02_Transaktionen_Dashboard.py", label="Transaktionen Dashboard", icon="💳", use_container_width=True)
    st.caption("Financial Metrics & Trends")

with col3:
    st.image("https://img.icons8.com/color/480/customer-support.png", width=100)
    st.page_link("pages/03_CRM_Dashboard.py", label="CRM Dashboard", icon="📞", use_container_width=True)
    st.caption("Support & Complaints")

st.divider()

col4, col5, col6 = st.columns(3)

with col4:
    st.page_link("pages/03_SimpleChat.py", label="💬 Simple Chat", icon="💬", use_container_width=True)

with col5:
    st.page_link("pages/04_GenieAI.py", label="🧞 Genie AI", icon="🧞", use_container_width=True)

with col6:
    st.page_link("pages/05_Databricks_Dashboard.py", label="📊 Existing Dashboard", icon="📊", use_container_width=True)
