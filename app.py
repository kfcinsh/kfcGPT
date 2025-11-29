import streamlit as st
import os
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="kfcGPT 台灣房地產／法律／政策小幫手", layout="wide")

st.title("TW kfcGPT —— 台灣房地產／法律／政策 AI 助理")
st.write("每天更新台中房價資料，並提供台灣法律說明與公共政策解析。")

mode = st.sidebar.radio(
    "請選擇模式：",
    ["台中房地產行情", "台灣法律諮詢", "台灣政策說明"]
)
# Real Estate Mode
if mode == "台中房地產行情":
    st.subheader("台中房價每日更新")

    if os.path.exists("data/taichung_daily.txt"):
        with open("data/taichung_daily.txt", "r", encoding="utf-8") as f:
            report = f.read()
        st.text(report)
    else:
        st.write("目前尚無房地產資料。")


# Legal Mode
elif mode == "台灣法律諮詢":
    st.subheader("台灣法律 AI")

    q = st.text_input("請輸入您的法律問題：")

    if q:
        reply = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一位台灣法律顧問 AI，請以台灣現行法律為基礎提供清楚、易懂的分析。"},
                {"role": "user", "content": q}
            ]
        )
        st.write(reply.choices[0].message.content)

# Policy Mode
elif mode == "台灣政策說明":
    st.subheader("台灣政策解析 AI")

    q = st.text_input("請輸入您想了解的政策問題：")

    if st.button("提交政策問題"):
        if q:
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一位台灣公共政策分析 AI，請用清楚、易懂的方式說明政府政策與制度。"},
                    {"role": "user", "content": q}
                ]
            )
            st.write(reply.choices[0].message.content)

