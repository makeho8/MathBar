import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Math Tutor", page_icon="🤖")

st.title("🤖 AI Math Tutor")

# --- 1. SIDEBAR: CLEAR BUTTON ---
# We put this in the sidebar so it's always accessible but out of the way
with st.sidebar:
    st.write("### ⚙️ Controls")
    if st.button("🗑️ Clear Chat History", type="primary"):
        st.session_state.messages = [] # Wipe the memory
        st.rerun() # Refresh the page immediately

# --- 2. CONNECT TO GOOGLE ---
try:
    api_key = st.secrets["gemini"]["api_key"]
    genai.configure(api_key=api_key)
    
    # Auto-detect model logic
    try:
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if "models/gemini-1.5-flash" in all_models:
            model_name = "models/gemini-1.5-flash"
        elif "models/gemini-pro" in all_models:
            model_name = "models/gemini-pro"
        else:
            model_name = all_models[0]
            
        model = genai.GenerativeModel(model_name)
        # st.caption(f"Connected to Brain: `{model_name}`") # Optional: Hide this from students to keep it clean
        
    except Exception as e:
        st.error(f"Could not find any AI models. Error: {e}")
        st.stop()

except Exception as e:
    st.error("Missing API Key! Check your Streamlit Secrets.")
    st.stop()

# --- 3. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display welcome message if chat is empty
if len(st.session_state.messages) == 0:
    st.info("👋 Hi! I am your Math Tutor. Ask me anything!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT INPUT ---
if prompt := st.chat_input("Ask a math question..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking... ⏳")
        
        try:
            full_prompt = f"You are a helpful math tutor. Answer this simply: {prompt}"
            response = model.generate_content(full_prompt)
            ai_text = response.text
            
            placeholder.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
            
        except Exception as e:
            placeholder.error(f"Error: {e}")

