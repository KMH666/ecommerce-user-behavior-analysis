# 电商用户消费行为分析系统

基于 **RFM 模型 + K-Means 聚类 + Streamlit** 的零售电商用户消费行为数据可视化分析系统。

本系统围绕「数据预处理 → 描述性统计可视化 → RFM 用户价值建模 → K-Means 用户分层 → 交互式 Web 应用」五个环节，构建了完整的电商用户消费行为分析流程，可为精细化运营与用户价值管理提供数据支持。

## 功能特性

- **数据预处理**：重复值删除、异常值剔除、缺失值处理、时间特征衍生、RFM 指标计算与 Min-Max 标准化
- **描述性统计可视化**：品类消费对比、金额分布直方图与箱线图、月度趋势、星期分布、品类-月份热力图
- **用户价值建模**：肘部法则确定最优聚类数，K-Means 将用户划分为高价值用户、中等价值用户、低流失风险用户
- **交互式系统**：基于 Streamlit 实现筛选联动（月份区间 / 商品品类 / 用户分层）、动态图表与 CSV 数据导出

## 项目结构

```
电商用户消费行为分析系统/
├── raw/                            # 原始数据
│   └── retail_orders_raw.csv
├── clean/                          # 清洗与分析结果数据
│   ├── retail_orders_clean.csv     # 清洗后的订单明细
│   ├── user_rfm.csv                # 用户 RFM 指标（含标准化）
│   └── user_rfm_labeled.csv        # 用户 RFM + 聚类分层结果
├── 图片结果/                        # 分析图表输出目录
│   ├── fig1_category_amount.png
│   ├── fig2_distribution_boxplot.png
│   ├── fig3_monthly_trend.png
│   ├── fig4_weekday_distribution.png
│   ├── fig5_heatmap.png
│   ├── fig_elbow.png
│   ├── fig_cluster_scatter.png
│   ├── fig_pie.png
│   └── fig_bar_rfm_comparison.png
├── data_preprocessing.py           # 代码1：数据清洗与 RFM 计算
├── visualization_plots.py          # 代码2：描述性统计与绘图
├── kmeans_clustering.py            # 代码3：K-Means 聚类建模
├── streamlit_app.py                # 代码4：Streamlit 交互式系统
├── requirements.txt
└── README.md
```

## 数据集说明

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | 字符串 | 用户唯一标识 |
| order_time | 日期时间 | 订单下单时间 |
| category | 字符串 | 商品品类（食品饮料/数码电子/服装鞋帽/家居日用/美妆个护/图书文具） |
| quantity | 整数 | 购买商品数量 |
| amount | 浮点数 | 订单消费金额（元） |

- 原始订单记录 2002 条，涉及 299 个用户，覆盖 2024 全年 12 个月
- 清洗后有效记录 1994 条，用户数 299 个

## 环境依赖

- Python 3.9+
- 依赖见 `requirements.txt`

```bash
pip install -r requirements.txt
```

> 绘图脚本使用中文字体 `SimHei` / `Microsoft YaHei`，在 Windows 环境下可正常显示中文。

## 使用方法

按以下顺序执行脚本（脚本内部已使用基于文件位置的相对路径，可在任意工作目录下运行）：

```bash
# 1. 数据清洗与 RFM 计算
python data_preprocessing.py

# 2. 描述性统计与可视化绘图（输出至 图片结果/）
python visualization_plots.py

# 3. K-Means 聚类建模（输出分层结果与新图表）
python kmeans_clustering.py

# 4. 启动 Streamlit 交互式系统
streamlit run streamlit_app.py
```

启动后浏览器会自动打开系统页面（默认 http://localhost:8501）。

## 技术栈

| 用途 | 工具 |
|------|------|
| 数据处理 | pandas、numpy |
| 机器学习 | scikit-learn（KMeans） |
| 静态可视化 | matplotlib、seaborn |
| 交互式可视化 | plotly、streamlit |

## 分析结论

- 消费金额呈显著右偏分布，少数高金额订单拉高整体均值；
- 用户被划分为三类：高价值用户、中等价值用户、低流失风险用户；
- 高价值用户消费频次与金额显著领先，是运营维护的重点人群；
- 交互式系统支持按月份、品类、用户分层多维度联动筛选，辅助差异化营销决策。

## 该项目仅供学习参考
