import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="Leaderboard", page_icon="🏆")

# --- 1. CONNECT TO GOOGLE SHEETS ---
# This function connects to the database using the key you saved in "Secrets"
def get_db_connection():
    # Load the key from the "Secrets" box
    key_dict = json.loads(st.secrets["google_sheets"]["json_key"])
    
    # Authorize with Google
    scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
    creds = Credentials.from_service_account_info(key_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    # Open the Sheet (Make sure the name matches exactly!)
    sheet = client.open("MathBar_Database").sheet1
    return sheet

# --- 2. TITLE & SCORE SAVER ---
st.title("🏆 Hall of Fame")

# Show current XP
current_xp = st.session_state.get("xp", 0)
st.info(f"Your Current XP: **{current_xp}**")

# Form to Save Score
with st.form("save_score"):
    st.write("### 💾 Save Your Score")
    name = st.text_input("Enter your Name:")
    submitted = st.form_submit_button("Submit to Global Leaderboard")
    
    if submitted:
        if name and current_xp > 0:
            try:
                sheet = get_db_connection()
                # Append a new row: [Name, XP, Date]
                # We use specific Python time format for date
                from datetime import datetime
                date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                sheet.append_row([name, current_xp, date_now])
                st.success(f"Success! {name} is now on the board!")
            except Exception as e:
                st.error(f"Error connecting to database: {e}")
        else:
            st.warning("You need a Name and some XP (Score > 0) to submit!")

# --- 3. DISPLAY LEADERBOARD ---
st.divider()
st.subheader("🌍 Top Players")

try:
    sheet = get_db_connection()
    # Get all records
    data = sheet.get_all_records()
    
    if data:
        # Convert to a nice table (DataFrame)
        df = pd.DataFrame(data)
        
        # Sort by XP (Highest first)
        df = df.sort_values(by="XP", ascending=False)
        
        # Add a "Rank" column (1, 2, 3...)
        df.insert(0, 'Rank', range(1, 1 + len(df)))
        
        # Display the table
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.write("No scores yet. Be the first!")
        
except Exception as e:
    st.warning("Waiting for connection...")