import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# --- CONFIGURATION ---
TOPIC_NAME = "Multi-Variable Calculus"
TOPIC_ICON = "∬"

st.set_page_config(page_title=TOPIC_NAME, page_icon=TOPIC_ICON, layout="wide")
st.title(f"{TOPIC_ICON} {TOPIC_NAME}")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📚 Content", "📝 Practice", "👨‍🏫 Slides"])

# --- TAB 1: CONTENT ---
with tab1:
    st.header("Partial Derivatives")
    st.write("In 3D, we can check the slope along the X-axis or the Y-axis separately.")
    st.latex(r"\nabla f = \left[ \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right]")

    st.subheader("3D Surface Plotter")
    # 3D Plotting
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) # Ripple function
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    st.pyplot(fig)

# --- TAB 2: PRACTICE ---
with tab2:
    st.header("🧠 3D Quiz")
    
    st.write("**Question 1:** If $f(x,y) = x^2 + y^2$, what is $\\frac{\\partial f}{\\partial x}$?")
    st.info("Hint: Treat 'y' as a constant number.")
    ans = st.radio("Select Answer:", ["2x", "2y", "2x + 2y", "0"], key="calc2_q1")
    
    if st.button("Check Answer", key="btn_c2"):
        if ans == "2x":
            st.success("Correct! Since 'y' is constant, its derivative is 0.")
        else:
            st.error("Treat y like a number (e.g., 5). Derivative of 5^2 is 0.")

# --- TAB 3: SLIDES ---
with tab3:
    st.write("### 📽️ Lecture Slides")
    if 'slide_c2' not in st.session_state: st.session_state.slide_c2 = 0
    
    def s1():
        st.header("The Gradient Vector")
        st.write("The Gradient points in the direction of steepest ascent.")
    def s2():
        st.header("Double Integrals")
        st.write("Volume under a surface.")
        st.latex(r"\iint_D f(x,y) \,dA")
    
    slides = [s1, s2]
    
    c1, c2, c3 = st.columns([1,2,1])
    if c1.button("⬅️ Prev", key="c2_prev"):
        if st.session_state.slide_c2 > 0: st.session_state.slide_c2 -= 1; st.rerun()
    if c3.button("Next ➡️", key="c2_next"):
        if st.session_state.slide_c2 < len(slides)-1: st.session_state.slide_c2 += 1; st.rerun()
        
    st.divider()
    slides[st.session_state.slide_c2]()