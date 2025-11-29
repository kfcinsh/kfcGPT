from datetime import datetime, timedelta, timezone
from pathlib import Path

# 設定台灣時間
tz = timezone(timedelta(hours=8))
today = datetime.now(tz)
date_str = today.strftime("%Y/%m/%d")

# 目前先使用示範用的固定房價數字（之後要接政府資料再改）
prices = {
    "北屯區": 43.5,
    "西屯區": 48.1,
    "南屯區": 41.3,
    "烏日區": 28.7,
}

# 建立 data 資料夾（如果已經存在就略過）
Path("data").mkdir(exist_ok=True)

# 寫入 data/taichung_daily.txt
output_path = Path("data") / "taichung_daily.txt"

with output_path.open("w", encoding="utf-8") as f:
    f.write(f"{date_str} 台中房價每日更新：\n\n")
    for area, price in prices.items():
        f.write(f"- {area}：單價 {price} 萬/坪\n")
    f.write("\n(此為測試資料)\n")

print(f"已更新 {output_path}")
