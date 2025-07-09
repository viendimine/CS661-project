import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv("C:/Users/Acer/CS661-project/dashboard_project/CS661-project/stock_data.csv")

# Set page title
st.set_page_config(page_title="Macroeconomic Dashboard", layout="wide")
st.title("📊 Interactive Macro-Economic Dashboard")

options = [
    "📈 Closing Price Line Chart",
    "📉 RSI Line Chart",
    "📊 MACD Line Chart",
    "🧠 Sentiment vs Close Price",
    "🔍 Correlation Heatmap"
]

# Date filter
st.sidebar.header("📂 Select a Visualization")
selected_option = st.sidebar.radio("Choose a chart to display:", options)

if selected_option == "📈 Closing Price Line Chart":
    st.subheader("📈 Closing Price Over Time")
    st.plotly_chart(px.line(df, y='Close', title="Closing Price Over Time"), use_container_width=True)

elif selected_option == "📉 RSI Line Chart":
    st.subheader("📉 RSI Indicator (Relative Strength Index)")
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(y=df['RSI'], mode='lines', name='RSI', line=dict(color='orange')))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
    fig_rsi.update_layout(title="RSI Line Chart")
    st.plotly_chart(fig_rsi, use_container_width=True)

elif selected_option == "📊 MACD Line Chart":
    st.subheader("📊 MACD Indicator")
    st.plotly_chart(px.line(df, y='MACD', title="MACD Over Time"), use_container_width=True)

elif selected_option == "🧠 Sentiment vs Close Price":
    st.subheader("🧠 Sentiment Score vs Closing Price")
    fig_sentiment = px.scatter(df, x='Sentiment_Score', y='Close', trendline='ols',
                               title="Sentiment vs Close Price")
    st.plotly_chart(fig_sentiment, use_container_width=True)

elif selected_option == "🔍 Correlation Heatmap":
    st.subheader("🔍 Correlation Heatmap")
    corr = df.corr(numeric_only=True)
    fig_corr = px.imshow(corr, title="Feature Correlation Matrix")
    st.plotly_chart(fig_corr, use_container_width=True)