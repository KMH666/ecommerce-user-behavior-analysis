# -*- coding: utf-8 -*-
"""零售电商数据可视化系统"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
from pathlib import Path
warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent
CLEAN_DIR = BASE_DIR / "clean"

st.set_page_config(page_title="零售电商数据可视化系统", layout="wide", page_icon="📊")

@st.cache_data
def load_data():
    df = pd.read_csv(CLEAN_DIR / "retail_orders_clean.csv", encoding="utf-8-sig")
    rfm = pd.read_csv(CLEAN_DIR / "user_rfm_labeled.csv", encoding="utf-8-sig")
    df["order_time"] = pd.to_datetime(df["order_time"])
    return df, rfm

df_raw, rfm_raw = load_data()

st.sidebar.title("📌 筛选面板")
st.sidebar.markdown("---")
min_m, max_m = int(df_raw["month"].min()), int(df_raw["month"].max())
month_range = st.sidebar.slider("月份区间", min_m, max_m, (min_m, max_m))
all_cats = df_raw["category"].unique().tolist()
selected_cats = st.sidebar.multiselect("商品品类", all_cats, default=all_cats)
all_segs = ["全部"] + rfm_raw["user_segment"].unique().tolist()
selected_segment = st.sidebar.radio("用户分层", all_segs, index=0)

df_f = df_raw[
    (df_raw["month"] >= month_range[0]) &
    (df_raw["month"] <= month_range[1]) &
    (df_raw["category"].isin(selected_cats))
].copy()
if selected_segment != "全部":
    users = rfm_raw[rfm_raw["user_segment"] == selected_segment]["user_id"].tolist()
    df_f = df_f[df_f["user_id"].isin(users)]

st.title("🛒 零售电商数据可视化分析系统")
st.markdown(f"筛选条件:{month_range[0]}月-{month_range[1]}月 | {len(selected_cats)}个品类 | {selected_segment}")

st.header("📊 数据总览")
c1,c2,c3,c4 = st.columns(4)
c1.metric("订单总数", f"{len(df_f):,}")
c2.metric("用户总数", f"{df_f["user_id"].nunique()}")
c3.metric("总销售额", f"¥{df_f["amount"].sum():,.0f}")
avg_p = df_f["amount"].mean() if len(df_f) > 0 else 0
c4.metric("平均客单价", f"¥{avg_p:.0f}")

st.header("📈 多维消费趋势")
tc1, tc2 = st.columns(2)
with tc1:
    st.subheader("月度消费总额趋势")
    monthly = df_f.groupby("month")["amount"].sum().reset_index()
    f1 = px.line(monthly, x="month", y="amount", markers=True, labels={"month": "月份", "amount": "消费总额(元)"}, color_discrete_sequence=["#ff7f0e"])
    f1.update_layout(height=350)
    st.plotly_chart(f1, use_container_width=True)
with tc2:
    st.subheader("星期消费数量分布")
    wd_map = {1:"周一",2:"周二",3:"周三",4:"周四",5:"周五",6:"周六",7:"周日"}
    df_f["wd_name"] = df_f["weekday"].map(wd_map)
    wk = df_f.groupby("wd_name")["quantity"].sum().reindex(["周一","周二","周三","周四","周五","周六","周日"]).reset_index()
    f2 = px.bar(wk, x="wd_name", y="quantity", labels={"wd_name": "星期", "quantity": "消费数量"}, color="wd_name", color_discrete_sequence=px.colors.qualitative.Pastel)
    f2.update_layout(showlegend=False, height=350)
    st.plotly_chart(f2, use_container_width=True)

st.header("📦 商品品类分析")
cc1, cc2 = st.columns(2)
with cc1:
    st.subheader("品类平均消费")
    cat_df = df_f.groupby("category")["amount"].mean().sort_values(ascending=False).reset_index()
    f3 = px.bar(cat_df, x="category", y="amount", labels={"category": "品类", "amount": "平均消费(元)"}, color="amount", color_continuous_scale="OrRd", text_auto=".0f")
    f3.update_layout(height=400)
    st.plotly_chart(f3, use_container_width=True)
with cc2:
    st.subheader("品类-月份热力图")
    pivot = df_f.pivot_table(values="amount", index="category", columns="month", aggfunc="mean", fill_value=0)
    f4 = px.imshow(pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(), text_auto=".0f", color_continuous_scale="YlOrRd", labels=dict(x="月份", y="品类", color="平均消费(元)"))
    f4.update_layout(height=400)
    st.plotly_chart(f4, use_container_width=True)

st.header("👥 用户聚类分层分析")
uc1, uc2 = st.columns(2)

uc1, uc2 = st.columns(2)
seg_f = rfm_raw if selected_segment == "全部" else rfm_raw[rfm_raw["user_segment"] == selected_segment]
with uc1:
    st.subheader("R-F聚类散点图")
    f5 = px.scatter(seg_f, x="Recency", y="Frequency", color="user_segment", size="Monetary", hover_data=["user_id", "Monetary"], color_discrete_sequence=px.colors.qualitative.Set2, labels={"Recency": "最近消费天数(R)", "Frequency": "消费频次(F)", "user_segment": "分层"}, size_max=15)
    f5.update_layout(height=450)
    st.plotly_chart(f5, use_container_width=True)
with uc2:
    st.subheader("用户分层占比")
    pie_df = seg_f["user_segment"].value_counts().reset_index()
    pie_df.columns = ["segment", "count"]
    f6 = px.pie(pie_df, values="count", names="segment", hole=0.3, color_discrete_sequence=px.colors.qualitative.Set2)
    f6.update_traces(textinfo="label+percent")
    f6.update_layout(height=450)
    st.plotly_chart(f6, use_container_width=True)

st.subheader("📋 分层用户明细数据")
cols = ["user_id", "Recency", "Frequency", "Monetary", "user_segment"]
st.dataframe(seg_f[cols].sort_values("Monetary", ascending=False).reset_index(drop=True), use_container_width=True, height=300)

st.markdown("---")
st.header("📥 数据导出")
d1, d2 = st.columns(2)
d1.download_button(label="📄 下载筛选后订单数据(CSV)", data=df_f.to_csv(index=False, encoding="utf-8-sig"), file_name="filtered_orders.csv", mime="text/csv")
d2.download_button(label="📄 下载用户分层数据(CSV)", data=seg_f[cols].to_csv(index=False, encoding="utf-8-sig"), file_name="user_segments.csv", mime="text/csv")
st.caption("零售电商数据可视化分析系统 | 数据可视化课程期末作业")
