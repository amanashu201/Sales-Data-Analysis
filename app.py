import pandas as pd
import streamlit as st
import plotly.express as px

# Load CSV
df = pd.read_csv("data/sales.csv")
df['SalesAmount'] = df['Quantity'] * df['Price']
df['Date'] = pd.to_datetime(df['Date'])

# Title
st.title("📊 Sales Dashboard")

# Sidebar filters
st.sidebar.header("Filter")
product_filter = st.sidebar.multiselect("Select Product:", df['Product'].unique(), default=df['Product'].unique())
date_filter = st.sidebar.date_input("Select Date Range:", [df['Date'].min(), df['Date'].max()])

# Filtered Data
filtered_df = df[
    (df['Product'].isin(product_filter)) &
    (df['Date'] >= pd.to_datetime(date_filter[0])) &
    (df['Date'] <= pd.to_datetime(date_filter[1]))
]

# KPIs
st.subheader("📌 Summary")
st.metric("Total Revenue", f"${filtered_df['SalesAmount'].sum():,.2f}")
st.metric("Total Units Sold", int(filtered_df['Quantity'].sum()))

# 📈 Plotly Line Chart: Revenue Over Time
st.subheader("📈 Revenue Over Time")
revenue_trend = filtered_df.groupby('Date')['SalesAmount'].sum().reset_index()
fig_line = px.line(revenue_trend, x='Date', y='SalesAmount', markers=True, title="Revenue Trend")
st.plotly_chart(fig_line, use_container_width=True)

# 📊 Plotly Bar Chart: Product-wise Sales
st.subheader("📊 Product-wise Revenue")
product_sales = filtered_df.groupby('Product')['SalesAmount'].sum().reset_index()
fig_bar = px.bar(product_sales, x='Product', y='SalesAmount', title="Product Revenue", color='Product')
st.plotly_chart(fig_bar, use_container_width=True)

# 📎 Button to Show Raw Data
if st.checkbox("📂 Show Raw Data"):
    st.dataframe(filtered_df)

# 💾 Button to Download Filtered Data as CSV
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv'
)

# 🔝 Peak Revenue Day Info
peak_day = revenue_trend.loc[revenue_trend['SalesAmount'].idxmax()]
st.info(f"🔝 Peak Revenue Day: {peak_day['Date'].date()} (${peak_day['SalesAmount']:,.2f})")



# 🥧 Pie Chart: Revenue Share by Product
st.subheader("🥧 Revenue Share by Product")
fig_pie = px.pie(
    product_sales,
    names='Product',
    values='SalesAmount',
    title="Product Revenue Share",
    hole=0.4  # donut style
)
st.plotly_chart(fig_pie, use_container_width=True)
