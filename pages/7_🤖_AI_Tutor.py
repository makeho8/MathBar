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


