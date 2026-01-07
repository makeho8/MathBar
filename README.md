# MathBar
**Full-Stack Web Application**.
📂 mathbar/
 ├── 📄 app.py
 ├── 📂 pages/                     (The Menu Buttons - Keep these files TINY)
 │    ├── 1_🚀_Advanced_Math.py
 │    ├── 2_🌀_Specialized_Math.py
 │    ├── 3_🎲_Prob_Stats.py
 │    ├── 4_🧩_Discrete_Math.py
 │    ├── 5_📐_Linear_Algebra.py
 │    ├── 6_∫_Calculus_Single.py
 │    └── 7_∬_Calculus_Multi.py
 │
 └── 📂 materials/                 (The Heavy Content - Put the long code here)
      ├── 📂 advanced_math/
      │    ├── content.py          <-- The Textbook (Text/Latex/Graphs)
      │    ├── quiz.py             <-- The Practice Questions
      │    └── slides.py           <-- The Presentation Logic
      │
      ├── 📂 specialized_math/     (Same 3 files inside...)
      ├── 📂 prob_stats/           (Same 3 files inside...)
      ├── 📂 discrete_math/        (Same 3 files inside...)
      ├── 📂 linear_algebra/       (Same 3 files inside...)
      ├── 📂 calculus_single/      (Same 3 files inside...)
      └── 📂 calculus_multi/       (Same 3 files inside...)

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
google-generativeai>=0.7.2
# Force Update 1

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



### Step 1: Get Your Free API Key 🔑

1. Go to **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
2. Click the blue button **"Create API Key"**.
3. (If asked) Select your "MathBar" project (or create a new one).
4. Copy the key (it starts with `AIza...`).

---

### Step 2: Save the Key in Streamlit Secrets 🔒

Just like we did for the Google Sheet, we need to hide this password.

1. Go to **Streamlit Cloud Dashboard**  App Settings  **Secrets**.
2. Add a new section at the bottom (below the `[google_sheets]` part).

**Paste this:**

```toml
[gemini]
api_key = "PASTE_YOUR_AIza_KEY_HERE"

```

3. Click **Save**.

---

### Step 3: Update `requirements.txt` 📦

We need a new tool to talk to Google's brain.

1. Open `requirements.txt` in GitHub/Thonny.
2. Add this line at the bottom:
```text
google-generativeai>=0.7.2

```

---

### Step 4: The Real AI Code 🧠

Now, let's perform the brain transplant. We will replace the "Parrot" code with the "Gemini" code.

**Open `pages/7_🤖_AI_Tutor.py` and replace EVERYTHING with this:**

```python
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Math Tutor", page_icon="🤖")

st.title("🤖 AI Math Tutor")

# --- 1. CONNECT TO GOOGLE ---
try:
    # Get Key
    api_key = st.secrets["gemini"]["api_key"]
    genai.configure(api_key=api_key)
    
    # --- AUTO-DETECT MODEL ---
    # This block finds a working model automatically so we stop getting 404 errors
    try:
        # Ask Google what models are available
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Prefer the fast one, fallback to the standard one, or take whatever is there
        if "models/gemini-1.5-flash" in all_models:
            model_name = "models/gemini-1.5-flash"
        elif "models/gemini-pro" in all_models:
            model_name = "models/gemini-pro"
        else:
            model_name = all_models[0] # Just take the first one that works
            
        model = genai.GenerativeModel(model_name)
        st.caption(f"Connected to Brain: `{model_name}`")
        
    except Exception as e:
        st.error(f"Could not find any AI models. Error: {e}")
        st.stop()

except Exception as e:
    st.error("Missing API Key! Check your Streamlit Secrets.")
    st.stop()

# --- 2. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. CHAT INPUT ---
if prompt := st.chat_input("Ask me a math question..."):
    
    # Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking... ⏳")
        
        try:
            # Simple math tutor prompt
            full_prompt = f"You are a helpful math tutor. Answer this simply: {prompt}"
            
            response = model.generate_content(full_prompt)
            ai_text = response.text
            
            placeholder.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
            
        except Exception as e:
            placeholder.error(f"Error: {e}")

```
