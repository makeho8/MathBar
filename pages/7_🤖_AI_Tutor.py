import streamlit as st
import random
import time

st.set_page_config(page_title="Math Bot", page_icon="🤖")

st.title("🤖 Math Tutor Bot")
st.write("I am here to help! (Currently in 'Training Mode')")

# --- 1. MEMORY (Session State) ---
# We need to store the chat history, otherwise it disappears when you click a button.
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. DISPLAY HISTORY ---
# Every time the app reloads, we print the old messages again.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. THE CHAT INPUT ---
# This creates the text box at the bottom
if prompt := st.chat_input("Ask me a math question..."):
    
    # A. Show User's Message
    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display in UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # B. Generate Robot Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # --- SIMPLE LOGIC (The "Brain") ---
        # Right now, it just picks a random phrase. 
        # Later, we will connect this to ChatGPT!
        responses = [
            "That is an interesting question! 🤔",
            "Have you tried using the Pythagorean theorem?",
            "I am still learning, but I think the answer involves 'x'.",
            f"You said: '{prompt}'. I am listening!",
            "Math is fun! Let's solve this together."
        ]
        assistant_response = random.choice(responses)
        
        # Simulate "Typing" effect
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to show it's working
            message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(full_response)
    
    # C. Save Robot's Message to History
    st.session_state.messages.append({"role": "assistant", "content": full_response})