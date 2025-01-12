import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie

lottie_url = "https://lottie.host/47c4d828-2aaf-4bea-b0f4-e5655a927505/y6Q7dbwGee.json"


def learning_page():

    st.markdown("<h1 style='text-align: center;'>Financial Literacy Lessons</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
            .centered-text {
                text-align: center;
                padding-left: 6em;
                padding-right: 1em;
                max-width: 600px;
                line-height: 1.6;
                font-size: 18px;
            }
        </style>
        <p class='centered-text'>
            Empower yourself with essential <b>financial knowledge!</b> Our interactive lessons are designed to help women in rural areas build 
            <b>smart money habits, manage savings, and create brighter futures</b> for their families.
        </p>
        """, 
        unsafe_allow_html=True
    )


    st_lottie(lottie_url, speed=1, key="animation")
    lesson_options = ["Understanding Budgets", "Saving Strategies", "Introduction to Investments"]
    selected_lesson = st.selectbox("Select a Lesson", lesson_options)

    if selected_lesson == "Understanding Budgets":
        st.subheader("Lesson 1: Understanding Budgets") 
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <iframe width="800" height="450" src="https://www.youtube.com/embed/sVKQn2I4HDM" 
                title="Budgeting Basics!" frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
                encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen></iframe>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.checkbox("Mark as Complete"):
            st.session_state['learning_progress']['lesson1'] = True

    elif selected_lesson == "Saving Strategies":
        st.subheader("Lesson 2: Saving Strategies")
        st.write("Learn different ways to save money effectively...")
        st.image("https://via.placeholder.com/300x150?text=Saving+Visual", width=300)
        if st.checkbox("Mark as Complete"):
            st.session_state['learning_progress']['lesson2'] = True

    elif selected_lesson == "Introduction to Investments":
        st.subheader("Lesson 3: Introduction to Investments")
        st.write("Discover the basics of investing and how it can grow your wealth...")
        st.image("https://via.placeholder.com/300x150?text=Investment+Visual", width=300)
        if st.checkbox("Mark as Complete"):
            st.session_state['learning_progress']['lesson3'] = True

    st.subheader("Your Learning Progress")
    progress_data = pd.DataFrame({
        'Lesson': ['Understanding Budgets', 'Saving Strategies', 'Introduction to Investments'],
        'Completed': [st.session_state['learning_progress']['lesson1'], st.session_state['learning_progress']['lesson2'], st.session_state['learning_progress']['lesson3']]
    })
    fig_progress = px.bar(progress_data, x='Lesson', y='Completed', color='Completed',
                         color_discrete_map={True: 'green', False: 'red'})
    st.plotly_chart(fig_progress)

if __name__ == "__main__":
    learning_page()