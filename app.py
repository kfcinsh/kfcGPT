import streamlit as st
import os
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="kfcGPT Taiwan Assistant", layout="wide")

st.title("TW kfcGPT — Taiwan Real Estate / Law / Policy AI Assistant")
st.write("Daily updated Taichung real estate data + Taiwan law + public policy explanations.")

mode = st.sidebar.radio(
    "Select a mode:",
    ["Real Estate (Taichung)", "Legal Advice (Taiwan)", "Policy Explanation (Taiwan)"]
)

# Real Estate Mode
if mode == "Real Estate (Taichung)":
    st.subheader("Taichung Daily Real Estate Update")

    if os.path.exists("data/taichung_daily.txt"):
        with open("data/taichung_daily.txt", "r", encoding="utf-8") as f:
            report = f.read()
        st.text(report)
    else:
        st.write("No real estate data available yet.")

# Legal Mode
elif mode == "Legal Advice (Taiwan)":
    st.subheader("Taiwan Legal AI")

    q = st.text_input("Enter your legal question:")

    if st.button("Submit Legal Question"):
        if q:
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a Taiwan legal advisor AI."},
                    {"role": "user", "content": q}
                ]
            )
            st.write(reply.choices[0].message.content)

# Policy Mode
elif mode == "Policy Explanation (Taiwan)":
    st.subheader("Taiwan Policy AI")

    q = st.text_input("Enter your policy question:")

    if st.button("Submit Policy Question"):
        if q:
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a Taiwan public policy analyst AI."},
                    {"role": "user", "content": q}
                ]
            )
            st.write(reply.choices[0].message.content)
