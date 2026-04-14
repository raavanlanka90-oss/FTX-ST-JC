# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials

# # ---------------------------
# # PAGE CONFIG
# # ---------------------------
# st.set_page_config(page_title="ST JC FMS", layout="wide")

# # ---------------------------
# # GOOGLE SHEETS CONNECTION
# # ---------------------------
# scope = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]

# creds = Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"],
#     scopes=scope
# )

# client = gspread.authorize(creds)

# SHEET_ID = "1qS9TcpIxpaYg8x8xFepvWLQK87JdBzlNDXyM0SbN3rw"
# SHEET_NAME = "ST JC FMS"

# sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# # ---------------------------
# # LOAD DATA
# # ---------------------------
# @st.cache_data(ttl=60)
# def load_data():
#     data = sheet.get("A6:HD")
#     df = pd.DataFrame(data)

#     # Use index-based columns (avoid duplicate header issue)
#     df.columns = range(len(df.columns))

#     # Remove header row (row 6)
#     df = df[1:].reset_index(drop=True)

#     return df

# df = load_data()

# # ---------------------------
# # PROCESS FUNCTION
# # ---------------------------
# def process_block(df, doer_i, planned_i, actual_i):
#     try:
#         temp = df[[
#             0,  # JOB SERIES
#             1,  # TIMESTAMP
#             2,  # JC CARD NO
#             3,  # BUYER
#             4,  # ITEM CODE
#             5,  # CUT QTY
#             6,  # CUTTER
#             doer_i,
#             planned_i,
#             actual_i
#         ]].copy()

#         temp.columns = [
#             "JOB SERIES",
#             "TIMESTAMP",
#             "JC CARD NO",
#             "BUYER",
#             "ITEM CODE",
#             "CUT QTY",
#             "CUTTER",
#             "DOER",
#             "PLANNED",
#             "ACTUAL"
#         ]

#         # Clean values
#         temp["PLANNED"] = temp["PLANNED"].astype(str).str.strip()
#         temp["ACTUAL"] = temp["ACTUAL"].astype(str).str.strip()

#         # Filter: Planned present & Actual blank
#         temp = temp[
#             (temp["PLANNED"] != "") &
#             (temp["ACTUAL"] == "")
#         ]

#         return temp

#     except:
#         return pd.DataFrame()

# # ---------------------------
# # COLUMN BLOCKS (FIXED INDEX)
# # ---------------------------
# blocks = [
#     (12, 13, 14),  # M N O
#     (20, 21, 22),  # U V W
#     (28, 29, 30),  # AC AD AE
#     (36, 37, 38),  # AK AL AM
#     (44, 45, 46),  # AS AT AU
#     (52, 53, 54),  # BA BB BC
#     (60, 61, 62),  # BI BJ BK
#     (68, 69, 70),  # BQ BR BS
#     (76, 77, 78),  # BY BZ CA
# ]

# # ---------------------------
# # PROCESS ALL BLOCKS
# # ---------------------------
# final_df = pd.DataFrame()

# for doer_i, planned_i, actual_i in blocks:
#     temp_df = process_block(df, doer_i, planned_i, actual_i)
#     final_df = pd.concat([final_df, temp_df], ignore_index=True)

# # ---------------------------
# # UI
# # ---------------------------
# st.title("📊 ST JC FMS - Pending Work")

# if final_df.empty:
#     st.warning("⚠️ No pending data found")
# else:
#     st.success(f"✅ Total Pending Rows: {len(final_df)}")

#     # Buyer filter
#     buyer_list = sorted(final_df["BUYER"].dropna().unique().tolist())
#     buyer_filter = st.selectbox("Filter by Buyer", ["All"] + buyer_list)

#     if buyer_filter != "All":
#         final_df = final_df[final_df["BUYER"] == buyer_filter]

#     # Show table
#     st.dataframe(final_df, use_container_width=True)

#     # Download button
#     csv = final_df.to_csv(index=False).encode("utf-8")
#     st.download_button(
#         "⬇ Download CSV",
#         csv,
#         "pending_data.csv",
#         "text/csv"
#     )





# //-----------------------//
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

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
MAIN_SHEET = client.open_by_key(SHEET_ID).worksheet("ST JC FMS")
STORE_SHEET = client.open_by_key(SHEET_ID).worksheet("STORE")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data(ttl=60)
def load_data():
    data = MAIN_SHEET.get("A6:HD")
    df = pd.DataFrame(data)

    df.columns = range(len(df.columns))
    df = df[1:].reset_index(drop=True)

    return df

df = load_data()

# ---------------------------
# PROCESS FUNCTION
# ---------------------------
def process_block(df, doer_i, planned_i, actual_i, step_name):
    try:
        temp = df[[
            0,  # JOB SERIES
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
            "JC CARD NO",
            "BUYER",
            "ITEM CODE",
            "CUT QTY",
            "CUTTER",
            "DOER",
            "PLANNED",
            "ACTUAL"
        ]

        temp["PLANNED"] = temp["PLANNED"].astype(str).str.strip()
        temp["ACTUAL"] = temp["ACTUAL"].astype(str).str.strip()

        temp = temp[
            (temp["PLANNED"] != "") &
            (temp["ACTUAL"] == "")
        ]

        # Add STEP column
        temp["STEP NO"] = step_name

        return temp

    except:
        return pd.DataFrame()

# ---------------------------
# BLOCKS WITH STEP
# ---------------------------
blocks = [
    (12, 13, 14, "STEP-1"),  # M N O
    (20, 21, 22, "STEP-2"),  # U V W
    (28, 29, 30, "STEP-3"),  # AC AD AE
    (36, 37, 38, "STEP-4"),  # AK AL AM
    (44, 45, 46, "STEP-5"),  # AS AT AU
    (52, 53, 54, "STEP-6"),  # BA BB BC
    (60, 61, 62, "STEP-7"),  # BI BJ BK
    (68, 69, 70, "STEP-8"),  # BQ BR BS
    (76, 77, 78, "STEP-9"),  # BY BZ CA
]

# ---------------------------
# PROCESS ALL
# ---------------------------
final_df = pd.DataFrame()

for doer, planned, actual, step in blocks:
    temp = process_block(df, doer, planned, actual, step)
    final_df = pd.concat([final_df, temp], ignore_index=True)

# ---------------------------
# UI
# ---------------------------
st.title("📊 ST JC FMS - Pending Work")

if final_df.empty:
    st.warning("⚠️ No pending data found")
else:
    st.success(f"✅ Total Pending Rows: {len(final_df)}")

    # Filter
    buyer_list = sorted(final_df["BUYER"].dropna().unique().tolist())
    buyer_filter = st.selectbox("Filter by Buyer", ["All"] + buyer_list)

    if buyer_filter != "All":
        final_df = final_df[final_df["BUYER"] == buyer_filter]

    # Remove unwanted columns
    display_df = final_df.drop(columns=["ACTUAL"])

    # ---------------------------
    # DISPLAY WITH BUTTONS
    # ---------------------------
    for i, row in display_df.iterrows():
        cols = st.columns([2,2,2,2,2,2,2,2,2,1])

        cols[0].write(row["JOB SERIES"])
        cols[1].write(row["JC CARD NO"])
        cols[2].write(row["BUYER"])
        cols[3].write(row["ITEM CODE"])
        cols[4].write(row["CUT QTY"])
        cols[5].write(row["CUTTER"])
        cols[6].write(row["DOER"])
        cols[7].write(row["PLANNED"])
        cols[8].write(row["STEP NO"])

        if cols[9].button("SUBMIT", key=f"btn_{i}"):

            STORE_SHEET.append_row([
                datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                row["JOB SERIES"],
                row["STEP NO"],
                "YES"
            ])

            st.success(f"✅ Submitted: {row['JOB SERIES']} ({row['STEP NO']})")
            st.cache_data.clear()
            st.rerun()
