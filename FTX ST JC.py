import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="ST JC FMS", layout="wide")

# ---------------------------
# GOOGLE SHEETS CONNECTION
# ---------------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# Open sheet
SHEET_ID = "1qS9TcpIxpaYg8x8xFepvWLQK87JdBzlNDXyM0SbN3rw"
SHEET_NAME = "ST JC FMS"

sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data(ttl=60)
def load_data():
    data = sheet.get("A6:HD")
    df = pd.DataFrame(data)

    # Set header
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    return df

df = load_data()

# ---------------------------
# SAFE COLUMN GETTER
# ---------------------------
def get_col(df, index):
    try:
        return df.columns[index]
    except:
        return None

# ---------------------------
# PROCESS BLOCK FUNCTION
# ---------------------------
def process_block(df, doer_col, planned_col, actual_col):
    if not doer_col or not planned_col or not actual_col:
        return pd.DataFrame()

    try:
        temp = df[[
            df.columns[0],   # JOB SERIES
            df.columns[1],   # TIMESTAMP
            df.columns[2],   # JC CARD NO
            df.columns[3],   # BUYER
            df.columns[4],   # ITEM CODE
            df.columns[5],   # CUT QTY
            df.columns[6],   # CUTTER
            doer_col,
            planned_col,
            actual_col
        ]].copy()

        temp.columns = [
            "JOB SERIES",
            "TIMESTAMP",
            "JC CARD NO",
            "BUYER",
            "ITEM CODE",
            "CUT QTY",
            "CUTTER",
            "DOER",
            "PLANNED",
            "ACTUAL"
        ]

        # Filter condition
        temp = temp[
            (temp["PLANNED"] != "") &
            ((temp["ACTUAL"] == "") | (temp["ACTUAL"].isna()))
        ]

        return temp

    except:
        return pd.DataFrame()

# ---------------------------
# COLUMN BLOCKS (INDEX BASED)
# ---------------------------
blocks = [
    (get_col(df, 12), get_col(df, 13), get_col(df, 14)),   # M N O
    (get_col(df, 20), get_col(df, 21), get_col(df, 22)),   # U V W
    (get_col(df, 28), get_col(df, 29), get_col(df, 30)),   # AC AD AE
    (get_col(df, 36), get_col(df, 37), get_col(df, 38)),   # AK AL AM
    (get_col(df, 44), get_col(df, 45), get_col(df, 46)),   # AS AT AU
    (get_col(df, 52), get_col(df, 53), get_col(df, 54)),   # BA BB BC
    (get_col(df, 60), get_col(df, 61), get_col(df, 62)),   # BI BJ BK
    (get_col(df, 68), get_col(df, 69), get_col(df, 70)),   # BQ BR BS
    (get_col(df, 76), get_col(df, 77), get_col(df, 78)),   # BY BZ CA
]

# ---------------------------
# PROCESS ALL BLOCKS
# ---------------------------
final_df = pd.DataFrame()

for doer, planned, actual in blocks:
    temp_df = process_block(df, doer, planned, actual)
    final_df = pd.concat([final_df, temp_df], ignore_index=True)

# ---------------------------
# UI
# ---------------------------
st.title("📊 ST JC FMS - Pending Work")

st.write("### 📌 Planned but Not Completed")

st.write(f"Total Pending Rows: **{len(final_df)}**")

# Optional filters
buyer_filter = st.selectbox(
    "Filter by Buyer",
    ["All"] + sorted(final_df["BUYER"].dropna().unique().tolist())
)

if buyer_filter != "All":
    final_df = final_df[final_df["BUYER"] == buyer_filter]

# Display
st.dataframe(final_df, use_container_width=True)

# Download option
csv = final_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇ Download CSV",
    csv,
    "pending_data.csv",
    "text/csv"
)
