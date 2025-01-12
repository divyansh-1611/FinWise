# helper.py
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px


def simulate_signup(username, password, language, literacy):
    st.session_state['user_data']['username'] = username
    st.session_state['user_data']['password'] = password
    st.session_state['user_data']['language'] = language
    st.session_state['user_data']['literacy'] = literacy
    st.session_state['user_authenticated'] = True
    st.success("Signup successful!")


def simulate_login(username, password):
    if 'username' in st.session_state['user_data'] and st.session_state['user_data']['username'] == username and \
            st.session_state['user_data']['password'] == password:
        st.session_state['user_authenticated'] = True
        st.success("Login successful!")
        return True
    else:
        st.error("Invalid username or password.")
        return False


def add_expense(description, amount, category):
    st.session_state['expenses'].append(
        {'date': datetime.now(), 'description': description, 'amount': amount, 'category': category})
    st.success("Expense added!")


def get_personalized_budget():
    if 'income' in st.session_state['user_data']:
        income = st.session_state['user_data']['income']
        return {
            'Food': income * 0.3,
            'Rent': income * 0.3,
            'Utilities': income * 0.1,
            'Savings': income * 0.2,
            'Other': income * 0.1
        }
    return {}


def get_savings_suggestions():
    total_spent = sum(expense['amount'] for expense in st.session_state['expenses'])
    budget = get_personalized_budget()
    suggestions = []
    for category, budget_amount in budget.items():
        category_spent = sum(
            expense['amount'] for expense in st.session_state['expenses'] if expense['category'] == category)
        if category_spent > budget_amount:
            suggestions.append(f"Consider reducing spending on {category}.")
    if not suggestions:
        suggestions.append("You are doing well with your budget!")
    return suggestions


def recommend_investment():
    return {"name": "Fixed Deposit", "rate": "5", "risk": "Low", "min_amount": 100}


def make_investment(amount, investment_name):
    st.session_state['investments'].append({'date': datetime.now(), 'name': investment_name, 'amount': amount})
    st.success(f"Investment in {investment_name} successful!")


def check_welfare_eligibility():
    if 'income' in st.session_state['user_data'] and st.session_state['user_data']['income'] < 1000:
        return ["Food Assistance Program", "Healthcare Subsidy"]
    return []


def submit_loan_application(amount, purpose):
    st.session_state['loan_applications'].append(
        {'date': datetime.now(), 'amount': amount, 'purpose': purpose, 'status': 'Pending'})
    st.success("Loan application submitted!")


def display_budget_info():
    st.subheader("Your Budget")
    budget = get_personalized_budget()
    if budget:
        budget_data = pd.DataFrame(list(budget.items()), columns=['Category', 'Budgeted Amount'])
        spent_data = pd.DataFrame([
            {'Category': cat,
             'Spent': sum(exp['amount'] for exp in st.session_state['expenses'] if exp['category'] == cat)}
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


def display_investment_info():
    st.subheader("Recommended Investment")
    recommendation = recommend_investment()
    st.write(
        f"Consider investing in **{recommendation['name']}** with a rate of **{recommendation['rate']}** (Risk: {recommendation['risk']}). Minimum amount: ${recommendation['min_amount']}.")

    st.subheader("Your Investments")
    if st.session_state['investments']:
        df_investments = pd.DataFrame(st.session_state['investments']).sort_values(by='date', ascending=False)
        df_investments['date'] = df_investments['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(df_investments[['date', 'name', 'amount']], hide_index=True)

        st.subheader("Investment Growth Over Time")
        investment_growth_data = []
        cumulative_amount = 0
        for inv in sorted(st.session_state['investments'], key=lambda x: x['date']):
            cumulative_amount += inv['amount']
            investment_growth_data.append({
                'date': inv['date'],
                'value': cumulative_amount * (1 + int(recommendation['rate']) / 100 / 12) ** (
                            (datetime.now() - inv['date']).days / 30)
            })

        df_growth = pd.DataFrame(investment_growth_data)
        fig_growth = px.line(df_growth, x='date', y='value', title='Investment Portfolio Value')
        st.plotly_chart(fig_growth)
    else:
        st.write("You haven't made any investments yet.")