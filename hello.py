from preswald import connect, get_df, query, text, table, plotly, sidebar

import pandas as pd
import plotly.express as px

# Load and clean data
connect()

# Sidebar setup
sidebar("## 📊 Superstore Dashboard")
sidebar("Built with Preswald · v1.0")
sidebar("Made by Shreejith")
sidebar("💼 Data: Sample Superstore")

df = get_df("superstore")
df.columns = df.columns.str.strip()

df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df = df.dropna(subset=['Order Date'])

df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
df['Profit Margin (%)'] = (df['Profit'] / df['Sales'] * 100).round(1)

# Title & KPIs
text("# Superstore Sales Dashboard")
text("### A self-service retail analytics app for exploring product performance, sales trends, and discount risks.")

text(f"📦 Total Orders: {len(df)} 💰 Total Sales: ${df['Sales'].sum():,.0f} 📈 Total Profit: ${df['Profit'].sum():,.0f} 🧾 Avg Margin: {df['Profit Margin (%)'].mean():.1f}%")

# Sample Records (via SQL)
text("## 🔍 Sample Records")
text("Here’s a quick snapshot of 10 rows queried directly using SQL.")
sql_sample = """
SELECT "Product Name", "Category", "Sales", "Profit"
FROM superstore
LIMIT 10
"""
sample_df = query(sql_sample, "superstore")
table(sample_df, title="Sample Orders (via SQL)")

# Time Series Trends
text("## 📈 Monthly Sales & Profit Over Time")
text("This chart shows how sales and profit have evolved across months. Notice seasonal spikes and profit dips.")
monthly = df.groupby('Year-Month')[['Sales', 'Profit']].sum().reset_index()
fig_line = px.line(monthly, x='Year-Month', y=['Sales', 'Profit'], markers=True, title="Monthly Sales and Profit")
plotly(fig_line)
text("👉 Sales show a consistent upward trend, especially post-2016. However, profit remains relatively flat, suggesting increasing costs or discounting issues.")

# Regional Breakdown
text("## 🗺️ Regional Sales by Sub-Category")
text("Sales performance varies widely by region and product type. Phones, Chairs, and Binders dominate across all.")
subcat = df.groupby(['Region', 'Sub-Category'])[['Sales']].sum().reset_index()
fig_bar = px.bar(subcat, x='Sub-Category', y='Sales', color='Region', barmode='group', title="Sales by Sub-Category and Region")
plotly(fig_bar)
text("👉 The West region dominates in almost every sub-category. Binders, Phones, and Chairs are top sellers across all regions.")

# Product Performance
product_summary = df.groupby('Product Name')[['Sales', 'Profit', 'Discount']].sum().reset_index()
product_summary['Profit Margin (%)'] = (product_summary['Profit'] / product_summary['Sales'] * 100).round(1)

text("## 🏆 Most Profitable Products")
text("These are the top-performing products in terms of raw profit.")
top10 = product_summary.sort_values('Profit', ascending=False).head(10)
table(top10, title="Top 10 Products by Profit")
text("👉 The top 10 products account for a significant share of total profit, and most come from Technology. These are likely 'cash cow' SKUs worth reinforcing.")

text("## 🔻 Worst Performing Products")
text("These products are losing money despite sales. Many are high-discount or oversupplied items.")
bottom10 = product_summary.sort_values('Profit').head(10)
table(bottom10, title="Bottom 10 Products by Profit")
text("👉 High-volume losses on items like printers and binding machines suggest pricing mismatches or poor product-market fit.")

# Scatterplot
text("## 🎯 Product Performance by Category")
text("Each dot represents a sold item. Sales vs Profit across categories helps identify pricing/value gaps.")
scatter_df = df[['Sales', 'Profit', 'Category']].dropna()
fig_scatter = px.scatter(scatter_df, x='Sales', y='Profit', color='Category', title="Sales vs Profit by Category")
plotly(fig_scatter)

# Discount Risks
text("## ⚠️ Discount Outliers")
text("These high-discount items are at risk of margin erosion. Consider reviewing pricing or bundling strategies.")
discounted = product_summary.sort_values('Discount', ascending=False).head(10)
table(discounted, title="Top 10 Products by Total Discount Given")
text("👉 Items with large discounts and negative margins (e.g., Premier Elliptical and Avery Self-Adhesive) need pricing review or bundling strategies.")

# Final takeaway
text("## 📌 Summary")
text("In summary, strong sales growth is offset by decreasing profit. Category-level winners are clear, but discounts may be eroding long-term margin health. This dashboard surfaces your top-selling items, high-risk losses, and where sales concentrate across time and region. Consider doubling down on high-profit categories and auditing discount-heavy SKUs.")
