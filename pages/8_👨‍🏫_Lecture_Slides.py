import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. PAGE SETUP (Wide mode looks better for slides)
st.set_page_config(page_title="Lecture Slides", page_icon="👨‍🏫", layout="wide")

# 2. DEFINE YOUR SLIDES (The Content)
# This is a list of functions. Each function represents one slide.
def slide_1_intro():
    st.header("👋 Lecture 1: Introduction to Calculus")
    st.write("### Welcome to Class!")
    st.write("Today we will cover:")
    st.write("- Limits")
    st.write("- Derivatives")
    st.write("- Integrals")
    st.info("Please open your notebooks.")

def slide_2_limits():
    st.header("🛑 Topic 1: Limits")
    st.write("A limit tells us the value that a function approaches as the input approaches some value.")
    st.latex(r"\lim_{x \to a} f(x) = L")
    st.write("Even if the function is undefined at $a$, the limit can still exist.")

def slide_3_graph():
    st.header("📈 Visualizing a Function")
    st.write("Let's look at the graph of $y = x^2$")
    
    # You can put REAL Python code inside your slide!
    x = np.linspace(-10, 10, 100)
    y = x**2
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.grid(True)
    st.pyplot(fig)

def slide_4_quiz():
    st.header("🧠 Quick Check")
    st.write("What is the derivative of $x^2$?")
    if st.button("Show Answer"):
        st.success("The answer is $2x$")

def slide_5_end():
    st.header("🏁 Class Dismissed")
    st.write("### Homework:")
    st.write("1. Complete the Quiz on Page 5")
    st.write("2. Join the Leaderboard")
    st.balloons()

# List of your slides in order
slides = [
    slide_1_intro,
    slide_2_limits,
    slide_3_graph,
    slide_4_quiz,
    slide_5_end
]

# 3. NAVIGATION LOGIC
if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0

# --- 3. NAVIGATION & RESOURCES (Sidebar) ---
with st.sidebar:
    st.title("🔧 Controls")
    
    # A. NAVIGATION
    st.subheader("Jump to Slide")
    slide_names = [f"Slide {i+1}" for i in range(len(slides))]
    selected_slide = st.radio("Go to:", range(len(slides)), format_func=lambda x: slide_names[x], index=st.session_state.slide_index)

    if selected_slide != st.session_state.slide_index:
        st.session_state.slide_index = selected_slide
        st.rerun()
    
    st.divider()

    # B. DIGITAL LIBRARY (Multiple Books)
    st.subheader("📚 Digital Library")
    
    # 1. DEFINE YOUR BOOKS HERE
    # Format: "Button Name": "ExactFilename.pdf"
    book_list = {
        "📘 Advanced Math Slide": "SlideToanCaoCap.pdf",
        "📕 Specialized Math Slide": "SlideToanChuyenDe.pdf",
        "📗 Formula Cheat Sheet": "formulas.pdf",
        "📄 Homework Set 1": "homework1.pdf"
    }

    # 2. GENERATE BUTTONS AUTOMATICALLY
    for display_name, file_name in book_list.items():
        try:
            with open(file_name, "rb") as pdf_file:
                st.download_button(
                    label=display_name,
                    data=pdf_file,
                    file_name=file_name,
                    mime="application/pdf",
                    use_container_width=True
                )
        except FileNotFoundError:
            # If you haven't uploaded the file yet, we show a helpful error
            st.warning(f"⚠️ Missing file: {file_name}")

    st.divider()

    # C. PRINT INSTRUCTIONS
    with st.expander("🖨️ How to Print Slides"):
        st.write("1. Press **Ctrl + P**.")
        st.write("2. Select **'Save as PDF'**.")
        st.write("3. Click **Save**.")

# 4. RENDER THE CURRENT SLIDE
# Create a container for the slide content
with st.container():
    st.markdown("---") # Top line
    # CALL THE FUNCTION FOR THE CURRENT SLIDE
    slides[st.session_state.slide_index]()
    st.markdown("---") # Bottom line

# 5. FOOTER BUTTONS (Prev / Next)
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    if st.button("⬅️ Previous"):
        if st.session_state.slide_index > 0:
            st.session_state.slide_index -= 1
            st.rerun()

with col2:
    # Display "Slide X of Y" in the center
    st.markdown(f"<div style='text-align: center; color: gray;'>Slide {st.session_state.slide_index + 1} of {len(slides)}</div>", unsafe_allow_html=True)

with col3:
    if st.button("Next ➡️"):
        if st.session_state.slide_index < len(slides) - 1:
            st.session_state.slide_index += 1
            st.rerun()