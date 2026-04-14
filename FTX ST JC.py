import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# GOOGLE SHEETS CONNECTION
# -----------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
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

# Convert to DataFrame
df = pd.DataFrame(data)

# Header is row 6 → index 5
df.columns = df.iloc[5]
df = df.iloc[6:].reset_index(drop=True)

# -----------------------------
# FUNCTION TO EXTRACT & STANDARDIZE
# -----------------------------
def extract_block(df, col_map):
    temp = df[col_map].copy()
    temp.columns = [
        "A", "B", "C", "D", "E", "F", "G",
        "Ref", "DateTime", "Blank"
    ]
    return temp

# -----------------------------
# COLUMN MAPPINGS
# -----------------------------
block1 = extract_block(df, ["A","B","C","D","E","F","G","M","N","O"])
block2 = extract_block(df, ["A","B","C","D","E","F","G","U","V","W"])
block3 = extract_block(df, ["A","B","C","D","E","F","G","AC","AD","AE"])

# -----------------------------
# COMBINE (ROW BIND)
# -----------------------------
final_df = pd.concat([block1, block2, block3], ignore_index=True)

# Optional: remove empty rows (where Ref is blank)
final_df = final_df[final_df["Ref"] != ""]

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("📊 Google Sheet Combined View")

st.dataframe(final_df, use_container_width=True)