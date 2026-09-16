# -*- coding: utf-8 -*-
"""
代码2：描述性统计与可视化绘图
功能：读取清洗数据 → 绘制5张分析图表 → 保存为PNG
生成：fig1~fig5 共5张图片
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 项目目录（保证脚本在任意工作目录下均可运行）
BASE_DIR = Path(__file__).resolve().parent
CLEAN_DIR = BASE_DIR / "clean"
FIG_DIR = BASE_DIR / "图片结果"
FIG_DIR.mkdir(exist_ok=True)

# 中文字体配置
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# 读取数据
df = pd.read_csv(CLEAN_DIR / "retail_orders_clean.csv", encoding="utf-8-sig")
rfm = pd.read_csv(CLEAN_DIR / "user_rfm.csv", encoding="utf-8-sig")

# ---- 图1：各商品品类平均消费金额柱状图 ----
cat_mean = df.groupby("category")["amount"].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
bars = plt.bar(cat_mean.index, cat_mean.values, color=sns.color_palette("Set3", 6))
plt.title("各商品品类平均消费金额")
plt.xticks(rotation=15)
plt.ylabel("平均消费金额（元）")
plt.savefig(FIG_DIR / "fig1_category_amount.png", dpi=200, bbox_inches="tight")
plt.close()
print("已生成：fig1_category_amount.png")

# ---- 图2：消费金额分布直方图与箱线图 ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
# 左图：直方图
axes[0].hist(df["amount"], bins=50, color="steelblue", edgecolor="white")
axes[0].axvline(df["amount"].mean(), color="red", linestyle="--",
                label=f"均值={df['amount'].mean():.0f}")
axes[0].axvline(df["amount"].median(), color="green", linestyle="--",
                label=f"中位数={df['amount'].median():.0f}")
axes[0].set_title("消费金额分布直方图")
axes[0].set_xlabel("金额（元）")
axes[0].set_ylabel("频数")
axes[0].legend()
# 右图：箱线图
axes[1].boxplot(df["amount"], vert=True, patch_artist=True,
                boxprops=dict(facecolor="lightcoral"))
axes[1].set_title("消费金额箱线图")
axes[1].set_ylabel("金额（元）")
plt.tight_layout()
plt.savefig(FIG_DIR / "fig2_distribution_boxplot.png", dpi=200)
plt.close()
print("已生成：fig2_distribution_boxplot.png")

# ---- 图3：月度消费总额折线图 ----
monthly = df.groupby("month")["amount"].sum()
plt.figure(figsize=(10, 6))
plt.plot(monthly.index, monthly.values, marker="o", linewidth=2.5, color="darkorange")
plt.title("月度消费总额趋势")
plt.xlabel("月份")
plt.ylabel("消费总额（元）")
plt.xticks(range(1, 13))
plt.grid(axis="y", alpha=0.3)
plt.savefig(FIG_DIR / "fig3_monthly_trend.png", dpi=200, bbox_inches="tight")
plt.close()
print("已生成：fig3_monthly_trend.png")

# ---- 图4：星期消费数量分布柱状图 ----
wd = df.groupby("weekday_name")["quantity"].sum()
colors = ["#66b3ff" if d in ["周六", "周日"] else "#99d8ff" for d in wd.index]
plt.figure(figsize=(10, 6))
plt.bar(wd.index, wd.values, color=colors)
plt.title("星期消费数量分布")
plt.xlabel("星期")
plt.ylabel("消费数量")
plt.savefig(FIG_DIR / "fig4_weekday_distribution.png", dpi=200, bbox_inches="tight")
plt.close()
print("已生成：fig4_weekday_distribution.png")

# ---- 图5：品类-月份平均消费热力图 ----
pivot = df.pivot_table(values="amount", index="category", columns="month", aggfunc="mean")
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd")
plt.title("品类-月份平均消费热力图")
plt.xlabel("月份")
plt.ylabel("品类")
plt.savefig(FIG_DIR / "fig5_heatmap.png", dpi=200, bbox_inches="tight")
plt.close()
print("已生成：fig5_heatmap.png")
print("所有图片生成完毕！")
