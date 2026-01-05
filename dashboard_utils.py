import os
import pandas as pd
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config
from dotenv import load_dotenv

# --------------------------
# Setup
# --------------------------

load_dotenv()

# Ensure environment variable is set correctly
# Make sure DATABRICKS_HOST and DATABRICKS_TOKEN are also set in your environment/env file
if not os.getenv('DATABRICKS_WAREHOUSE_ID'):
    st.error("DATABRICKS_WAREHOUSE_ID must be set in app.yaml or .env")
    st.stop()

CATALOG = "business_intelligence_systems"
SCHEMA = "03_Gold_Retail_Banking"

def sqlQuery(query: str) -> pd.DataFrame:
    cfg = Config() # Pull environment variables for auth
    try:
        with sql.connect(
            server_hostname=cfg.host,
            http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
            credentials_provider=lambda: cfg.authenticate
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                # Fetch as Arrow for performance, then convert to Pandas
                return cursor.fetchall_arrow().to_pandas()
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

# --------------------------
# Data Loaders
# --------------------------

@st.cache_data(ttl=300)
def get_demographics_geo():
    """Fetches aggregated client demographics by state."""
    query = f"""
    SELECT *
    FROM {CATALOG}.{SCHEMA}.kpi_client_demographics_geographics
    """
    return sqlQuery(query)

@st.cache_data(ttl=300)
def get_card_distribution():
    """Aggregates card types dynamically since the source table is granular."""
    query = f"""
    SELECT 
        card_type, 
        COUNT(1) as card_count 
    FROM {CATALOG}.{SCHEMA}.kpi_client_card_profile
    GROUP BY card_type
    ORDER BY card_count DESC
    """
    return sqlQuery(query)

@st.cache_data(ttl=300)
def get_monthly_transactions():
    """Fetches monthly transaction trends."""
    query = f"""
    SELECT *
    FROM {CATALOG}.{SCHEMA}.kpi_completedtrans_monthly
    ORDER BY kpi_month
    """
    return sqlQuery(query)

@st.cache_data(ttl=300)
def get_crm_stats():
    """Fetches CRM call stats by hour."""
    query = f"""
    SELECT *
    FROM {CATALOG}.{SCHEMA}.crm_calls_by_hour
    ORDER BY hour
    """
    return sqlQuery(query)

@st.cache_data(ttl=300)
def get_complaints_stats():
    """Fetches complaints by product."""
    query = f"""
    SELECT *
    FROM {CATALOG}.{SCHEMA}.crm_complaints_by_product
    ORDER BY count DESC
    """
    return sqlQuery(query)
