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

if page == "🏠 Overview":
    st.title("360 Degree Business Intelligence and Strategy Platform")
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
        st.error("**Customer Retention Crisis** — 1.03 average orders per customer. 56% of customers are Lost or At Risk.")
        st.error("**Logistics Breakdown** — Late delivery rate hit 18% in March 2018 during peak volume months.")
    with col2:
        st.success("**Revenue Opportunity** — $510,139 recoverable from converting 10% of At Risk customers to Loyal.")
        st.success("**Growth Trajectory** — Revenue grew 4x in 2017. $3.2M forecast over next 90 days.")
    st.markdown("---")
    st.markdown("### A/B Test Result")
    col1, col2, col3 = st.columns(3)
    col1.metric("On-Time Review Score", "4.29")
    col2.metric("Late Delivery Score", "2.27", delta="-2.02", delta_color="inverse")
    col3.metric("Statistical Significance", "p < 0.0001")

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
    st.success("**Revenue Opportunity:** Converting 10% of At Risk customers (23,294) to Loyal — $510,139 additional revenue")

elif page == "🚚 Delivery Analysis":
    st.title("🚚 Delivery and Operations Analysis")
    st.markdown("---")
    st.markdown("### A/B Test: On-Time vs Late Deliveries")
    col1, col2, col3 = st.columns(3)
    col1.metric("On-Time Score", "4.29")
    col2.metric("Late Delivery Score", "2.27", delta="-2.02", delta_color="inverse")
    col3.metric("T-Statistic", "132.04")
    st.markdown("---")
    df_delay = load_data("""
        SELECT STRFTIME('%Y-%m', order_purchase_timestamp) AS month,
               COUNT(order_id) AS total_orders,
               SUM(is_late) AS late_orders,
               ROUND(AVG(is_late)*100, 1) AS late_rate_pct
        FROM orders
        WHERE order_purchase_timestamp IS NOT NULL
        AND STRFTIME('%Y', order_purchase_timestamp) IN ('2017','2018')
        GROUP BY month ORDER BY month
    """)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_delay["month"], y=df_delay["total_orders"],
                         name="Total Orders", marker_color="#B5D4F4"))
    fig.add_trace(go.Scatter(x=df_delay["month"], y=df_delay["late_rate_pct"],
                             name="Late Rate %", yaxis="y2",
                             line=dict(color="#C0392B", width=2.5)))
    fig.update_layout(
        title="Order Volume vs Late Delivery Rate",
        yaxis=dict(title="Total Orders"),
        yaxis2=dict(title="Late Rate %", overlaying="y", side="right"),
        legend=dict(x=0, y=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.markdown("### Key Operational Findings")
    col1, col2, col3 = st.columns(3)
    col1.error("**18%** late delivery rate in March 2018")
    col2.warning("**66%** of orders arrive 10+ days early")
    col3.error("**2.02 point** review score drop from late delivery")

elif page == "📈 Forecasting":
    st.title("📈 Revenue Forecasting")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("90-Day Forecast", "$3.2M")
    col2.metric("Daily Avg Forecast", "$35,583", delta="+41% vs historical")
    col3.metric("Black Friday Spike", "7x")
    st.markdown("---")
    df_monthly = load_data("""
        SELECT STRFTIME('%Y-%m', order_purchase_timestamp) AS month,
               ROUND(SUM(payment_value), 2) AS revenue
        FROM orders o JOIN payments p ON o.order_id = p.order_id
        WHERE order_purchase_timestamp IS NOT NULL
        AND STRFTIME('%Y', order_purchase_timestamp) IN ('2017','2018')
        GROUP BY month ORDER BY month
    """)
    fig = px.line(df_monthly, x="month", y="revenue",
                  title="Monthly Revenue Trend with Black Friday Spike",
                  labels={"revenue": "Revenue ($)", "month": "Month"})
    fig.update_traces(line_color="#E67E22", line_width=2.5)
    fig.add_annotation(x="2017-11", y=1271039,
                       text="Black Friday: $175K/day",
                       showarrow=True, arrowhead=2,
                       bgcolor="#E67E22", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.markdown("### Seasonality Insights")
    col1, col2, col3 = st.columns(3)
    col1.info("**Monday** is peak shopping day")
    col2.warning("**Saturday and Sunday** are weakest days")
    col3.error("**November** Black Friday is the biggest revenue event")