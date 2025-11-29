import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# --- 基本設定 ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(page_title="kfcGPT – Taiwan Assistant", layout="wide")

st.title("🇹🇼 kfcGPT — Taiwan Real Estate • Law • Policy AI Assistant")
st.write("每天自動更新台中房價資料 + 台灣法律 + 政策 AI 解說")

# --- 側邊欄選單 ---
mode = st.sidebar.radio(
    "請選擇模式",
    ["🏠 房地產（台中）", "⚖️ 法律諮詢（台灣）", "🏛️ 政策解說（台灣）")

# --- 房地產模式 ---
if mode == "🏠 房地產（台中）"
    st.subheader("🏠 台中房價每日更新資料")

