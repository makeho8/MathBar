import streamlit as st

# 1. Page Config
st.set_page_config(page_title="The Math Bar", page_icon="☕", layout="wide")

# --- 🔐 SECURITY SYSTEM ---
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "0123456789makeho":#Your password here
            st.session_state["password_correct"] = True
            del st.session_state["password"] #Don't store password
        else:
            st.session_state["password_correct"] = False
            
    # If we have verified the password already, return True
    if st.session_state.get("password_correct", False):
        return True
    
    #Show input for password
    st.text_input("🔒 Enter Password:", type="password", on_change=password_entered, key="password")
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

# --- 🛑 STOP HERE IF NOT LOGGED IN ---
if not check_password():
    st.stop()  # The app stops here. Nothing below runs until password is correct.

# ============================================
# 🚀 THE APP CONTENT (Only runs if Logged In)
# ============================================

# 2. The Backpack (Session State)
if 'xp' not in st.session_state:
    st.session_state.xp = 0

# 3. --- SIDEBAR (With Reset Button) ---
with st.sidebar:
    st.header(f"🎓 Student XP: {st.session_state.xp}")
    st.write("---")
    # THE RESET BUTTON
    # We use a unique key to prevent conflicts
    if st.button("🔄 Reset Score"):
        st.session_state.xp = 0 # Set score to zero
        st.rerun() # Refresh the app instantly
        
    st.write("---")
    st.write("Select a topic above to start practicing!")

# 4. Main Content-----------------------
st.title("☕ Welcome to The Math Bar")
st.write("### 📚 Select a topic from the sidebar 👈 or Click a card below 👇 to start your brain workout.")

# 5. Your Menu Cards
# Row 1
c1, c2, c3 = st.columns(3)
with c1:
    st.page_link("pages/1_🚀_Advanced_Math.py", label="Advanced Math", icon="🚀", use_container_width=True)
    st.info("Calculus & Analysis")
with c2:
    st.page_link("pages/2_🌀_Specialized_Math.py", label="Specialized Math", icon="🌀", use_container_width=True)
    st.success("Complex Numbers")
with c3:
    st.page_link("pages/3_🎲_Prob_Stats.py", label="Prob & Stats", icon="🎲", use_container_width=True)
    st.warning("Data Science")

# Row 2
c4, c5, c6 = st.columns(3)

with c4:
    st.page_link("pages/4_🧩_Discrete_Math.py", label="Discrete Math", icon="🧩", use_container_width=True)
    st.error("Logic & Sets")

with c5:
    st.page_link("pages/5_📝_Quiz.py", label="Final Quiz", icon="📝", use_container_width=True)
    st.info("**Test Yourself**")

with c6:
    # 🆕 THIS IS THE NEW LINK
    st.page_link("pages/6_🏆_Leaderboard.py", label="Hall of Fame", icon="🏆", use_container_width=True)
    st.warning("**Global Rankings**")
    
# --- Row 3 (AI Section) ---
st.divider() # Adds a nice line to separate sections
st.subheader("🤖 AI Assistance")

# Create a new column layout (we center the button)
c7, c8, c9 = st.columns([1, 2, 1])

with c8: # This puts the button in the middle column so it looks important
    st.page_link("pages/7_🤖_AI_Tutor.py", label="Chat with AI Tutor", icon="🤖", use_container_width=True)
    st.info("**Need help? Ask the Robot!** (Experimental)")

# --- Row 4 (Teacher Tools) ---
st.divider()
st.subheader("👨‍🏫 Classroom Resources")

# We use 3 columns to keep buttons organized
d1, d2, d3 = st.columns(3)

with d1:
    st.page_link("pages/8_👨‍🏫_Lecture_Slides.py", label="Open Lecture Slides", icon="📽️", use_container_width=True)

with d2:
    st.info("Select 'Lecture Slides' to project the lesson.")

with d3:
    # Placeholder for future files (like a Syllabus PDF)
    st.write("")
    
