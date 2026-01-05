import streamlit as st
import plotly.express as px
from dashboard_utils import get_crm_stats, get_complaints_stats

st.set_page_config(layout="wide", page_title="CRM Dashboard")

st.title("📞 CRM & Support Dashboard")
st.markdown("Customer Support Analysis.")

# Load Data
df_crm_calls = get_crm_stats().copy()
df_complaints = get_complaints_stats().copy()

st.subheader("Customer Support Metrics")

c1, c2 = st.columns(2)

with c1:
    # Calls by Hour
    fig_calls = px.bar(
        df_crm_calls,
        x="hour",
        y="count",
        title="Call Center Volume by Hour of Day",
        labels={"hour": "Hour of Day (24h)", "count": "Number of Calls"},
        color="average_time", # Color by duration
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_calls, use_container_width=True)
    st.caption("Bar color indicates average call duration (seconds).")
    
with c2:
    # Complaints by Product
    fig_comp = px.bar(
        df_complaints,
        y="product",
        x="count",
        orientation='h',
        title="Complaints by Product Category",
        color="count",
        color_continuous_scale="Reds"
    )
    fig_comp.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_comp, use_container_width=True)

# Detailed CRM Data
with st.expander("🔍 View CRM Source Data"):
    st.write("Calls by Priority")
    st.dataframe(df_crm_calls, use_container_width=True)
