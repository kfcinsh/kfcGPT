import streamlit as st
import os
from openai import OpenAI
import pandas as pd

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit 頁面設定
st.set_page_config(page_title="kfcGPT Taiwan Assistant", layout="wide")

# 標題
st.title("TW kfcGPT — Taiwan Real Estate • Law • Policy AI Assistant")
st.write("每天自動更新台中房價資料 + 台灣法律解說 + 台灣政策說明")

# 側邊欄選單
mode = st.sidebar.radio(
    "請選擇模式：",
    ["房地產（台中）", "法律諮詢（台灣）", "政策解說（台灣）"]
)

# ------------------------
# 房地產模式
# ------------------------
if mode == "房地產（台中）":
    st.subheader("台中房價每日更新資料")

    if os.path.exists("data/taichung_daily.txt"):
        with open("data/taichung_daily.txt", "r", encoding="utf-8") as f:
            report = f.read()
        st.text(report)
    else:
        st.write("目前尚無房價資料（等待自動更新功能上線）")

# ------------------------
# 法律模式
# ------------------------
elif mode == "法律諮詢（台灣）":
    st.subheader("台灣法律 AI 回答")

    q = st.text_input("請輸入你的法律問題：")

    if st.button("送出法律問題"):
        if q:
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一位台灣法律 AI 顧問。"},
                    {"role": "user", "content": q}
                ]
            )
            st.write(reply.choices[0].message.content)

# ------------------------
# 政策模式
# ------------------------
elif mode == "政策解說（台灣）":
    st.subheader("台灣政策 AI 解說")

    q = st.text_input("請輸入你想了解的政策問題：")

    if st.button("送出政策問題"):
        if q:
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一位台灣公共政策 AI 分析顧問。"},
                    {"role": "user", "content": q}
                ]
            )
            st.write(reply.choices[0].message.content)

