import streamlit as st
import pandas as pd
from helper import check_welfare_eligibility

def compliance_page():
    st.title("Welfare Scheme Eligibility")
    st.write("Check if you are eligible for government welfare schemes.")

    eligible_schemes = check_welfare_eligibility()
    if eligible_schemes:
        st.success("Congratulations! You are eligible for the following schemes:")
        for scheme in eligible_schemes:
            st.markdown(f"- **{scheme}**: [Apply Now](https://example.gov/apply)")
            with st.expander(f"View Pre-filled Form for {scheme}"):
                st.write(f"Name: {st.session_state['user_data'].get('username', '')}")
                st.write(f"Language Preference: {st.session_state['user_data'].get('language', '')}")
                st.button(f"Submit {scheme} Application (Simulated)")
    else:
        st.info("Based on your information, you are not currently eligible for any major welfare schemes.")

    st.subheader("Explore Other Schemes")
    st.write("Browse a list of available welfare schemes and check their criteria.")
    other_schemes_data = pd.DataFrame({
        'Scheme Name': ['Scholarship Program', 'Disability Support'],
        'Description': ['Financial aid for education.', 'Support for individuals with disabilities.']
    })
    st.dataframe(other_schemes_data, hide_index=True)

if __name__ == "__main__":
    compliance_page()
