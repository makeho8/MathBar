import streamlit as st
import random
import time

st.set_page_config(page_title="Specialized Math", page_icon="🌀")
if 'xp' not in st.session_state: st.session_state.xp = 0
with st.sidebar: st.header(f"🎓 XP: {st.session_state.xp}")

st.title("🌀 Specialized Math: Complex Numbers")

tab1, tab2 = st.tabs(["📚 Learn", "📝 Practice"])

with tab1:
    st.header("Adding Complex Numbers")
    st.write("Combine real parts with real parts, and imaginary parts with imaginary parts.")
    st.latex(r"(a + bi) + (c + di) = (a+c) + (b+d)i")

with tab2:
    if 'spec_r1' not in st.session_state:
        st.session_state.spec_r1 = random.randint(1, 10)
        st.session_state.spec_i1 = random.randint(1, 10)
        st.session_state.spec_r2 = random.randint(1, 10)
        st.session_state.spec_i2 = random.randint(1, 10)

    r1, i1 = st.session_state.spec_r1, st.session_state.spec_i1
    r2, i2 = st.session_state.spec_r2, st.session_state.spec_i2
    
    st.write(f"Calculate: $({r1} + {i1}i) + ({r2} + {i2}i)$")
    
    user_r = st.number_input("Real Part:", step=1)
    user_i = st.number_input("Imaginary Part:", step=1)
    
    if st.button("Submit Complex Answer"):
        if user_r == (r1+r2) and user_i == (i1+i2):
            st.balloons()
            st.success("Correct! +20 XP")
            st.session_state.xp += 20
            del st.session_state['spec_r1'] 
            # (Delete others too if you want strict cleanup, but this triggers the reset)
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Add the real numbers together and the imaginary numbers together.")