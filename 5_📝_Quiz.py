import streamlit as st

st.header("📝 The Daily Quiz")
st.write("Answer all questions correctly to win a **50 XP Bonus**!")

# --- 1. Check Backpack ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0

# CREATE A PLACEHOLDER (A reserved seat in the sidebar)
# We assign it to a variable 'xp_display' so we can update it later
with st.sidebar:
    xp_display = st.empty() 
    # Write the current score immediately into the placeholder
    xp_display.header(f"🎓 XP: {st.session_state.xp}")

# --- 2. The Quiz Form ---
# Everything inside 'with st.form' waits for the Submit button
with st.form("math_quiz"):
    
    # Question 1: Algebra (Multiple Choice)
    st.write("### Question 1")
    st.write("If $2x = 10$, what is $x$?")
    q1_ans = st.radio("Select answer:", [2, 4, 5, 10])
    
    # Question 2: Geometry (Text Input)
    st.write("### Question 2")
    st.write("What is the name of a triangle with 3 equal sides?")
    # .lower() helps us ignore capitalization (Equilateral vs equilateral)
    q2_ans = st.text_input("Type your answer:").lower()
    
    # Question 3: Logic (Checkbox)
    st.write("### Question 3")
    st.write("Which of these are integers? (Select all that apply)")
    q3_opt1 = st.checkbox("2.5")
    q3_opt2 = st.checkbox("7") # Correct
    q3_opt3 = st.checkbox("-5") # Correct
    
    # The Submit Button
    submitted = st.form_submit_button("Submit Quiz 🚀")

# --- 3. Grading Logic ---
# This code runs ONLY when the button is clicked
if submitted:
    score = 0
    
    # Check Q1
    if q1_ans == 5:
        score += 1
    else:
        st.error("Question 1 is wrong.")
        
    # Check Q2 (Check if 'equilateral' is in their answer)
    if "equilateral" in q2_ans:
        score += 1
    else:
        st.error("Question 2 is wrong. (Hint: Starts with E)")
        
    # Check Q3 (Must have Opt2 AND Opt3 checked, but NOT Opt1)
    if q3_opt2 and q3_opt3 and not q3_opt1:
        score += 1
    else:
        st.error("Question 3 is wrong.")
    
    # Final Result
    if score == 3:
        st.balloons()
        st.success("🎉 PERFECT SCORE! You earned +50 XP")
        st.session_state.xp += 50
        
        # --- THE FIX: UPDATE THE SIDEBAR NOW ---
        # We overwrite the text in the placeholder we created at the top
        xp_display.header(f"🎓 XP: {st.session_state.xp}")
        
    else:
        st.warning(f"You got {score}/3 correct. Try again!")