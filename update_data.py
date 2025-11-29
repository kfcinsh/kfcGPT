import pandas as pd
import requests
import zipfile
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta, timezone

# 設定台灣時間
tz = timezone(timedelta(hours=8))
today = datetime.now(tz)
date_str = today.strftime("%Y/%m/%d")

# 正確政府資料 ZIP 檔網址
url = "https://plvr.land.moi.gov.tw/Download?type=zip&fileName=lvr_land_A.zip"

print("下載不動產成交 ZIP 檔中...")
response = requests.get(url)
response.raise_for_status()

zip_file = zipfile.ZipFile(BytesIO(response.content))

# ZIP 內的真正檔名
csv_name = "A_lvr_land_A.CSV"

df = pd.read_csv(zip_file.open(csv_name), encoding="big5")

# 只抓台中市資料（縣市欄=台中市）
df = df[df["鄉鎮市區"].notna()]

# 關鍵字
residential_keywords = ["華厦", "住宅", "公寓", "透天", "店面", "大樓"]

# 篩選「房屋類型」
df = df[df["建物型態"].astype(str).str.contains("|".join(residential_keywords))]

# 各行政區平均單價
result = df.groupby("鄉鎮市區")["單價元平方公尺"].mean().sort_values()

# 換算成「萬/坪」
def convert(x):
    return round((x / 10000) * 3.3058, 1)

result = result.apply(convert)

# 建立輸出資料夾
Path("data").mkdir(exist_ok=True)

# 更新至 data/taichung_daily.txt
with open("data/taichung_daily.txt", "w", encoding="utf-8") as f:
    f.write(f"{date_str} 台中房價每日更新：\n\n")
    for area, price in result.items():
        f.write(f"- {area}: 單價 {price} 萬/坪\n")

print("更新完成！已寫入 data/taichung_daily.txt")


