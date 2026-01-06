import streamlit as st
import random
import time

st.set_page_config(page_title="Advanced Math", page_icon="🚀")
if 'xp' not in st.session_state: st.session_state.xp = 0
with st.sidebar: st.header(f"🎓 XP: {st.session_state.xp}")

st.title("🚀 Advanced Mathematics: Calculus")

tab1, tab2 = st.tabs(["📚 Learn", "📝 Practice"])

with tab1:
    st.header("The Power Rule (Derivatives)")
    st.write("To find the derivative of $x^n$, bring the power down and subtract 1.")
    st.latex(r"\frac{d}{dx} x^n = n \cdot x^{n-1}")

with tab2:
    st.subheader("Find the Derivative")
    
    if 'adv_n' not in st.session_state:
        st.session_state.adv_n = random.randint(2, 9)
        
    n = st.session_state.adv_n
    
    st.write(f"What is the derivative of $x^{{{n}}}$?")
    
    c1, c2 = st.columns(2)
    coeff = c1.number_input("Coefficient (The number in front):", step=1)
    power = c2.number_input("New Power (The exponent):", step=1)
    
    if st.button("Check Derivative"):
        if coeff == n and power == (n-1):
            st.balloons()
            st.success("Correct! +20 XP")
            st.session_state.xp += 20
            del st.session_state['adv_n']
            time.sleep(1.5)
            st.rerun()
        else:
            st.error(f"Hint: Bring down {n}, then subtract 1 from the power.")