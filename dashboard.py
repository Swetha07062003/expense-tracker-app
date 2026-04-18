import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Expense Tracker Dashboard",
    page_icon="💰",
    layout="wide"
)

# -------------------------------------------------
# Custom CSS Styling
# -------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #eef2ff, #f8fafc);
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] * {
    color: white;
}

.header-box {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    padding: 30px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
}

.metric-box {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    border-left: 6px solid #2563eb;
    margin-bottom: 10px;
}

.metric-title {
    font-size: 15px;
    color: #6b7280;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #111827;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #111827;
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = pd.read_csv("data/expenses.csv")

# Change this only if your dataset has different column names
df.columns = ["Date", "Category", "Amount", "Payment", "Notes"]

# Convert date
df["Date"] = pd.to_datetime(df["Date"])

# Create Month column
df["Month"] = df["Date"].dt.strftime("%b %Y")

# -------------------------------------------------
# Header Section
# -------------------------------------------------
st.markdown("""
<div class="header-box">
    <h1>💰 Expense Tracker Dashboard</h1>
    <p style="font-size:18px;">
        Analyze spending trends, identify overspending, and understand where your money goes.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("🔎 Filter Your Data")

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=list(df["Category"].unique())
)

selected_payments = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["Payment"].unique(),
    default=list(df["Payment"].unique())
)

# Filter data
filtered_df = df[
    (df["Category"].isin(selected_categories)) &
    (df["Payment"].isin(selected_payments))
]

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------
total_spending = filtered_df["Amount"].sum()
average_spending = filtered_df["Amount"].mean()
highest_expense = filtered_df["Amount"].max()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">💸 Total Spending</div>
        <div class="metric-value">₹{total_spending:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">📈 Average Expense</div>
        <div class="metric-value">₹{average_spending:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">🚨 Highest Expense</div>
        <div class="metric-value">₹{highest_expense:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Overview",
    "🚨 High Expenses",
    "📂 Raw Data"
])

# -------------------------------------------------
# Overview Tab
# -------------------------------------------------
with tab1:

    col1, col2 = st.columns(2)

    # Category Spending
    with col1:
        st.markdown('<div class="section-title">Category-wise Spending</div>', unsafe_allow_html=True)

        category_total = (
            filtered_df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
            .sort_values(by="Amount", ascending=False)
        )

        fig_bar = px.bar(
            category_total,
            x="Category",
            y="Amount",
            color="Category",
            text="Amount",
            template="plotly_white"
        )

        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(
            showlegend=False,
            height=450,
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # Payment Method Pie Chart
    with col2:
        st.markdown('<div class="section-title">Payment Method Distribution</div>', unsafe_allow_html=True)

        payment_total = (
            filtered_df.groupby("Payment")["Amount"]
            .sum()
            .reset_index()
        )

        fig_pie = px.pie(
            payment_total,
            names="Payment",
            values="Amount",
            hole=0.55,
            template="plotly_white"
        )

        fig_pie.update_layout(
            height=450,
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    # Monthly Trend
    st.markdown('<div class="section-title">Monthly Spending Trend</div>', unsafe_allow_html=True)

    monthly_total = (
        filtered_df.groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    fig_line = px.line(
        monthly_total,
        x="Month",
        y="Amount",
        markers=True,
        template="plotly_white"
    )

    fig_line.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Month",
        yaxis_title="Amount Spent"
    )

    st.plotly_chart(fig_line, use_container_width=True)

# -------------------------------------------------
# High Expenses Tab
# -------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">Top 10 Highest Expense Transactions</div>', unsafe_allow_html=True)

    top_expenses = (
        filtered_df.sort_values(by="Amount", ascending=False)
        .head(10)
    )

    st.dataframe(
        top_expenses[["Date", "Category", "Amount", "Payment", "Notes"]],
        use_container_width=True
    )

# -------------------------------------------------
# Raw Data Tab
# -------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">Filtered Dataset</div>', unsafe_allow_html=True)

    st.dataframe(filtered_df, use_container_width=True)