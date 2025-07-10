import streamlit as st
import pandas as pd
import os
import mplfinance as mpf
import matplotlib.pyplot as plt

custom_style = mpf.make_mpf_style(
    base_mpf_style='charles',
    marketcolors=mpf.make_marketcolors(
        up='lime',      # green for up candles
        down='red',     # red for down candles
        wick='white',
        edge='inherit',
        volume='inherit'
    ),
    facecolor='black',      # chart background
    edgecolor='white',      # axis edge
    figcolor='black',       # figure background
    gridcolor='white',
    rc={
        'axes.labelcolor': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'axes.edgecolor': 'white',
        'axes.titlecolor': 'white'
    }
)


# --- CONFIGURATION ---
folder_path = 'C:/Users/Acer/CS661-project/dashboard_project/CS661-project/Stocks'

st.title("📊 US Stock Candlestick Chart ")

# --- File Selection ---
stock_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
if not stock_files:
    st.error("No .txt files found in the specified folder.")
    st.stop()

selected_file = st.selectbox("Select a stock file:", stock_files)
file_path = os.path.join(folder_path, selected_file)

# --- Read and Clean File ---
try:
    df = pd.read_csv(file_path)

    if df.empty or 'Date' not in df.columns:
        st.error("❌ Invalid or empty file selected.")
        st.stop()

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.columns = [col.strip().capitalize() for col in df.columns]

    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ File missing required OHLCV columns: {required_cols}")
        st.stop()

    # --- Show Data Table (Optional) ---
    with st.expander("🔍 Show Raw Data"):
        st.dataframe(df.tail(10))

    # --- Plot Candlestick (last 100 rows) ---
    st.subheader("📈 Candlestick Chart (last 100 days)")

    days = st.slider("Please select the days range" , 5, 100)
    fig, axes = mpf.plot(df[-days:], 
                     type='candle',
                     mav=(20, 50),
                     volume=True,
                     style=custom_style,
                     returnfig=True,
                     warn_too_much_data=len(df)+1)

    st.pyplot(fig)
    



    st.markdown("""
<style>
/* 🔲 GLOBAL BACKGROUND + SIDEBAR */
                
header[data-testid="stHeader"] {
    background-color: black !important;
}

.block-container {
    padding-top: 3rem !important;
}
                
.stApp, .block-container {
    background-color: black !important;
    color: white !important;
}
label {
        color: white !important;
    }

    /* Change the background and text color of the selectbox input area */
    div[data-baseweb="select"] > div {
        background-color: black !important;
        color: white !important;
    }

    /* Style the dropdown options */
    div[data-baseweb="select"] div[role="option"] {
        background-color: black !important;
        color: white !important;
    }
                
.sttitle {
        font-size:100px;
}
.stSelectbox label, .stSelectbox div, .stSelectbox span {
            color: white !important;
}
.stexpander label,.stexpander div ,.stexpander span {
            color: black !important;
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


except pd.errors.EmptyDataError:
    st.error("❌ Empty file.")
except Exception as e:
    st.error(f"⚠️ Error reading file: {e}")
