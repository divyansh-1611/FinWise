import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from helper import recommend_investment, submit_loan_application


def banking_page():
    st.markdown('<h1 style="text-align: center;">Banking Services</h1>', unsafe_allow_html=True)

    # Account Balance
    st.markdown("<h3 style='text-align: Left;'>Account Balance</h3>", unsafe_allow_html=True)
    account_balance = sum(inv['amount'] for inv in st.session_state['investments']) * 1.02
    st.success(f"Your current balance is: ${account_balance:.2f}")

    # Transfer Funds
    with st.expander("Transfer Funds", expanded=False):
        with st.form("transfer_form"):
            transfer_to = st.text_input("Recipient Account")
            transfer_amount = st.number_input("Amount to Transfer", min_value=1.0, max_value=account_balance, step=10.0 )
            if st.form_submit_button("Transfer"):
                st.success(f"Successfully transferred ${transfer_amount:.2f} to {transfer_to}.")

    # Loan Application
    st.subheader("Apply for a Loan")
    with st.form("loan_application_form"):
        loan_amount = st.number_input("Loan Amount", min_value=100.00, step=100.00)
        loan_purpose = st.text_area("Purpose of Loan")
        if st.form_submit_button("Apply for Loan"):
            submit_loan_application(loan_amount, loan_purpose)

    # Loan Applications Table
    st.subheader("Your Loan Applications")
    if st.session_state['loan_applications']:
        df_loans = pd.DataFrame(st.session_state['loan_applications']).sort_values(by='date', ascending=False)
        df_loans['date'] = df_loans['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(df_loans[['date', 'amount', 'purpose', 'status']], hide_index=True)
    else:
        st.write("No loan applications submitted yet.")

    # Account Balance History
    st.subheader("Account Balance History")
    recommendation = recommend_investment() #calling a recommendation so that I can get the rate and calculate the balance for the history.
    balance_history_data = [{
    'date': inv['date'] - timedelta(days=np.random.randint(1, 30)), 
    'balance': inv['amount'] * (1 + int(recommendation['rate']) / 100 / 12) ** np.random.randint(1, 30)
    } for inv in st.session_state['investments']]
    df_balance_history = pd.DataFrame(balance_history_data).sort_values('date')
    fig_balance = px.line(df_balance_history, x='date', y='balance', title='Account Balance Trend')
    st.plotly_chart(fig_balance)


if __name__ == "__main__":
    banking_page()