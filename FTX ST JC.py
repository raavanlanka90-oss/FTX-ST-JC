import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------------------
# GOOGLE SHEET CONNECTION
# ---------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

# Open Sheet
sheet_id = "1qS9TcpIxpaYg8x8xFepvWLQK87JdBzlNDXyM0SbN3rw"
sheet = client.open_by_key(sheet_id).worksheet("ST JC FMS")

# ---------------------------
# LOAD DATA
# ---------------------------
data = sheet.get("A6:HD")

df = pd.DataFrame(data)

# Set header (Row 6)
df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)

# ---------------------------
# HELPER FUNCTION
# ---------------------------
def process_block(df, doer_col, planned_col, actual_col):
    temp = df[[
        df.columns[0],   # JOB SERIES (A)
        df.columns[2],   # JC CARD NO (C)
        df.columns[3],   # BUYER (D)
        df.columns[4],   # ITEM CODE (E)
        df.columns[5],   # CUT QTY (F)
        df.columns[6],   # CUTTER (G)
        doer_col,
        planned_col,
        actual_col
    ]].copy()

    temp.columns = [
        "JOB SERIES",
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


# ---------------------------
# COLUMN BLOCKS
# ---------------------------
blocks = [
    ("DOER", "PLANNED", "ACTUAL"),  # M N O (already header names)
    (df.columns[20], df.columns[21], df.columns[22]),  # U V W
    (df.columns[28], df.columns[29], df.columns[30]),  # AC AD AE
    (df.columns[36], df.columns[37], df.columns[38]),  # AK AL AM
    (df.columns[44], df.columns[45], df.columns[46]),  # AS AT AU
    (df.columns[52], df.columns[53], df.columns[54]),  # BA BB BC
    (df.columns[60], df.columns[61], df.columns[62]),  # BI BJ BK
    (df.columns[68], df.columns[69], df.columns[70]),  # BQ BR BS
    (df.columns[76], df.columns[77], df.columns[78]),  # BY BZ CA
]

# ---------------------------
# PROCESS ALL BLOCKS
# ---------------------------
final_df = pd.DataFrame()

for block in blocks:
    try:
        temp_df = process_block(df, block[0], block[1], block[2])
        final_df = pd.concat([final_df, temp_df], ignore_index=True)
    except:
        pass

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.title("📊 ST JC FMS - Pending Work")

st.write("### Filtered Data (Planned but Not Actual)")

st.dataframe(final_df, use_container_width=True)
