import streamlit as st
import plotly.express as px
from dashboard_utils import get_demographics_geo, get_card_distribution

st.set_page_config(layout="wide", page_title="Kunden Dashboard")

st.title("👥 Kunden & Accounts Dashboard")
st.markdown("Overview of Client Demographics based on Gold Layer data.")

# Load Data
df_demo = get_demographics_geo().copy()
df_cards = get_card_distribution().copy()

# Sidebar Filters
st.sidebar.title("Filters")
all_states = sorted(df_demo["state_name"].unique())
selected_states = st.sidebar.multiselect("Select States", all_states, default=all_states[:5])

# Apply Filter
if selected_states:
    df_demo_filtered = df_demo[df_demo["state_name"].isin(selected_states)]
else:
    df_demo_filtered = df_demo

st.subheader("Client Demographics & Card Portfolio")

# Top Level Metrics
total_clients_in_view = df_demo_filtered["client_count"].sum()
st.metric(label="Total Clients (Selected States)", value=f"{total_clients_in_view:,}")

col1, col2 = st.columns(2)

with col1:
    # Age Group Distribution
    fig_age = px.bar(
        df_demo_filtered.groupby("age_group")["client_count"].sum().reset_index(),
        x="age_group",
        y="client_count",
        title="Client Distribution by Age Group",
        color_discrete_sequence=["#3366CC"]
    )
    st.plotly_chart(fig_age, use_container_width=True)
    
with col2:
    # Gender Distribution
    fig_sex = px.pie(
        df_demo_filtered.groupby("sex")["client_count"].sum().reset_index(),
        values="client_count",
        names="sex",
        title="Client Distribution by Gender",
        hole=0.4
    )
    st.plotly_chart(fig_sex, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    # Geographic Map (using State Names)
    fig_state = px.bar(
        df_demo_filtered.groupby("state_name")["client_count"].sum().reset_index().sort_values("client_count", ascending=False).head(10),
        x="client_count",
        y="state_name",
        orientation='h',
        title="Top States by Client Count",
        color="client_count",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_state, use_container_width=True)

with col4:
    # Card Types
    fig_cards = px.bar(
        df_cards,
        x="card_type",
        y="card_count",
        title="Credit Card Portfolio Mix",
        color="card_type",
        text_auto=True
    )
    st.plotly_chart(fig_cards, use_container_width=True)
