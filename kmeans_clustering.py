# -*- coding: utf-8 -*-
"""
代码3：K-Means聚类建模
功能：读取RFM数据 → 肘部法则确定K值 → K-Means聚类 → 标签映射 → 输出分层结果及图表
生成：fig_elbow.png, fig_cluster_scatter.html, fig_pie.html, fig_pie.png, fig_bar_rfm_comparison.png
      并输出 user_rfm_labeled.csv
"""
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import plotly.express as px

# 项目目录（保证脚本在任意工作目录下均可运行）
BASE_DIR = Path(__file__).resolve().parent
CLEAN_DIR = BASE_DIR / "clean"
FIG_DIR = BASE_DIR / "图片结果"
FIG_DIR.mkdir(exist_ok=True)

# 中文字体配置
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# 读取RFM数据
rfm = pd.read_csv(CLEAN_DIR / "user_rfm.csv", encoding="utf-8-sig")
X = rfm[["Recency_scaled", "Frequency_scaled", "Monetary_scaled"]].values

# ---- 肘部法则：确定最优聚类数 ----
sse = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init="auto")
    km.fit(X)
    sse.append(km.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), sse, marker="o", linewidth=2.5, color="royalblue")
plt.axvline(x=3, color="red", linestyle="--", label="k=3")
plt.title("肘部法则曲线")
plt.xlabel("聚类数 K")
plt.ylabel("SSE（误差平方和）")
plt.legend()
plt.savefig(FIG_DIR / "fig_elbow.png", dpi=200, bbox_inches="tight")
plt.close()
print("已生成：fig_elbow.png")

# ---- K-Means聚类（K=3）----
model = KMeans(n_clusters=3, random_state=42, n_init="auto")
rfm["cluster"] = model.fit_predict(X)

# ---- 标签映射：根据RFM均值特征为各簇命名 ----
cm = rfm.groupby("cluster")[["Recency", "Frequency", "Monetary"]].mean()
high_val = cm["Frequency"].sort_values(ascending=False).index[0]    # F最高 → 高价值
low_risk = cm["Recency"].sort_values(ascending=False).index[0]      # R最高 → 低流失风险
mid = [c for c in range(3) if c not in [high_val, low_risk]][0]     # 剩余 → 中等价值

label_map = {high_val: "高价值用户", mid: "中等价值用户", low_risk: "低流失风险用户"}
rfm["user_segment"] = rfm["cluster"].map(label_map)
rfm.to_csv(CLEAN_DIR / "user_rfm_labeled.csv", index=False, encoding="utf-8-sig")
print("已输出：clean/user_rfm_labeled.csv")

# ---- 聚类散点图（交互式HTML）----
fig = px.scatter(rfm, x="Recency", y="Frequency", color="user_segment",
                 size="Monetary", hover_data=["user_id", "Monetary"],
                 title="R-F用户聚类散点图")
fig.write_html(FIG_DIR / "fig_cluster_scatter.html")
print("已生成：图片结果/fig_cluster_scatter.html")

# ---- 分层占比饼图 ----
pie_data = rfm["user_segment"].value_counts()
fig = px.pie(values=pie_data.values, names=pie_data.index, hole=0.3,
             title="用户分层占比")
fig.write_html(FIG_DIR / "fig_pie.html")
fig.write_image(FIG_DIR / "fig_pie.png", scale=2)
print("已生成：图片结果/fig_pie.html, 图片结果/fig_pie.png")

# ---- RFM均值对比柱状图 ----
ms = rfm.groupby("user_segment")[["Recency", "Frequency", "Monetary"]].mean()
ms.plot.bar(figsize=(10, 6), title="各分层用户RFM均值对比")
plt.ylabel("均值")
plt.xticks(rotation=0)
plt.savefig(FIG_DIR / "fig_bar_rfm_comparison.png", dpi=200, bbox_inches="tight")
plt.close()
print("已生成：fig_bar_rfm_comparison.png")
print("聚类分析全部完成！")
