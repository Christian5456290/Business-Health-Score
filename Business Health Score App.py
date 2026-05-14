import streamlit as st

st.set_page_config(page_title="Business Health Scorecard", layout="centered")

st.title("Business Health Scorecard")
st.markdown("Enter your business metrics below to generate a health score.")

st.divider()

st.subheader("Input Your Metrics")

revenue_growth = st.slider("Revenue Growth (%)", min_value=-50, max_value=100, value=10)
churn_rate = st.slider("Customer Churn Rate (%)", min_value=0, max_value=100, value=20)
profit_margin = st.slider("Profit Margin (%)", min_value=-50, max_value=100, value=15)
nps_input = st.slider("Net Promoter Score (NPS)", min_value=-100, max_value=100, value=30)

st.divider()
st.subheader("Your Business Health Score")

def calculate_score(revenue, churn, margin, nps):
    revenue_score = min(max((revenue + 50) / 150 * 100, 0), 100)
    churn_score = min(max((100 - churn), 0), 100)
    margin_score = min(max((margin + 50) / 150 * 100, 0), 100)
    nps_score = min(max((nps + 100) / 200 * 100, 0), 100)

    weighted_score = (
        revenue_score * 0.30 +
        churn_score * 0.25 +
        margin_score * 0.25 +
        nps_score * 0.20
    )
    return round(weighted_score, 1)

score = calculate_score(revenue_growth, churn_rate, profit_margin, nps_input)

st.metric(label="Overall Health Score", value=f"{score} / 100")

if score >= 70:
    st.success(f"Healthy business - your score of {score} is strong.")
elif score >= 40:
    st.success(f"Average health - your score of {score} has room to improve.")
else:
    st.error(f"At risk - your score of {score} needs attention.")
    
st.divider()
st.subheader("Metric Breakdown")

import plotly.express as px
import pandas as pd

breakdown = pd.DataFrame({
    "Metric": ["Revenue Growth", "Churn Rate", "Profit Margin", "Net Promoter Score"],
    "Score": [
        min(max((revenue_growth + 50) / 150 * 100, 0), 100),
        min(max((100 - churn_rate), 0), 100),
        min(max((profit_margin + 50) / 150 * 100, 0), 100),
        min(max((nps_input + 100) / 200 * 100, 0), 100)
    ]
})

fig = px.bar(breakdown, x="Metric", y="Score", range_y=[0,100],
            color="Score", color_continuous_scale="RdYlGn")
st.plotly_chart(fig)

st.divider()
st.subheader("Recomendations")

if churn_rate > 50:
    st.write("- High churn rate detected. Focus on customer retention strategies.")
if revenue_growth < 0:
    st.write("- Negative revenue growth. Review pricing and sales pipeline.")
if profit_margin < 10:
    st.write("- Low profit margin. Audit operating costs for inefficiencies.")
if nps_input < 0:
    st.write("- Negative NPS. Prioritize customer satisfaction improvements.")
if score >= 70:
    st.write("- Business looks healthy. Focus on sustaining current performance.")
