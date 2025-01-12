import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from helper import add_expense, get_personalized_budget, get_savings_suggestions


def budgeting_page():
    st.markdown("<h1 style='text-align: center;'>Budgeting and Savings</h1>", unsafe_allow_html=True)

    with st.expander("Log New Expense", expanded=False):
        with st.form("add_expense_form"):
            expense_description = st.text_input("Description")
            expense_amount = st.number_input("Amount", min_value=0.01)
            expense_category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Other"])
            if st.form_submit_button("Add Expense"):
                add_expense(expense_description, expense_amount, expense_category)

    st.subheader("Your Budget")
    budget = get_personalized_budget()
    if budget:
        budget_data = pd.DataFrame(list(budget.items()), columns=['Category', 'Budgeted Amount'])
        spent_data = pd.DataFrame([
            {'Category': cat, 'Spent': sum(exp['amount'] for exp in st.session_state['expenses'] if exp['category'] == cat)}
            for cat in budget.keys()
        ])
        merged_data = pd.merge(budget_data, spent_data, on='Category', how='left').fillna(0)
        merged_data['Remaining'] = merged_data['Budgeted Amount'] - merged_data['Spent']

        fig_budget = px.bar(merged_data, x='Category', y=['Budgeted Amount', 'Spent', 'Remaining'], barmode='group',
                            labels={'value': 'Amount', 'variable': 'Type'})
        st.plotly_chart(fig_budget)
    else:
        st.write("No budget available yet. More data needed.")

    st.subheader("Savings Suggestions")
    suggestions = get_savings_suggestions()
    for suggestion in suggestions:
        st.info(suggestion)

    if st.session_state['expenses']:
        st.subheader("Expense Breakdown")
        df_expenses = pd.DataFrame(st.session_state['expenses'])
        fig_pie = px.pie(df_expenses, names='category', values='amount', title='Expenses by Category')
        st.plotly_chart(fig_pie)

if __name__ == "__main__":
    budgeting_page()