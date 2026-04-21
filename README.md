360° Business Intelligence & Strategy Platform
Olist Brazilian E-Commerce | End-to-End Analytics & Consulting Project
Show Image
Show Image
Show Image
Show Image

Project Summary
A full end-to-end business intelligence and strategy engagement on Olist's Brazilian e-commerce dataset — covering 100,000+ orders, 93,344 customers, and 9 relational SQL tables across 7 analytical phases.
Built to mirror a real consulting engagement: raw data → ETL pipeline → business diagnostics → customer intelligence → operational analysis → demand forecasting → executive strategy deck.
Live consulting deck: Olist_Strategy_Report.pptx

Key Findings
FindingResultTop revenue categoryHealth & Beauty — $1.25MCustomer retention rate1.03 avg orders per customerLost or At Risk customers56% of 93,344 customersRevenue recovery opportunity$510,139 (10% At Risk conversion)Late delivery impactReview score drops 4.29 → 2.27 (p<0.0001)Late delivery peak18% in March 201890-day revenue forecast$3.2M projectedBlack Friday spike7× average daily revenue

Analytical Phases
Phase 1 — Data Engineering & SQL
ETL pipeline ingesting 9 CSV files into SQLite. Multi-table SQL queries covering revenue, delivery performance, seller rankings, and review scores.
Phase 2 — EDA & Business Diagnostics
Exploratory analysis revealing 4× revenue growth, Black Friday spike to $175K/day, and late delivery rate correlation with satisfaction collapse.
Phase 3 — Customer Segmentation
RFM scoring of 93,344 customers into 5 cohorts using SQL and K-Means clustering. Identified $510K recovery opportunity in At Risk segment.
Phase 4 — Operational Analysis & A/B Testing
Statistical proof that late deliveries reduce review scores by 2.02 points (t=132.04, p<0.0001). Identified 66% delivery padding problem.
Phase 5 — Time-Series Forecasting
Prophet model forecasting $3.2M over 90 days. Identified Monday peak demand and Black Friday 7× spike requiring pre-built logistics capacity.
Phase 6 — Power BI Dashboard
Dual operational and customer intelligence dashboards tracking revenue, late delivery rate, customer segments, and KPIs.
Phase 7 — Executive Consulting Deck
10-slide strategy presentation structured as Situation → Complication → Findings → Recommendations → Financial Impact.

Tech Stack

Python — pandas, matplotlib, seaborn, scikit-learn, prophet, scipy
SQL — SQLite, multi-table joins, window functions, CTEs
Power BI — DAX, data modelling, KPI dashboards
Statistical Testing — t-test, A/B testing, p-value analysis
Forecasting — Facebook Prophet, seasonality decomposition


How to Run

Clone this repo
Download the dataset from https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
Place all 9 CSV files in the data/ folder
Run: pip install pandas matplotlib seaborn scikit-learn prophet scipy sqlalchemy jupyter
Run notebooks in order: 01 → 02 → 03 → 04


Author
Swarnadeep Chatterjee
Data Analytics Professional | MBA Candidate, University of Louisville
LinkedIn | GitHub