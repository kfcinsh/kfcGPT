import pandas as pd
import requests
import zipfile
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta, timezone

# 取得今天日期（台灣時間）
tz = timezone(timedelta(hours=8))
today = datetime.now(tz)
date_str = today.strftime("%Y/%m/%d")

# 內政部實價登錄不動產成交資料（全台）
# 官方下載入口（A 案：不動產買賣）
url = "https://plvr.land.moi.gov.tw//Download?fileName=lvr_landcsv.zip"

print("下載實價登錄 ZIP 檔中…")
response = requests.get(url)
response.raise_for_status()

zip_file = zipfile.ZipFile(BytesIO(response.content))

# 台灣全國「建物買賣」資料檔名（A_lvr_land_A.csv）
csv_name = "A_lvr_land_A.csv"

print("讀取 CSV 檔中…")
# 官方檔案編碼是 cp950（Big5），要特別設定
df = pd.read_csv(zip_file.open(csv_name), encoding="cp950")

# 只取「台中市」＋「住家用」的資料
df = df[df["縣市"] == "臺中市"]
df = df[df["主要用途"] == "住家用"]

# 只算「建物型態」看起來是一般住宅的案件（可依喜好調整）
residential_keywords = ["住宅大樓", "華廈", "透天厝", "透天住宅"]
df = df[df["建物型態"].astype(str).str.contains("|".join(residential_keywords))]

# 單價元/平方公尺 → 萬/坪
# 1 坪 = 3.305785 平方公尺
PING_PER_M2 = 1 / 3.305785
df["單價_萬每坪"] = df["單價元平方公尺"] * PING_PER_M2 / 10000

# 要統計的行政區
target_areas = ["北屯區", "西屯區", "南屯區", "烏日區"]

avg_price = {}

for area in target_areas:
    sub = df[df["鄉鎮市區"] == area]
    # 避免有 0 或缺值干擾平均
    clean = sub["單價_萬每坪"].replace(0, pd.NA).dropna()
    if len(clean) == 0:
        avg = None
    else:
        avg = round(clean.mean(), 1)
    avg_price[area] = avg

# 準備輸出文字
lines = []
lines.append(f"{date_str} 台中房價每日更新：")
lines.append("")

def fmt(area_name):
    value = avg_price[area_name]
    if value is None:
        return f"- {area_name}：今日無足夠成交資料"
    else:
        return f"- {area_name}：單價 {value} 萬／坪"

lines.append(fmt("北屯區"))
lines.append(fmt("西屯區"))
lines.append(fmt("南屯區"))
lines.append(fmt("烏日區"))
lines.append("")
lines.append("（以上資料來自內政部實價登錄，由 kfcGPT 自動計算產生）")

# 確保 data 資料夾存在
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

out_path = data_dir / "taichung_daily.txt"

print(f"寫入 {out_path} …")
with out_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("完成：台中房價每日更新已產生。")

