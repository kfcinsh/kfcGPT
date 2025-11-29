import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# 基本設定
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(page_title="kfcGPT - Taiwan Assistant", layout="wide")

st.title("tw kfcGPT - Taiwan Real Estate • Law • Policy AI Assistant")
st.write("每天自動更新台中房價資料 + 台灣法律 + 政策 AI 解說")

# 側邊選單
mode = st.sidebar.radio(
    "請選擇模式：",
    ["🏠 房地產（台中）", "⚖️ 法律諮詢（台灣）", "📘 政策解說（台灣）"]
)

# --- 房地產模式 ---
if mode == "🏠 房地產（台中）":
    st.subheader("🏠 台中房價每日更新資料")

    if os.path.exists("data/taichung_daily.txt"):
        with open("data/taichung_daily.txt", "r", encoding="utf-8") as f:
            report = f.read()
        st.text(report)
    else:
        st.write("目前尚沒有房價資料（等待 GitHub Actions 自動更新）")

# --- 法律諮詢 ---
elif mode == "⚖️ 法律諮詢（台灣）":
    st.subheader("⚖️ 台灣法律 AI 問答")
    q = st.text_input("請輸入法律問題：")
    if st.button("送出法律問題"):
        if q:
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": f"你是台灣法律顧問，請回答：{q}"}]
            )
            st.write(reply.choices[0].message.content)

# --- 政策解說 ---
elif mode == "📘 政策解說（台灣）":
    st.subheader("📘 台灣政策 AI 解說")
    q = st.text_input("請輸入政策問題：")
    if st.button("送出政策問題"):
        if q:
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": f"請用台灣民眾聽得懂的方式解釋政策：{q}"}]
            )
            st.write(reply.choices[0].message.content)
