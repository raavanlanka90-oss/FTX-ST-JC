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

    # Use index-based columns (avoid duplicate header issue)
    df.columns = range(len(df.columns))

    # Remove header row (row 6)
    df = df[1:].reset_index(drop=True)

    return df

df = load_data()

# ---------------------------
# PROCESS FUNCTION
# ---------------------------
def process_block(df, doer_i, planned_i, actual_i):
    try:
        temp = df[[
            0,  # JOB SERIES
            1,  # TIMESTAMP
            2,  # JC CARD NO
            3,  # BUYER
            4,  # ITEM CODE
            5,  # CUT QTY
            6,  # CUTTER
            doer_i,
            planned_i,
            actual_i
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

        # Clean values
        temp["PLANNED"] = temp["PLANNED"].astype(str).str.strip()
        temp["ACTUAL"] = temp["ACTUAL"].astype(str).str.strip()

        # Filter: Planned present & Actual blank
        temp = temp[
            (temp["PLANNED"] != "") &
            (temp["ACTUAL"] == "")
        ]

        return temp

    except:
        return pd.DataFrame()

# ---------------------------
# COLUMN BLOCKS (FIXED INDEX)
# ---------------------------
blocks = [
    (12, 13, 14),  # M N O
    (20, 21, 22),  # U V W
    (28, 29, 30),  # AC AD AE
    (36, 37, 38),  # AK AL AM
    (44, 45, 46),  # AS AT AU
    (52, 53, 54),  # BA BB BC
    (60, 61, 62),  # BI BJ BK
    (68, 69, 70),  # BQ BR BS
    (76, 77, 78),  # BY BZ CA
]

# ---------------------------
# PROCESS ALL BLOCKS
# ---------------------------
final_df = pd.DataFrame()

for doer_i, planned_i, actual_i in blocks:
    temp_df = process_block(df, doer_i, planned_i, actual_i)
    final_df = pd.concat([final_df, temp_df], ignore_index=True)

# ---------------------------
# UI
# ---------------------------
st.title("📊 ST JC FMS - Pending Work")

if final_df.empty:
    st.warning("⚠️ No pending data found")
else:
    st.success(f"✅ Total Pending Rows: {len(final_df)}")

    # Buyer filter
    buyer_list = sorted(final_df["BUYER"].dropna().unique().tolist())
    buyer_filter = st.selectbox("Filter by Buyer", ["All"] + buyer_list)

    if buyer_filter != "All":
        final_df = final_df[final_df["BUYER"] == buyer_filter]

    # Show table
    st.dataframe(final_df, use_container_width=True)

    # Download button
    csv = final_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download CSV",
        csv,
        "pending_data.csv",
        "text/csv"
    )
