import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("C:/Users/Acer/CS661-project/dashboard_project/macro_data_interpolated.csv")
df['Date'] = pd.to_datetime(df['Unnamed: 0'])

# Set page title
st.set_page_config(page_title="Macroeconomic Dashboard", layout="wide")
st.title("📊 Interactive Macro-Economic Dashboard")

# Date filter
st.sidebar.header("📅 Filter by Date")
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
start_date = st.sidebar.date_input("Start date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End date", max_date, min_value=min_date, max_value=max_date)

# Filter data
filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

if filtered_df.empty:
    st.warning("⚠️ No data available for the selected date range.")
else:
    # Layout columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 GDP Over Time")
        fig_gdp = px.line(filtered_df, x='Date', y='GDP', title='GDP Over Time')
        st.plotly_chart(fig_gdp, use_container_width=True)

    with col2:
        st.subheader("📉 Unemployment Rate Over Time")
        fig_unemp = px.line(filtered_df, x='Date', y='Unemployment Rate', title='Unemployment Rate Over Time')
        st.plotly_chart(fig_unemp, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📈 CPI Over Time")
        fig_cpi = px.line(filtered_df, x='Date', y='CPI', title='CPI Over Time')
        st.plotly_chart(fig_cpi, use_container_width=True)

    with col4:
        st.subheader("📊 Fed Funds Rate Over Time")
        fig_fed = px.line(filtered_df, x='Date', y='Fed Funds Rate', title='Fed Funds Rate Over Time')
        st.plotly_chart(fig_fed, use_container_width=True)

    # Scatter plot: CPI vs Fed Funds Rate
    st.subheader("🟠 CPI vs Fed Funds Rate (Scatter)")
    scatter_fig = px.scatter(filtered_df, x='CPI', y='Fed Funds Rate', trendline='ols')
    st.plotly_chart(scatter_fig, use_container_width=True)
