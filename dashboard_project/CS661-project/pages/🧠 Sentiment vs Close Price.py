import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

df = pd.read_csv("C:/Users/Acer/CS661-project/dashboard_project/CS661-project/stock_data.csv")

# Add synthetic Date column (one row = one business day)
df.insert(0, "Date", pd.date_range(start="2020-01-01", periods=len(df), freq="B"))
df['Date'] = pd.to_datetime(df['Date'])



min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input(
    "📅 Select date range:",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date,
    key="daterange",
    help="Select start and end dates",
    format="YYYY-MM-DD"
)
if isinstance(date_range, list) or isinstance(date_range, tuple):
    start_date, end_date = date_range
else:
    st.error("Please select a valid date range.")
    st.stop()

# Filter the dataframe
filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))] 

st.subheader("🧠 Sentiment Score vs Closing Price")
fig_sentiment = px.scatter(filtered_df, x='Sentiment_Score', y='Close', trendline='ols',
                               title="Sentiment vs Close Price")
fig_sentiment.update_layout(
    paper_bgcolor='black',     # Outside chart (plot container) background
    plot_bgcolor='black',      # Inside chart (actual graph area)
    font=dict(color='white'),  # Text, tick labels
    xaxis=dict(
        color='white',
        gridcolor='gray',
        zerolinecolor='gray'
    ),
    yaxis=dict(
        color='white',
        gridcolor='gray',
        zerolinecolor='gray'
    ),
    title_font=dict(color='white')
)
st.plotly_chart(fig_sentiment, use_container_width=True)


st.markdown("""
<style>
/* 🔲 GLOBAL BACKGROUND + SIDEBAR */
.stApp, .block-container {
    background-color: black !important;
    color: white !important;
}
section[data-testid="stSidebar"] {
    background-color: #111 !important;
    color: white !important;
    border-right: 1px solid #444;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
.stTextInput input, .stDateInput input {
    background-color: #222 !important;
    color: white !important;
    border: 1px solid #444 !important;
}

/* 📅 CALENDAR STYLING */
div[data-baseweb="datepicker"] {
    background-color: #111 !important;
    color: white !important;
    border: 1px solid #444 !important;
}

/* Month/Year Header */
div[data-baseweb="datepicker"] div[role="presentation"] {
    background-color: #111 !important;
    color: white !important;
}

/* Month/Year buttons + arrows */
div[data-baseweb="datepicker"] svg,
div[data-baseweb="datepicker"] button {
    color: white !important;
    fill: white !important;
    background-color: transparent !important;
}

/* Weekday names (Su, Mo...) */
div[data-baseweb="calendar"] div[role="row"] div[role="columnheader"] {
    background-color: #111 !important;
    color: white !important;
}

/* Days */
div[data-baseweb="calendar"] div[role="gridcell"] {
    color: white !important;
    background-color: #111 !important;
}

/* Selected Day (Red circle) */
div[data-baseweb="calendar"] div[aria-selected="true"] {
    background-color: #e74c3c !important;
    color: white !important;
    border-radius: 50%;
}

/* Hover Day */
div[data-baseweb="calendar"] div[role="option"]:hover {
    background-color: #333 !important;
}

/* Disabled buttons (non-clickable nav arrows) */
div[data-baseweb="calendar"] button:disabled {
    color: #777 !important;
}
</style>
""", unsafe_allow_html=True)


