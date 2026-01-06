import streamlit as st
import random
import time

st.set_page_config(page_title="Probability", page_icon="🎲")
if 'xp' not in st.session_state: st.session_state.xp = 0
with st.sidebar: st.header(f"🎓 XP: {st.session_state.xp}")

st.title("🎲 Probability & Statistics")

tab1, tab2 = st.tabs(["📚 Learn", "📝 Practice"])

with tab1:
    st.header("The Mean (Average)")
    st.write("Add up all the numbers, then divide by how many numbers there are.")
    st.latex(r"\bar{x} = \frac{\sum x}{n}")

with tab2:
    if 'prob_nums' not in st.session_state:
        # Generate 3 random numbers
        st.session_state.prob_nums = [random.randint(1, 10) for _ in range(3)]

    nums = st.session_state.prob_nums
    correct_mean = sum(nums) / len(nums)
    
    st.write(f"Find the mean of these numbers: **{nums}**")
    
    # Format %.2f allows 2 decimal places
    user_ans = st.number_input("Mean =", format="%.2f")
    
    if st.button("Check Mean"):
        # Allow a small error margin for decimals
        if abs(user_ans - correct_mean) < 0.1:
            st.balloons()
            st.success("Correct! +15 XP")
            st.session_state.xp += 15
            del st.session_state['prob_nums']
            time.sleep(1.5)
            st.rerun()
        else:
            st.error(f"Hint: ({nums[0]} + {nums[1]} + {nums[2]}) / 3")