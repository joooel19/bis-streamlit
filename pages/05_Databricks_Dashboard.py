import streamlit as st

st.set_page_config(layout="wide", page_title="Existing Dashboard")

st.title("📊 Existing Databricks Dashboard")

# Embed the dashboard using an iframe
st.markdown("""
<iframe
  src="https://dbc-13758abc-6acf.cloud.databricks.com/embed/dashboardsv3/01f0e8b2f49f14d69fb7315f7ad74700?o=1632171080722505"
  width="100%"
  height="800"
  frameborder="0">
</iframe>
""", unsafe_allow_html=True)
