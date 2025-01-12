import streamlit as st
from helper import add_expense, display_budget_info, display_investment_info

def home_page():
    st.title("Welcome to your FinWise Dashboard!")
    st.write(f"Hello, {st.session_state['user_data'].get('username', 'User')}!")

    # Income Form
    with st.expander("Set Your Income", expanded=True):
        with st.form("income_form"):
            income = st.number_input("Enter your monthly income", min_value=0.0, step=100.0)
            if st.form_submit_button("Set Income"):
                st.session_state['user_data']['income'] = income
                st.success("Income set successfully!")

    st.subheader("Key Highlights")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Savings", f"${sum(inv['amount'] for inv in st.session_state['investments']):.2f}")
    with col2:
        available_funds = sum(inv['amount'] for inv in st.session_state['investments']) * 1.02
        st.metric("Available Funds", f"${available_funds:.2f}")
    with col3:
        st.metric("Budget Compliance", "85%", "+5%")

    st.subheader("Quick Actions")
    # New layout of the Buttons
    with st.container():
        action_cols = st.columns(3)
        with action_cols[0]:
            if st.button("Add Expense"):
                st.session_state['expense_modal'] = True
        with action_cols[1]:
            if st.button("View Budget"):
                st.session_state['show_budget'] = not st.session_state.get('show_budget', False)
                st.session_state['expense_modal'] = False # Close the modal if any other button is pressed
        with action_cols[2]:
            if st.button("Explore Investments"):
                st.session_state['show_investments'] = not st.session_state.get('show_investments', False)
                st.session_state['expense_modal'] = False # Close the modal if any other button is pressed

    if 'expense_modal' in st.session_state and st.session_state['expense_modal']:
        with st.container():
            st.subheader("Add Expense")
            with st.form("add_expense_form_modal"):
                expense_description_modal = st.text_input("Description")
                expense_amount_modal = st.number_input("Amount", min_value=0.01)
                expense_category_modal = st.selectbox("Category", ["Food", "Rent", "Utilities", "Other"])
                if st.form_submit_button("Add"):
                    add_expense(expense_description_modal, expense_amount_modal, expense_category_modal)
                    st.session_state['expense_modal'] = False
                    st.rerun()
            if st.button("Close"):
                st.session_state['expense_modal'] = False
                st.rerun()

    if st.session_state.get('show_budget', False):
        display_budget_info()

    if st.session_state.get('show_investments', False):
        display_investment_info()

    st.subheader("Recent Transactions")
    if st.session_state['expenses']:
        df_expenses = pd.DataFrame(st.session_state['expenses']).sort_values(by='date', ascending=False).head(5)
        df_expenses['date'] = df_expenses['date'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(df_expenses[['date', 'description', 'amount', 'category']], hide_index=True)
    else:
        st.write("No recent transactions.")

if __name__ == "__main__":
    home_page()