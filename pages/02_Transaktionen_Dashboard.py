import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard_utils import get_monthly_transactions

st.set_page_config(layout="wide", page_title="Transaktionen Dashboard")

st.title("💳 Transaktionen Dashboard")
st.markdown("Financial Performance Over Time.")

# Load Data
df_trans = get_monthly_transactions().copy()

# Preprocess
df_trans["kpi_month"] = pd.to_datetime(df_trans["kpi_month"])

st.subheader("Financial Trends")

# Metrics
latest_month = df_trans["kpi_month"].max()
latest_data = df_trans[df_trans["kpi_month"] == latest_month].iloc[0]

m1, m2, m3 = st.columns(3)
m1.metric("Latest Monthly Volume", f"${latest_data['total_amount']:,.0f}")
m2.metric("Latest Tx Count", f"{latest_data['transaction_count']:,}")
m3.metric("Avg Ending Balance", f"${latest_data['average_ending_balance']:,.0f}")

# Dual Axis Chart: Amount vs Count
fig_trend = go.Figure()

fig_trend.add_trace(go.Bar(
    x=df_trans["kpi_month"],
    y=df_trans["total_amount"],
    name="Total Amount",
    marker_color='rgb(26, 118, 255)',
    opacity=0.6
))

fig_trend.add_trace(go.Scatter(
    x=df_trans["kpi_month"],
    y=df_trans["transaction_count"],
    name="Transaction Count",
    yaxis='y2',
    mode='lines+markers',
    line=dict(color='rgb(255, 65, 54)', width=3)
))

fig_trend.update_layout(
    title="Monthly Transaction Volume vs Count",
    xaxis_title="Month",
    yaxis=dict(title="Total Amount ($)"),
    yaxis2=dict(title="Count", overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.99)
)
st.plotly_chart(fig_trend, use_container_width=True)

# Balance Trend
fig_bal = px.line(
    df_trans,
    x="kpi_month",
    y="average_ending_balance",
    title="Average Account Balance Trends",
    markers=True
)
st.plotly_chart(fig_bal, use_container_width=True)

with st.expander("🔍 View Transaction Data"):
    st.dataframe(df_trans.style.format({"total_amount": "${:,.2f}", "average_ending_balance": "${:,.2f}"}), use_container_width=True)
