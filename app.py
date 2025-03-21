import streamlit as st
import requests
import os
import pandas as pd

# Load environment variables
GROQ_API_KEY = "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"

# Initialize session state for bills and subscriptions
if "subscriptions" not in st.session_state:
    st.session_state.subscriptions = []

# Page Config
st.set_page_config(page_title="Automated Bill & Subscription Management", layout="wide")

# Page Title
st.title("💳 Automated Bill & Subscription Management")

# Function to call Groq API for processing requests
def call_groq_api(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 150,
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Section to add a subscription
st.sidebar.header("Add a Subscription")
subscription_name = st.sidebar.text_input("Subscription Name")
amount = st.sidebar.number_input("Amount", min_value=0.0, format="%.2f")
frequency = st.sidebar.selectbox("Frequency", ["Monthly", "Quarterly", "Yearly"])

if st.sidebar.button("Add Subscription"):
    if subscription_name and amount > 0:
        st.session_state.subscriptions.append({
            "name": subscription_name,
            "amount": amount,
            "frequency": frequency
        })
        st.success(f"Subscription '{subscription_name}' added successfully!")

# Display current subscriptions
st.header("Current Subscriptions")
if st.session_state.subscriptions:
    subscriptions_df = pd.DataFrame(st.session_state.subscriptions)
    st.dataframe(subscriptions_df)
else:
    st.warning("No subscriptions added yet.")

# Manage existing subscriptions (Delete)
if st.button("Delete Last Subscription"):
    if st.session_state.subscriptions:
        deleted = st.session_state.subscriptions.pop()
        st.success(f"Deleted subscription: {deleted['name']}")
    else:
        st.warning("No subscriptions to delete.")

# Call Groq API for advice or suggestions based on subscriptions
if st.button("Get Financial Advice"):
    if st.session_state.subscriptions:
        prompt = "Provide financial advice regarding the following subscriptions: " + ', '.join([sub['name'] for sub in st.session_state.subscriptions])
        advice = call_groq_api(prompt)
        st.subheader("Financial Advice")
        st.write(advice)
    else:
        st.warning("Add some subscriptions to receive advice.")

# Footer
st.markdown("---")
st.markdown("*Note: Ensure your subscriptions are properly tracked and budgeted.*")
