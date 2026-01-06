import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Math Tutor", page_icon="🤖")

st.title("🤖 AI Math Tutor")
st.caption("Powered by Google Gemini")

# --- 1. SETUP THE BRAIN ---
try:
    # Get the key from Secrets
    api_key = st.secrets["gemini"]["api_key"]
    genai.configure(api_key=api_key)
    
    # Select the model (Flash is fast and free)
    # Select the model (Pro is the standard stable version)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")
    st.stop()

# --- 2. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. THE CHAT LOOP ---
if prompt := st.chat_input("Ask a math question (e.g., 'Explain derivatives')..."):
    
    # A. Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # B. Generate AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... 🤔")
        
        try:
            # Create a prompt specifically for a Math Tutor
            # We tell the AI how to behave
            tutor_instruction = """
            You are a friendly and helpful Math Tutor for students.
            - Explain concepts simply.
            - Use emojis to make it fun.
            - If there is a calculation, show the steps.
            - Use LaTeX for math formulas (like $x^2$).
            
            Student Question: 
            """
            
            full_prompt = tutor_instruction + prompt
            
            # Send to Google
            response = model.generate_content(full_prompt)
            ai_text = response.text
            
            # Show Result
            message_placeholder.markdown(ai_text)
            
            # C. Save AI Message
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
            
        except Exception as e:
            message_placeholder.error(f"Error: {e}")

