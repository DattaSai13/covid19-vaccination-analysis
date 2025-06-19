# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page title & layout
st.set_page_config(
    page_title="COVID-19 Vaccination Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("country_vaccinations.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ---- SIDEBAR ----
st.sidebar.title("Filters")
selected_country = st.sidebar.selectbox(
    "Select Country", 
    df['country'].unique()
)

# ---- MAIN DASHBOARD ----
st.title("🌍 COVID-19 Vaccination Dashboard")
st.markdown("""
    *Data Source: [Kaggle](https://www.kaggle.com/gpreda/covid-world-vaccination-progress)*
""")

# Key Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Countries", len(df['country'].unique()))
with col2:
    st.metric("Max Vaccinations", f"{df['total_vaccinations'].max():,}")
with col3:
    st.metric("Avg Daily Doses", f"{df['daily_vaccinations'].mean():,.0f}")

# Charts
tab1, tab2 = st.tabs(["Country Trends", "Global Comparison"])

with tab1:
    st.header(f"Vaccination Progress: {selected_country}")
    country_data = df[df['country'] == selected_country]
    st.line_chart(country_data, x="date", y="total_vaccinations")

with tab2:
    st.header("Top 10 Vaccinated Countries")
    top_10 = df.groupby('country')['total_vaccinations'].max().nlargest(10)
    st.bar_chart(top_10)

# Data Table
st.header("Raw Data")
st.dataframe(df, height=300)