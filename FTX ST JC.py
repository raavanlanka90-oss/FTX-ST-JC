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
# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials
# from datetime import datetime

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
# MAIN_SHEET = client.open_by_key(SHEET_ID).worksheet("ST JC FMS")
# STORE_SHEET = client.open_by_key(SHEET_ID).worksheet("STORE")

# # ---------------------------
# # LOAD DATA
# # ---------------------------
# @st.cache_data(ttl=60)
# def load_data():
#     data = MAIN_SHEET.get("A6:HD")
#     df = pd.DataFrame(data)

#     df.columns = range(len(df.columns))
#     df = df[1:].reset_index(drop=True)

#     return df

# df = load_data()

# # ---------------------------
# # PROCESS FUNCTION
# # ---------------------------
# def process_block(df, doer_i, planned_i, actual_i, step_name):
#     try:
#         temp = df[[
#             0, 2, 3, 4, 5, 6,
#             doer_i, planned_i, actual_i
#         ]].copy()

#         temp.columns = [
#             "JOB SERIES",
#             "JC CARD NO",
#             "BUYER",
#             "ITEM CODE",
#             "CUT QTY",
#             "CUTTER",
#             "DOER",
#             "PLANNED",
#             "ACTUAL"
#         ]

#         temp["PLANNED"] = temp["PLANNED"].astype(str).str.strip()
#         temp["ACTUAL"] = temp["ACTUAL"].astype(str).str.strip()

#         temp = temp[
#             (temp["PLANNED"] != "") &
#             (temp["ACTUAL"] == "")
#         ]

#         temp["STEP NO"] = step_name

#         return temp

#     except:
#         return pd.DataFrame()

# # ---------------------------
# # BLOCKS
# # ---------------------------
# blocks = [
#     (12, 13, 14, "STEP-1"),
#     (20, 21, 22, "STEP-2"),
#     (28, 29, 30, "STEP-3"),
#     (36, 37, 38, "STEP-4"),
#     (44, 45, 46, "STEP-5"),
#     (52, 53, 54, "STEP-6"),
#     (60, 61, 62, "STEP-7"),
#     (68, 69, 70, "STEP-8"),
#     (76, 77, 78, "STEP-9"),
# ]

# # ---------------------------
# # BUILD DATA
# # ---------------------------
# final_df = pd.DataFrame()

# for b in blocks:
#     temp = process_block(df, *b)
#     final_df = pd.concat([final_df, temp], ignore_index=True)

# # ---------------------------
# # SESSION STATE (for button color)
# # ---------------------------
# if "submitted" not in st.session_state:
#     st.session_state.submitted = set()

# # ---------------------------
# # UI
# # ---------------------------
# st.title("📊 ST JC FMS - Pending Work")

# if final_df.empty:
#     st.warning("⚠️ No pending data found")
#     st.stop()

# st.success(f"✅ Total Pending Rows: {len(final_df)}")

# # ---------------------------
# # FILTERS
# # ---------------------------
# col1, col2, col3 = st.columns(3)

# buyer_list = ["All"] + sorted(final_df["BUYER"].dropna().unique())
# doer_list = ["All"] + sorted(final_df["DOER"].dropna().unique())
# step_list = ["All"] + sorted(final_df["STEP NO"].dropna().unique())

# buyer_filter = col1.selectbox("Filter by Buyer", buyer_list)
# doer_filter = col2.selectbox("Filter by DOER", doer_list)
# step_filter = col3.selectbox("Filter by STEP", step_list)

# filtered_df = final_df.copy()

# if buyer_filter != "All":
#     filtered_df = filtered_df[filtered_df["BUYER"] == buyer_filter]

# if doer_filter != "All":
#     filtered_df = filtered_df[filtered_df["DOER"] == doer_filter]

# if step_filter != "All":
#     filtered_df = filtered_df[filtered_df["STEP NO"] == step_filter]

# # ---------------------------
# # HEADER (FREEZE STYLE)
# # ---------------------------
# header = st.columns([2,2,2,2,2,2,2,2,2,1])

# headers = [
#     "JOB SERIES","JC CARD NO","BUYER","ITEM CODE",
#     "CUT QTY","CUTTER","DOER","PLANNED","STEP NO","ACTION"
# ]

# for col, h in zip(header, headers):
#     col.markdown(f"**{h}**")

# st.markdown("---")

# # ---------------------------
# # ROW DISPLAY
# # ---------------------------
# for i, row in filtered_df.iterrows():
#     cols = st.columns([2,2,2,2,2,2,2,2,2,1])

#     cols[0].write(row["JOB SERIES"])
#     cols[1].write(row["JC CARD NO"])
#     cols[2].write(row["BUYER"])
#     cols[3].write(row["ITEM CODE"])
#     cols[4].write(row["CUT QTY"])
#     cols[5].write(row["CUTTER"])
#     cols[6].write(row["DOER"])
#     cols[7].write(row["PLANNED"])
#     cols[8].write(row["STEP NO"])

#     key_id = f"{row['JOB SERIES']}_{row['STEP NO']}"

#     # Button color logic
#     if key_id in st.session_state.submitted:
#         cols[9].button("✅ DONE", key=f"done_{i}", disabled=True)
#     else:
#         if cols[9].button("SUBMIT", key=f"btn_{i}"):

#             STORE_SHEET.append_row([
#                 datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
#                 row["JOB SERIES"],
#                 row["STEP NO"],
#                 "YES"
#             ])

#             st.session_state.submitted.add(key_id)

#             st.success(f"✅ Submitted: {row['JOB SERIES']} ({row['STEP NO']})")

#             st.cache_data.clear()
#             st.rerun()


# //------------------------------------------------------------------------//
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
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>
.header-row {
    position: sticky;
    top: 0;
    background-color: #0E1117;
    z-index: 999;
    padding: 10px 0;
    border-bottom: 2px solid #444;
}

div.stButton > button {
    white-space: nowrap;
    width: 100%;
    height: 40px;
    font-weight: bold;
}

.done-btn button {
    background-color: #28a745 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# GOOGLE SHEETS
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
# PROCESS BLOCK
# ---------------------------
def process_block(df, doer_i, planned_i, actual_i, step_name):
    temp = df[[0,2,3,4,5,6,doer_i,planned_i,actual_i]].copy()

    temp.columns = [
        "JOB SERIES","JC CARD NO","BUYER","ITEM CODE",
        "CUT QTY","CUTTER","DOER","PLANNED","ACTUAL"
    ]

    temp["PLANNED"] = temp["PLANNED"].astype(str).str.strip()
    temp["ACTUAL"] = temp["ACTUAL"].astype(str).str.strip()

    temp = temp[(temp["PLANNED"] != "") & (temp["ACTUAL"] == "")]

    temp["STEP NO"] = step_name

    return temp

# ---------------------------
# BLOCKS
# ---------------------------
blocks = [
    (12,13,14,"STEP-1"),
    (20,21,22,"STEP-2"),
    (28,29,30,"STEP-3"),
    (36,37,38,"STEP-4"),
    (44,45,46,"STEP-5"),
    (52,53,54,"STEP-6"),
    (60,61,62,"STEP-7"),
    (68,69,70,"STEP-8"),
    (76,77,78,"STEP-9"),
]

final_df = pd.concat([process_block(df,*b) for b in blocks], ignore_index=True)

# ---------------------------
# SESSION STATE
# ---------------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = set()

# ---------------------------
# UI
# ---------------------------
st.title("📊 ST JC FMS - Pending Work")

if final_df.empty:
    st.warning("No pending data")
    st.stop()

st.success(f"Total Pending Rows: {len(final_df)}")

# ---------------------------
# FILTERS (ONLY DOER + STEP)
# ---------------------------
c1, c2 = st.columns(2)

doer = c1.selectbox("Filter by DOER", ["All"] + sorted(final_df["DOER"].unique()))
step = c2.selectbox("Filter by STEP", ["All"] + sorted(final_df["STEP NO"].unique()))

df_f = final_df.copy()

if doer != "All":
    df_f = df_f[df_f["DOER"] == doer]

if step != "All":
    df_f = df_f[df_f["STEP NO"] == step]

# ---------------------------
# HEADER
# ---------------------------
header = st.columns([2,2,2,2,2,2,2,2,2,1])

for col, name in zip(header, [
    "JOB SERIES","JC CARD NO","BUYER","ITEM CODE",
    "CUT QTY","CUTTER","DOER","PLANNED","STEP NO","ACTION"
]):
    col.markdown(f"<div class='header-row'><b>{name}</b></div>", unsafe_allow_html=True)

# ---------------------------
# ROWS
# ---------------------------
for i, row in df_f.iterrows():
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

    key = f"{row['JOB SERIES']}_{row['STEP NO']}"

    if key in st.session_state.submitted:
        cols[9].markdown("<div class='done-btn'>", unsafe_allow_html=True)
        cols[9].button("DONE", key=f"d{i}", disabled=True)
        cols[9].markdown("</div>", unsafe_allow_html=True)
    else:
        if cols[9].button("SUBMIT", key=f"s{i}"):

            STORE_SHEET.append_row([
                datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                row["JOB SERIES"],
                row["STEP NO"],
                "YES"
            ])

            st.session_state.submitted.add(key)
            st.success(f"Submitted {row['JOB SERIES']} - {row['STEP NO']}")
            st.cache_data.clear()
            st.rerun()
