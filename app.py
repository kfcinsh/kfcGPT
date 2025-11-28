import streamlit as st
import os
from pathlib import Path
from openai import OpenAI

st.set_page_config(page_title="kfcGPT", layout="wide")

st.title("🇹🇼 kfcGPT — Taiwan Real Estate AI Assistant")
st.markdown("每天自動更新台中市房地產資料 · 使用 ChatGPT API")

# 讀取每日房價資料
def load_taichung_daily():
    path = Path("data/taichung_daily.txt")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "目前尚無房價資料（等待首次自動更新）。"

daily_report = load_taichung_daily()

# 輸入區
question = st.text_input("請輸入想問的問題（房價、政策、資料查詢皆可）")

if st.button("送出"):
    if not question.strip():
        st.warning("請輸入問題！")
    else:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
你是一個台灣房地產與政策專家 AI。
以下是每天自動更新的台中市房價資料（來自 GitHub Actions）：

{daily_report}

使用台灣常用語氣，清楚、簡潔回答使用者問題：
「{question}」
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        st.subheader("💡 回覆：")
        st.write(response.choices[0].message.content)
