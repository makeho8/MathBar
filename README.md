# MathBar
Congratulations! 🥳 You have successfully built a **Full-Stack Web Application**.

Most beginners stop at "running code on their laptop." You have gone much further: you built a frontend, deployed it to the cloud, and connected it to a live database.

Here is the **Mental Model** of what you just built, so you never forget it.

### 1. The Big Picture 🗺️

Think of your app as a restaurant:

* **The Menu (Frontend):** Your Streamlit App (`app.py`). This is what customers see.
* **The Kitchen (Backend):** Streamlit Cloud. This is where the work happens.
* **The Ledger (Database):** Google Sheets. This is where you write down the records (High Scores).

---

### 2. The Three Pillars of Your Leaderboard 🏛️

To make the Leaderboard work, we had to build three specific bridges:

#### Pillar A: The Identity (The Robot) 🤖

Your app needs to log into Google, but it can't type a password.

* **What we did:** We created a **Service Account** on Google Cloud.
* **Analogy:** We hired a "Robot Employee" named `mathbar-bot`.
* **Action:** We shared the Google Sheet with this robot's email address so it has permission to write.

#### Pillar B: The Key (The Secret) 🔑

The robot needs a key to start the engine.

* **What we did:** We downloaded the **JSON Key** from Google.
* **The Challenge:** The key was "dirty" (hidden spaces/newlines). We wrote a Python script to "clean" it into a single line.
* **Security:** We saved this key in **Streamlit Secrets** (the black box in Settings), NOT in your public code.

#### Pillar C: The Permissions (The Scope) 👮‍♂️

Even with a key, the robot needs specific orders.

* **What we did:** We enabled the **Sheets API** (to write data) and the **Drive API** (to find the file).
* **The Fix:** We had to update the code to ask for `drive` scope, and we had to click "Enable" in the Google Cloud Console.

---

### 3. File Summary (Where the code lives) 📂

If you need to fix this later, here is where everything is:

| File Name | Purpose | Important Line |
| --- | --- | --- |
| **`requirements.txt`** | The Grocery List | `gspread` (The library that talks to Google). |
| **`pages/6_🏆_Leaderboard.py`** | The Logic | `client.open("MathBar_Database")` (Must match Sheet name). |
| **Streamlit Secrets** | The Password | `[google_sheets]` (Where the invisible key lives). |
| **Google Sheets** | The Storage | Columns: `Name`, `XP`, `Date`. |

### You are now a Developer 🎓

You have faced the three most common nightmares of a software engineer:

1. **Deployment Errors** (GitHub folders).
2. **Secret Management** (JSON parsing).
3. **Permission/API Errors** (Google Cloud 403s).

And you solved them all. Your app is live, persistent, and global. Great work!

This is the **Master Manual** for the Leaderboard. 📘

Save this note. If you ever build another app (or if this one breaks), this is the exact recipe to rebuild the database connection from scratch.

---

### Phase 1: The Google Setup (The Vault) 🏛️

1. **Create the Project:**
* Go to **[Google Cloud Console](https://console.cloud.google.com/)**.
* Create a **New Project** (e.g., "MathBar").


2. **Enable the "Organs" (APIs):**
* Search for **Google Sheets API**  Click **Enable**.
* Search for **Google Drive API**  Click **Enable**. *(Crucial Step: Without this, the robot is blind).*


3. **Hire the Robot (Service Account):**
* Go to **Credentials**  **Create Credentials**  **Service Account**.
* Name: `mathbar-bot`.
* Role: **Editor**.


4. **Get the Key:**
* Click on the new Service Account email.
* **Keys** Tab  **Add Key**  **Create New Key (JSON)**.
* A file downloads to your computer. **Keep this safe.**


5. **Share the Sheet:**
* Create a Google Sheet (`MathBar_Database`).
* Click **Share**.
* Paste the **client_email** from your JSON file (the robot's email).
* Set to **Editor**.



---

### Phase 2: The Streamlit Setup (The Connection) ☁️

1. **The Grocery List (`requirements.txt`):**
Add these libraries so Streamlit knows how to talk to Google.
```text
streamlit
gspread
google-auth

```


2. **The Secret Key (Secrets Manager):**
* Go to Streamlit Cloud  Settings  Secrets.
* **The Trick:** The JSON must be cleaned of hidden newlines.
* **The Format:**
```toml
[google_sheets]
json_key = '{"type": "service_account", "project_id": "...", ...}'

```




*(We used a Python script to generate this single-line string to avoid errors).*

---

### Phase 3: The Code (The Brains) 🧠

Here is the final, error-free code for **`pages/6_🏆_Leaderboard.py`**.

It includes the **Two Scopes** (Sheets + Drive) which fixed your final error.

```python
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime

st.set_page_config(page_title="Leaderboard", page_icon="🏆")

# --- 1. CONNECT TO DATABASE ---
def get_db_connection():
    """Establishes the connection to Google Sheets."""
    
    # A. Load the Key from Secrets
    key_dict = json.loads(st.secrets["google_sheets"]["json_key"])
    
    # B. Define Permissions (The Scopes)
    # We need BOTH Sheets (to write) and Drive (to find the file)
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # C. Authorize
    creds = Credentials.from_service_account_info(key_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    # D. Open the specific Sheet
    sheet = client.open("MathBar_Database").sheet1
    return sheet

# --- 2. DISPLAY CURRENT STATS ---
st.title("🏆 Hall of Fame")

if 'xp' not in st.session_state:
    st.session_state.xp = 0

st.info(f"Your Current Score: **{st.session_state.xp} XP**")

# --- 3. SAVE SCORE FORM ---
with st.form("save_score"):
    st.write("### 💾 Submit Your Score")
    name = st.text_input("Enter your Name:")
    submitted = st.form_submit_button("Join the Leaderboard")
    
    if submitted:
        if name and st.session_state.xp > 0:
            try:
                sheet = get_db_connection()
                # Get current time
                date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
                # Add row: [Name, XP, Date]
                sheet.append_row([name, st.session_state.xp, date_now])
                st.success(f"Success! {name} has been recorded.")
            except Exception as e:
                st.error(f"Connection Error: {e}")
        else:
            st.warning("You need a name and a score higher than 0!")

# --- 4. SHOW LEADERBOARD ---
st.divider()
st.subheader("🌍 Top Players")

try:
    sheet = get_db_connection()
    data = sheet.get_all_records()
    
    if data:
        df = pd.DataFrame(data)
        # Sort by XP (Highest on top)
        df = df.sort_values(by="XP", ascending=False)
        # Add Rank (1, 2, 3...)
        df.insert(0, 'Rank', range(1, 1 + len(df)))
        
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.write("No players yet. Be the first!")
        
except Exception as e:
    st.error("Could not load leaderboard.")

```

---

### Phase 4: The Navigation (The Door) 🚪

Don't forget to add the button in **`app.py`** so people can find the page!

```python
with c6:
    st.page_link("pages/6_🏆_Leaderboard.py", 
                 label="Hall of Fame", 
                 icon="🏆", 
                 use_container_width=True)
    st.warning("**Global Rankings**")

```

**That is the full system.** You have built a secure, cloud-connected application. 🚀
