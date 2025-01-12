import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu  # Import the navigation bar component
from streamlit_lottie import st_lottie
import requests

# Import the helper functions (ensure this file exists and contains the functions)
from helper import simulate_signup, simulate_login, add_expense, get_personalized_budget, get_savings_suggestions, recommend_investment, make_investment, check_welfare_eligibility, submit_loan_application
# Import the page functions
from home import home_page
from learning import learning_page
from budgeting import budgeting_page
from investments import investments_page
from banking import banking_page
from compliance import compliance_page


lottie_url = "https://lottie.host/9cd46bae-89b2-41cb-8e85-76be21e9d559/O0tjvEkNY1.json"  # Replace with your Lottie animation URL

# --- Session State Management ---
if 'user_authenticated' not in st.session_state:
    st.session_state['user_authenticated'] = False
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}
if 'expenses' not in st.session_state:
    st.session_state['expenses'] = []
if 'investments' not in st.session_state:
    st.session_state['investments'] = []
if 'loan_applications' not in st.session_state:
    st.session_state['loan_applications'] = []
if 'learning_progress' not in st.session_state:
    st.session_state['learning_progress'] = {'lesson1': True, 'lesson2': False, 'lesson3': False}  # Mock lessons

# --- Navigation ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'login'

# --- Page Content ---

if not st.session_state['user_authenticated']:
    if st.session_state['current_page'] == 'login':
        st.title("Welcome to FinWise!")
        st.subheader("Login or Signup to get started.")

        auth_choice = st.radio("Choose an option:", ["Login", "Signup"])

        if auth_choice == "Login":
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if simulate_login(username, password):
                        st.session_state['current_page'] = 'home' # Navigate after successful login
                        st.rerun()  # Rerun to reflect the change

        elif auth_choice == "Signup":
            with st.form("signup_form"):
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                language_pref = st.selectbox("Preferred Language", ["English", "Spanish", "Hindi"]) # Add more languages
                literacy_pref = st.selectbox("Literacy Level", ["Beginner", "Intermediate", "Advanced"])
                if st.form_submit_button("Signup"):
                    simulate_signup(new_username, new_password, language_pref, literacy_pref)
                    if st.session_state['user_authenticated']:
                        st.session_state['current_page'] = 'home' # Navigate after successful signup
                        st.rerun() # Rerun to reflect the change

elif st.session_state['current_page'] != 'login':
    # --- Navigation Bar with Lottie Animation using streamlit-option-menu ---
    with st.sidebar:

        selected = option_menu(
            "Main Menu",
            ["Home", "Learning", "Budgeting", "Investments", "Banking", "Compliance"],
            icons=['house', 'book', 'piggy-bank', 'bar-chart', 'bank', 'shield-check'],
            menu_icon="cast",
            default_index=0,
        )
        st_lottie(lottie_url, key="finwise_animation", speed=1, loop=True)

    if selected == "Home":
        st.session_state['current_page'] = 'home'
    elif selected == "Learning":
        st.session_state['current_page'] = 'learning'
    elif selected == "Budgeting":
        st.session_state['current_page'] = 'budgeting'
    elif selected == "Investments":
        st.session_state['current_page'] = 'investments'
    elif selected == "Banking":
        st.session_state['current_page'] = 'banking'
    elif selected == "Compliance":
        st.session_state['current_page'] = 'compliance'

    # --- Page Content Display based on current_page ---
    if st.session_state['current_page'] == 'home':
        home_page()
    elif st.session_state['current_page'] == 'learning':
        learning_page()
    elif st.session_state['current_page'] == 'budgeting':
        budgeting_page()
    elif st.session_state['current_page'] == 'investments':
        investments_page()
    elif st.session_state['current_page'] == 'banking':
        banking_page()
    elif st.session_state['current_page'] == 'compliance':
        compliance_page()