import streamlit as st
import random
import time

st.set_page_config(page_title="Discrete Math", page_icon="🧩")
if 'xp' not in st.session_state: st.session_state.xp = 0
with st.sidebar: st.header(f"🎓 XP: {st.session_state.xp}")

st.title("🧩 Discrete Mathematics: Logic")

tab1, tab2 = st.tabs(["📚 Learn", "📝 Practice"])

with tab1:
    st.header("Logic Gates")
    st.markdown("""
    * **AND**: True only if BOTH are True.
    * **OR**: True if AT LEAST ONE is True.
    """)
    st.code("True AND False = False\nTrue OR False = True")

with tab2:
    if 'disc_op' not in st.session_state:
        st.session_state.disc_op = random.choice(["AND", "OR"])
        st.session_state.disc_val1 = random.choice([True, False])
        st.session_state.disc_val2 = random.choice([True, False])

    op = st.session_state.disc_op
    v1 = st.session_state.disc_val1
    v2 = st.session_state.disc_val2
    
    if op == "AND":
        ans = v1 and v2
    else:
        ans = v1 or v2
        
    st.write(f"Solve: **{v1} {op} {v2}**")
    
    user_choice = st.radio("Is this True or False?", [True, False])
    
    if st.button("Check Logic"):
        if user_choice == ans:
            st.balloons()
            st.success("Correct! +10 XP")
            st.session_state.xp += 10
            del st.session_state['disc_op']
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Check the Truth Table in the Learn tab!")