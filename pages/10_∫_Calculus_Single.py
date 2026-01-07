import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
TOPIC_NAME = "Single-Variable Calculus"
TOPIC_ICON = "∫"

st.set_page_config(page_title=TOPIC_NAME, page_icon=TOPIC_ICON, layout="wide")
st.title(f"{TOPIC_ICON} {TOPIC_NAME}")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📚 Content", "📝 Practice", "👨‍🏫 Slides"])

# --- TAB 1: CONTENT ---
with tab1:
    st.header("The Derivative")
    st.write("The derivative measures the **rate of change** (slope) of a function.")
    st.latex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}")

    st.subheader("Visualizing Tangent Lines")
    x_val = st.slider("Choose x value:", -3.0, 3.0, 1.0)
    
    # Graph y = x^2 and its tangent
    x = np.linspace(-4, 4, 100)
    y = x**2
    slope = 2 * x_val
    intercept = (x_val**2) - (slope * x_val)
    y_tan = slope * x + intercept
    
    fig, ax = plt.subplots()
    ax.plot(x, y, label="f(x) = x^2")
    ax.plot(x, y_tan, '--', label=f"Tangent at x={x_val}")
    ax.scatter([x_val], [x_val**2], color='red')
    ax.legend()
    ax.grid()
    st.pyplot(fig)

# --- TAB 2: PRACTICE ---
with tab2:
    st.header("🧠 Derivatives Quiz")
    
    st.write("**Question 1:** What is the derivative of $f(x) = 3x^2$?")
    ans = st.radio("Select Answer:", ["6x", "3x", "x^3", "6"], key="calc1_q1")
    
    if st.button("Check Answer", key="btn_c1"):
        if ans == "6x":
            st.success("Correct! Power rule: 2 * 3x^(2-1) = 6x")
        else:
            st.error("Remember the Power Rule: nx^(n-1)")

# --- TAB 3: SLIDES ---
with tab3:
    st.write("### 📽️ Lecture Slides")
    if 'slide_c1' not in st.session_state: st.session_state.slide_c1 = 0
    
    def s1():
        st.header("Intro to Integrals")
        st.write("Integration is finding the **Area Under the Curve**.")
    def s2():
        st.header("Fundamental Theorem of Calculus")
        st.latex(r"\int_a^b f(x)dx = F(b) - F(a)")
    
    slides = [s1, s2]
    
    c1, c2, c3 = st.columns([1,2,1])
    if c1.button("⬅️ Prev", key="c1_prev"):
        if st.session_state.slide_c1 > 0: st.session_state.slide_c1 -= 1; st.rerun()
    if c3.button("Next ➡️", key="c1_next"):
        if st.session_state.slide_c1 < len(slides)-1: st.session_state.slide_c1 += 1; st.rerun()
        
    st.divider()
    slides[st.session_state.slide_c1]()