import pandas as pd
import requests
import datetime
from pathlib import Path
from io import BytesIO
import zipfile

# 取得今天日期（台灣時間）
now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
today = now.strftime("%Y-%m-%d %H:%M:%S")

# 實價登錄每日更新檔案（A 表：不動產買賣）
url = "https://plvr.land.moi.gov.tw//Download?fileName=lvr_landcsv.zip"

# 下載 ZIP
response = requests.get(url)
zip_file = zipfile.ZipFile(BytesIO(response.content))

# A 表（不動產買賣資料）
csv_name = "A_lvr_land_A.csv"
df = pd.read_csv(zip_file.open(csv_name), encoding="utf-8")

# 篩選台中市 + 住家用
df = df[df["鄉鎮市區"].str.contains("台中", na=False)]
residential_keywords = ["住宅", "住家", "透天", "公寓", "華廈", "大樓"]
df = df[df["主要用途"].isin(residential_keywords)]

# 計算每坪單價
df["每坪單價"] = df["單價每平方公尺"].astype(float) / 3.3058

# 全市狀況
total_count = len(df)
avg_price_city = df["每坪單價"].mean()

# 各區
district_stats = df.groupby("鄉鎮市區")["每坪單價"].mean().sort_values()

# 建立 data 資料夾
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# 儲存結果
output = f"台中市不動產每日更新（{today}）\n"
output += f"【全市成交量】：{total_count} 件\n"
output += f"【全市平均每坪】：{avg_price_city:.2f} 萬元/坪\n\n"
output += "【各行政區平均每坪】\n"

for district, price in district_stats.items():
    output += f"- {district}：{price:.2f} 萬/坪\n"

file_path = data_dir / "taichung_daily.txt"
file_path.write_text(output, encoding="utf-8")

print("已產生台中每日房價資料：")
print(output)
