import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Olist BI Dashboard",
    page_icon="📊",
    layout="wide"
)

DB_PATH = "outputs/olist.db"

@st.cache_data
def load_data(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Sidebar
st.sidebar.title("📊 Olist BI Platform")
st.sidebar.markdown("**Swarnadeep Chatterjee**")
st.sidebar.markdown("MBA Candidate | Data Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "🏠 Overview",
    "💰 Revenue Analysis",
    "👥 Customer Segments",
    "🚚 Delivery Analysis",
    "📈 Forecasting"
])

st.sidebar.markdown("---")
st.sidebar.markdown("[GitHub](https://github.com/swarnadeepchatterjee02-glitch/olist-business-intelligence)")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/swarnadeepchatterjee02)")

# ─────────────────────────────
# PAGE 1 — OVERVIEW
# ─────────────────────────────
if page == "🏠 Overview":
    st.title("360° Business Intelligence & Strategy Platform")
    st.markdown("#### Olist Brazilian E-Commerce | 100,000+ Orders | 93,344 Customers")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", "99,441")
    col2.metric("Unique Customers", "93,344")
    col3.metric("Late Delivery Rate", "6.6%")
    col4.metric("Revenue Opportunity", "$510K")

    st.markdown("---")
    st.markdown("### Key Findings")

    col1, col2 = st.columns(2)
    with col1:
        st.error("**Customer Retention Crisis**\n\n1.03 average orders per customer. 56% of customers are Lost or At Risk.")
        st.error("**Logistics Breakdown**\n\nLate delivery rate hit 18% in March 2018 during peak volume months.")
    with col2:
        st.success("**Revenue Opportunity**\n\n$510,139 recoverable from converting 10% of At Risk customers to Loyal.")
        st.success("**Growth Trajectory**\n\nRevenue grew 4× in 2017. $3.2M forecast over next 90 days.")

    st.markdown("---")
    st.markdown("### A/B Test Result")
    col1, col2, col3 = st.columns(3)
    col1.metric("On-Time Review Score", "4.29")
    col2.metric("Late Delivery Score", "2.27", delta="-2.02", delta_color="inverse")
    col3.metric("Statistical Significance", "p < 0.0001")

# ─────────────────────────────
# PAGE 2 — REVENUE
# ─────────────────────────────
elif page == "💰 Revenue Analysis":
    st.title("💰 Revenue Analysis")
    st.markdown("---")

    df_rev = load_data("""
        SELECT c.product_category_name_english AS category,
               ROUND(SUM(i.price), 2) AS total_revenue,
               COUNT(DISTINCT i.order_id) AS total_orders
        FROM order_items i
        JOIN products p ON i.product_id = p.product_id
        JOIN categories c ON p.product_category_name = c.product_category_name
        GROUP BY category ORDER BY total_revenue DESC LIMIT 15
    """)

    fig1 = px.bar(df_rev, x="total_revenue", y="category",
                  orientation="h", title="Top 15 Categories by Revenue",
                  color="total_revenue", color_continuous_scale="Blues",
                  labels={"total_revenue": "Revenue ($)", "category": "Category"})
    fig1.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig1, use_container_width=True)

    df_monthly = load_data("""
        SELECT STRFTIME('%Y-%m', order_purchase_timestamp) AS month,
               ROUND(SUM(payment_value), 2) AS revenue,
               COUNT(DISTINCT o.order_id) AS total_orders
        FROM orders o JOIN payments p ON o.order_id = p.order_id
        WHERE STRFTIME('%Y', order_purchase_timestamp) IN ('2017','2018')
        GROUP BY month ORDER BY month
    """)

    fig2 = px.line(df_monthly, x="month", y="revenue",
                   title="Monthly Revenue Trend (2017-2018)",
                   labels={"revenue": "Revenue ($)", "month": "Month"})
    fig2.update_traces(line_color="#3266AD", line_width=2.5)
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────
# PAGE 3 — CUSTOMER SEGMENTS
# ─────────────────────────────
elif page == "👥 Customer Segments":
    st.title("👥 Customer Segmentation")
    st.markdown("---")

    df_seg = load_data("""
        SELECT segment,
               COUNT(*) AS customers,
               ROUND(AVG(monetary), 2) AS avg_spend,
               ROUND(AVG(frequency), 2) AS avg_orders,
               ROUND(AVG(recency_days), 0) AS avg_recency
        FROM customer_segments
        GROUP BY segment ORDER BY avg_spend DESC
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.pie(df_seg, values="customers", names="segment",
                      title="Customer Distribution by Segment",
                      color_discrete_map={
                          "Champions": "#27AE60",
                          "Loyal Customers": "#3266AD",
                          "Potential Loyalists": "#8E44AD",
                          "At Risk": "#E67E22",
                          "Lost": "#C0392B"
                      })
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(df_seg, x="segment", y="avg_spend",
                      title="Average Spend by Segment",
                      color="segment",
                      color_discrete_map={
                          "Champions": "#27AE60",
                          "Loyal Customers": "#3266AD",
                          "Potential Loyalists": "#8E44AD",
                          "At Risk": "#E67E22",
                          "Lost": "#C0392B"
                      })
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Segment Details")
    st.dataframe(df_seg, use_container_width=True)

    st.markdown("---")
    st.success("**Revenue Opportunity:** Converting 10% of At Risk customers (23,294) to Loyal → **$510,139 additional revenue**")

# ─────────────────────────────
# PAGE 4 — DELIVERY ANALYSIS
# ─────────────────────────────
elif page == "🚚 Delivery Analysis":
    st.title("🚚 Delivery & Operations Analysis")
    st.markdown("---")

    st.markdown("### A/B Test: On-Time vs Late Deliveries")
    col1, col2, col3 = st.columns(3)
    col1.metric("On-Time Score", "4.29", help="89,935 orders")
    col2.metric("Late Delivery Score", "2.27", delta="-2.02", delta_color="inverse", help="6,410 orders")
    col3.metric("T-Statistic", "132.04", help="p < 0.0001 - statistically significant")