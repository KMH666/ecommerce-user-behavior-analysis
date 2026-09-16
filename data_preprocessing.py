# -*- coding: utf-8 -*-
"""
代码1：数据清洗与RFM计算
功能：读取原始订单CSV → 清洗（去重/去异常/去缺失）→ 衍生时间字段 → 计算RFM指标 → Min-Max标准化 → 输出CSV
"""
from pathlib import Path

import pandas as pd
import numpy as np
from datetime import datetime

# 项目目录（保证脚本在任意工作目录下均可运行）
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
CLEAN_DIR = BASE_DIR / "clean"
CLEAN_DIR.mkdir(exist_ok=True)

# 读取原始数据
df = pd.read_csv(RAW_DIR / "retail_orders_raw.csv", encoding="utf-8-sig")
print(f"原始数据：{len(df)}条")

# ---- 数据清洗 ----
df = df.drop_duplicates()            # 删除完全重复的记录
df = df[df["amount"] >= 0]           # 剔除金额为负的异常值
df = df[df["quantity"] > 0]          # 剔除数量为零的无效记录
df = df.dropna()                     # 删除含缺失值的样本
print(f"清洗后：{len(df)}条，用户{df['user_id'].nunique()}个")

# ---- 时间特征衍生 ----
df["order_time"] = pd.to_datetime(df["order_time"])
df["year"] = df["order_time"].dt.year          # 年份
df["month"] = df["order_time"].dt.month        # 月份（1-12）
df["weekday"] = df["order_time"].dt.weekday + 1  # 星期（1=周一, 7=周日）
df["weekday_name"] = df["weekday"].map(
    {1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五", 6: "周六", 7: "周日"}
)  # 星期中文名

# ---- RFM指标计算 ----
max_date = df["order_time"].max()              # 以数据集最大日期为参考点
rfm = df.groupby("user_id").agg(
    Recency=("order_time", lambda x: (max_date - x.max()).days),   # 最近消费天数
    Frequency=("order_time", "count"),                              # 消费频次
    Monetary=("amount", "sum")                                      # 消费总金额
).reset_index()

# ---- Min-Max标准化 ----
for col in ["Recency", "Frequency", "Monetary"]:
    min_v, max_v = rfm[col].min(), rfm[col].max()
    rfm[f"{col}_scaled"] = (rfm[col] - min_v) / (max_v - min_v)

# 输出清洗后数据和RFM数据
df.to_csv(CLEAN_DIR / "retail_orders_clean.csv", index=False, encoding="utf-8-sig")
rfm.to_csv(CLEAN_DIR / "user_rfm.csv", index=False, encoding="utf-8-sig")
print("已输出：clean/retail_orders_clean.csv, clean/user_rfm.csv")
