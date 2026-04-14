import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="FTX ST JC", layout="wide")

st.title("📊 FTX ST JC - Combined View")

# -----------------------------
# GOOGLE SHEETS CONNECTION
# -----------------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# -----------------------------
# OPEN SHEET
# -----------------------------
SHEET_ID = "1qS9TcpIxpaYg8x8xFepvWLQK87JdBzlNDXyM0SbN3rw"
SHEET_NAME = "ST JC FMS"

sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# -----------------------------
# LOAD DATA
# -----------------------------
data = sheet.get_all_values()

df = pd.DataFrame(data)

# Header row (row 6 → index 5)
df.columns = df.iloc[5]
df = df.iloc[6:].reset_index(drop=True)

# -----------------------------
# DEBUG (VERY IMPORTANT)
# -----------------------------
st.write("Detected Columns:", list(df.columns))

# -----------------------------
# FUNCTION USING INDEX POSITION
# -----------------------------
def extract_block_by_index(df, indices):
    temp = df.iloc[:, indices].copy()
    temp.columns = [
        "A", "B", "C", "D", "E", "F", "G",
        "Ref", "DateTime", "Blank"
    ]
    return temp

try:
    # Column index mapping (0-based)
    block1 = extract_block_by_index(df, [0,1,2,3,4,5,6,12,13,14])   # A-G + M N O
    block2 = extract_block_by_index(df, [0,1,2,3,4,5,6,20,21,22])   # A-G + U V W
    block3 = extract_block_by_index(df, [0,1,2,3,4,5,6,28,29,30])   # A-G + AC AD AE

    # Combine
    final_df = pd.concat([block1, block2, block3], ignore_index=True)

    # Remove empty rows
    final_df = final_df[final_df["Ref"] != ""]

    # Convert DateTime
    final_df["DateTime"] = pd.to_datetime(final_df["DateTime"], errors="coerce")

    # -----------------------------
    # DISPLAY
    # -----------------------------
    st.success("✅ Data Loaded Successfully")

    st.dataframe(final_df, use_container_width=True)

except Exception as e:
    st.error("❌ Error in processing data")
    st.write(e)
