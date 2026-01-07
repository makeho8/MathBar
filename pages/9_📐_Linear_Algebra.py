import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
TOPIC_NAME = "Linear Algebra"
TOPIC_ICON = "📐"

st.set_page_config(page_title=TOPIC_NAME, page_icon=TOPIC_ICON, layout="wide")
st.title(f"{TOPIC_ICON} {TOPIC_NAME}")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📚 Content", "📝 Practice", "👨‍🏫 Slides"])

# --- TAB 1: CONTENT ---
with tab1:
    st.header("1. Vectors & Matrices")
    st.write("Linear algebra is the language of data. It deals with vectors (arrows) and matrices (spreadsheets of numbers).")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Visualizing a Vector")
        # Interactive Vector Plot
        vx = st.slider("X Component", -5.0, 5.0, 2.0)
        vy = st.slider("Y Component", -5.0, 5.0, 3.0)
        
        fig, ax = plt.subplots()
        ax.quiver(0, 0, vx, vy, angles='xy', scale_units='xy', scale=1, color='blue')
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.grid(True)
        ax.set_aspect('equal')
        st.pyplot(fig)

    with col2:
        st.subheader("Matrix Multiplication")
        st.latex(r"A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}, \quad B = \begin{bmatrix} x \\ y \end{bmatrix}")
        st.info("Matrix multiplication transforms a vector into a new vector.")

# --- TAB 2: PRACTICE ---
with tab2:
    st.header("🧠 Skill Check")
    
    st.write("**Question 1:** What is the determinant of this identity matrix?")
    st.latex(r"I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}")
    
    ans = st.radio("Select Answer:", ["0", "1", "2", "Undefined"], key="la_q1")
    if st.button("Check Answer", key="btn_la_q1"):
        if ans == "1":
            st.success("Correct! The determinant of Identity is always 1.")
        else:
            st.error("Try again.")

# --- TAB 3: SLIDES ---
with tab3:
    st.write("### 📽️ Lecture Slides")
    
    if 'slide_la' not in st.session_state: st.session_state.slide_la = 0
    
    def s1():
        st.header("Topic: Linear Independence")
        st.write("Vectors are independent if no vector can be written as a combo of others.")
    def s2():
        st.header("Topic: Eigenvalues")
        st.latex(r"A \vec{v} = \lambda \vec{v}")
        st.write("Eigenvectors don't change direction, only length.")
    
    slides = [s1, s2]
    
    # Navigation
    c1, c2, c3 = st.columns([1,2,1])
    if c1.button("⬅️ Prev", key="la_prev"):
        if st.session_state.slide_la > 0: st.session_state.slide_la -= 1; st.rerun()
    if c3.button("Next ➡️", key="la_next"):
        if st.session_state.slide_la < len(slides)-1: st.session_state.slide_la += 1; st.rerun()
        
    st.divider()
    slides[st.session_state.slide_la]()