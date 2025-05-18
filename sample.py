import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

# PostgreSQL connection setup
DB_URL = "postgresql://exam_streamlit_user:6beiuI3metBtg239sErSxtwEpLiBZ8xx@dpg-d0jugqre5dus73ba6b3g-a.singapore-postgres.render.com/exam_streamlit"
engine = create_engine(DB_URL, client_encoding='utf8')

# Load data from PostgreSQL
@st.cache_data
def fetch_sales_summary():
    query = """
        SELECT "Product", COUNT(*) AS sales_count
        FROM final
        GROUP BY "Product"
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return pd.DataFrame(result.mappings().all())

# Load and process data
data = fetch_sales_summary()
data = data.sort_values(by="sales_count", ascending=False)
total = data["sales_count"].sum()
data["sales_share"] = (data["sales_count"] / total * 100).round(2)

# Dashboard title
st.title("🛍️ Product Sales Analysis")

# Overview section
st.markdown("## 📦 Product Overview")
col1, col2 = st.columns(2)
col1.metric("Total Products", len(data))
col2.metric("Total Orders", total)

# Bar Chart - Top Products
st.markdown("### 🔝 Most Sold Products")
fig_bar = px.bar(data, x="Product", y="sales_count", color="Product",
                 labels={"sales_count": "Units Sold"}, title="Top Selling Products")
st.plotly_chart(fig_bar, use_container_width=True)

# Donut Chart - Sales Distribution
st.markdown("### 🥧 Product Sales Distribution")
fig_donut = px.pie(data, names="Product", values="sales_share", hole=0.5,
                   title="Sales Share per Product")
st.plotly_chart(fig_donut, use_container_width=True)

# Highlight Least Sold
st.markdown("### 🚨 Lowest Selling Product")
least = data.iloc[-1]
st.warning(f"\n**{least['Product']}** had the least sales with only **{least['sales_count']}** orders ({least['sales_share']}% of total).\n")
