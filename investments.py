import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from helper import recommend_investment, make_investment
import requests
import json

OLLAMA_URL = "http://127.0.0.1:1234/v1/completions"
# Replace with your Ollama server URL if different


def investments_page():
    st.markdown("<h1 style='text-align: center;'>Explore Investment Options</h1>", unsafe_allow_html=True)
    
    # --- Ollama Integration ---
    st.markdown("<h4 style='text-align: left'>Personalized Investment Queries with Ollama</h4>", unsafe_allow_html=True)
    
    ollama_prompt = st.text_area("Enter your investment query:", height=150)

    if st.button("Get Response from LLaMA"):
        if ollama_prompt:
            try:
                # Adjusted payload for OpenAI-like API
                payload = {
                    "model": "llama-3.2-3b-instruct",  # Replace with your model identifier
                    "prompt": ollama_prompt,
                    "max_tokens": 200,  # You can adjust this
                    "temperature": 0.7,  # For randomness in responses
                    "stream": False,
                }

                # Send POST request
                response = requests.post(OLLAMA_URL, json=payload)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

                # Extracting the response text
                json_resp = response.json()
                ollama_response = json_resp["choices"][0]["text"]  # Assuming OpenAI-like API

                st.subheader("LLaMA Response:")
                st.write(ollama_response)

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the LLaMA server: {e}")
            except KeyError as e:
                st.error(f"Error parsing LLaMA response: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter a prompt.")
    # --- Existing Investments Page Content ---

    if 'investments' not in st.session_state:
        st.session_state['investments'] = []

    # Dummy data for recommendations (replace with actual logic)
    def recommend_investment():
        return {'name': 'Fixed Deposit', 'rate': '7%', 'risk': 'Medium', 'min_amount': 100}

    # Dummy function to make an investment (replace with actual logic)
    def make_investment(amount, investment_name):
        st.session_state['investments'].append({'date': datetime.now(), 'name': investment_name, 'amount': amount})
        st.success(f"Successfully invested ${amount} in {investment_name}!")

    recommendation = recommend_investment()
    st.write(f"Consider investing in **{recommendation['name']}** with a rate of **{recommendation['rate']}** (Risk: {recommendation['risk']}). Minimum amount: ${recommendation['min_amount']}.")

    with st.expander("Invest Now", expanded=False):
        with st.form("investment_form", clear_on_submit=True):
            st.write("### Fill in your Investment Goals")
            invest_amount = st.number_input("Investment Amount", min_value=recommendation['min_amount'])
            investment_goal = st.selectbox("Investment Goal", ["Retirement", "Education", "House Down Payment", "Short-term Savings", "Other"])
            investment_duration = st.slider("Investment Duration (Years)", min_value=1, max_value=30, value=5)
            risk_tolerance = st.select_slider("Risk Tolerance", options=["Low", "Medium", "High"], value="Medium")
            funding_source = st.selectbox("Investment Type", ["Fixed Deposit", "Recurring Desposit", "SIP", "Mutual Funds"])
            notes = st.text_area("Additional Notes (Optional)")

            if st.form_submit_button("Invest Now"):
                make_investment(invest_amount, recommendation['name'])
                # You can also store the additional form data if needed
                print(f"Goal: {investment_goal}, Duration: {investment_duration}, Risk: {risk_tolerance}, Source: {funding_source}, Notes: {notes}")



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
                'value': cumulative_amount * (1 + int(recommendation['rate'].replace('%', '')) / 100 / 12) ** ((datetime.now() - inv['date']).days / 30)
            })

        df_growth = pd.DataFrame(investment_growth_data)
        fig_growth = px.line(df_growth, x='date', y='value', title='Investment Portfolio Value')
        st.plotly_chart(fig_growth)
    else:
        st.write("You haven't made any investments yet.")

if __name__ == "__main__":
    investments_page()