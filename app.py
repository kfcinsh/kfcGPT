import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# 基本設定
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(page_title="kfcGPT - Taiwan Assistant", layout="wide")

st.title("tw kfcGPT - Taiwan Real Estate • Law • Policy AI Assistant")
st.write("每天自動更新台中房價資料、台灣法律、政策 AI 解說")

# 側邊選單
mode = st.sidebar.radio(
    "請選擇模式：",
    ["房地產（台中）", "法律諮詢（台灣）", "政策解說（台灣）"]
)

# 房地產模式
if mode == "房地產（台中）":
    st.subheader("台中房價每日更新資料")

    data_path = "taichung_daily.txt"

    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            daily_data = f.read()
        st.text(daily_data)
    else:
        st.write("目前尚無資料（等待 GitHub Action 自動更新）")

# ================================
# 共用 ChatGPT 問答函式
# ================================
def ask_gpt(question):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一個專業的台灣法律與政策助理，使用繁體中文回答。"},
            {"role": "user", "content": question}
        ]
    )
    return completion.choices[0].message.content

# 法律諮詢
if mode == "法律諮詢（台灣）":
    st.subheader("台灣法律 AI 解答")
    q = st.text_area("請輸入你的法律問題：")
    if st.button("送出"):
        st.write(ask_gpt(q))

# 政策解說
if mode == "政策解說（台灣）":
    st.subheader("台灣政策 AI 解說")
    q = st.text_area("請輸入你的政策問題：")
    if st.button("送出"):
        st.write(ask_gpt(q))
