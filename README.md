# 🧾 Vendor Performance Analysis | 🏬 Retail Inventory & Sales  

_Analyzing vendor efficiency and profitability to support strategic purchasing and inventory decisions using SQL, Python, and Power BI._

---

## 🗂️ Table of Contents
- <a href="#overview">Overview</a>
- <a href="#business-problem">Business Problem</a>
- <a href="#dataset">Dataset</a>
- <a href="#tools--technologies">Tools & Technologies</a>
- <a href="#project-structure">Project Structure</a>
- <a href="#data-cleaning--preparation">Data Cleaning & Preparation</a>
- <a href="#exploratory-data-analysis-eda">Exploratory Data Analysis (EDA)</a>
- <a href="#research-questions--key-findings">Research Questions & Key Findings</a>
- <a href="#dashboard">Dashboard</a>
- <a href="#how-to-run-this-project">How to Run This Project</a>
- <a href="#final-recommendations">Final Recommendations</a>
- <a href="#author--contact">Author & Contact</a>

---

<h2><a class="anchor" id="overview"></a>Overview</h2>

This project evaluates vendor performance and retail inventory dynamics to drive strategic insights for purchasing, pricing, and inventory optimization. A complete data pipeline was built using SQL for ETL, Python for analysis and hypothesis testing, and Power BI for visualization.

---

<h2><a class="anchor" id="business-problem"></a>Business Problem</h2>

Effective inventory and sales management are critical in the retail sector. This project aims to:
1. Identify underperforming brands needing pricing or promotional adjustments
2. Determine vendor contributions to sales and profits
3. Analyze the cost-benefit of bulk purchasing
4. Investigate inventory turnover inefficiencies
5. Statistically validate differences in vendor profitability

---
<h2 class="anchor" id="dataset">Dataset</h2>

* Multiple CSV files located in `/data` folder (sales, vendors, inventory)
* Summary table created from ingested data and used for analysis
---

<h2 class="anchor" id="tools-technologies">Tools & Technologies</h2>

* **SQL** (Common Table Expressions, Joins, Filtering)
* **Python** (Pandas, Matplotlib, Seaborn, SciPy)
* **Power BI** (Interactive Visualizations)
* **GitHub**
---
<h2 class="anchor" id="project-structure">Project Structure</h2>

```
vendor-performance-analysis/
├── .gitignore
├── README.md
├── requirements.txt
├── Vendor Performance Report.pdf
├── notebooks/
│   ├── exploratory_data_analysis.ipynb  # Jupyter notebooks
│   └── vendor_performance_analysis.ipynb
├── scripts/
│   ├── ingestion_db.py                  # Python scripts for ingestion and processing
│   └── get_vendor_summary.py
└── dashboard/
└── vendor_performance_dashboard.pbix  # Power BI dashboard file
```
---

<h2 class="anchor" id="data-cleaning-preparation">Data Cleaning & Preparation</h2>

**Removed transactions with:**
* Gross Profit $\le 0$
* Profit Margin $\le 0$
* Sales Quantity $= 0$

Created summary tables with vendor-level metrics
Converted data types, handled outliers, merged lookup tables

---

<h2 class="anchor" id="exploratory-data-analysis-eda">Exploratory Data Analysis (EDA)</h2>

**Negative or Zero Values Detected:**
* Gross Profit: Min $\$-52,002.78$ (loss-making sales)
* Profit Margin: Min $\le 0$ (sales at zero or below cost)
* Unsold Inventory: Indicating slow-moving stock

**Outliers Identified:**
* High Freight Costs (up to $\text{\$257k}$)
* Large Purchase/Actual Prices

**Correlation Analysis:**
* Strong between Purchase Qty & Sales Qty (0.899)
* Negative between Profit Margin & Sales Price (-0.079)

---
<h2 class="anchor" id="research-questions-key-findings">Research Questions & Key Findings</h2>

1.  **Brands for Promotions:** $\mathbf{158}$ brands with low sales but high profit margins
2.  **Top Vendors:** Top 10 vendors = $\mathbf{65.69\%}$ of purchases ($\mathbf{risk}$ of over-reliance)
3.  **Bulk Purchasing Impact:** $\mathbf{72\%}$ cost savings per unit in large orders
4.  **Inventory Turnover:** $\mathbf{\$2.7M}$ worth of unsold inventory
5.  **Vendor Profitability:**
    * High Vendors: Mean Margin $\mathbf{31.17\%}$
    * Low Vendors: Mean Margin $\mathbf{41.15\%}$
6.  **Hypothesis Testing:** Statistically significant difference in profit margins distinct vendor strategies
---
<h2 class="anchor" id="dashboard">Dashboard</h2>

Power BI dashboard shows:
* Sales and Margins
* Vendor-wise Sales and Margins
* Inventory Turnover
* Bulk Purchase Savings
* Performance Heatmaps

![Vendor Performance Dashboard](images/dashboard.png)

---
<h2 class="anchor" id="how-to-run-this-project">How to Run This Project</h2>

1.  **Clone the repository:**
```bash
    git clone [https://github.com/SHANMUKHA-SANAPATHI/vendor-performance-analysis-sql--python-power-bi.git](https://github.com/SHANMUKHA-SANAPATHI/vendor-performance-analysis-sql--python-power-bi.git)
```

2.  **Load the CSVs and Ingest into database:**
```bash
    python scripts/ingestion_db.py
```
3.  **Create vendor summary table:**
```bash
    python scripts/get_vendor_summary.py
```
4.  **Open and run notebooks:**
    * `notebooks/exploratory_data_analysis.ipynb`
    * `notebooks/vendor_performance_analysis.ipynb`
5.  **Open Power BI Dashboard:**
    * `dashboard/vendor_performance_dashboard.pbix`
---
<h2 class="anchor" id="final-recommendations">Final Recommendations</h2>

1.  Diversify vendor base to reduce risk
2.  Optimize bulk order strategies
3.  Reprice slow-moving, high-margin brands
4.  Clear unsold inventory strategically
5.  Improve marketing for underperforming vendors

---
<h2 class="anchor" id="author-contact">Author & Contact</h2>

**shanmukha rao**
Data Analyst
* Email: shanmukhsanpathi@gmail.com

